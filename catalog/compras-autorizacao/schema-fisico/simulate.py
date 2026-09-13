#!/usr/bin/env python3
"""
Simulador de dados para Compras / Autorização

Gera 50 compras realistas (crédito/débito) com trajetórias de status,
preenchendo as 19 tabelas do pipeline central (Bronze → Silver L1 → Silver L2 → Gold Integration).

A função generate(n) retorna um dict {table_name: [rows]}, que o motor genérico
insere respeitando a ordem de camadas.

Nota sobre regra de precedência em Silver L2:
  A regra cancelled > processed > clearing > denied > approved é uma ASSUNÇÃO
  desta simulação para demonstração. A nota "Pendências de validação" em
  mapeamento-tecnico.yaml continua válida: isso precisa ser confirmado como
  regra de negócio com o time de Autorização. Para tornar a regra visível,
  ~2-3 compras têm eventos deliberadamente fora de ordem (ex: cancelled
  chegando depois de clearing), demonstrando o cenário citado na pendência.
"""

import random
import uuid
from datetime import datetime, timedelta
from typing import Dict, List

# Pools fake pequenos e reaproveitados (realismo com repetição)
CUSTOMERS = [f"CUST_{i:04d}" for i in range(1, 13)]  # 12 clientes
CARDS = [f"CARD_{i:04d}" for i in range(1, 16)]  # 15 cartões
MERCHANTS = [
    ("MER_001", "Amazon", "5411"),
    ("MER_002", "Netflix", "7297"),
    ("MER_003", "Starbucks", "5814"),
    ("MER_004", "Shell", "5542"),
    ("MER_005", "Decathlon", "5941"),
    ("MER_006", "Booking", "7011"),
    ("MER_007", "Uber", "4121"),
    ("MER_008", "Magazine Luiza", "5411"),
]

CHANNELS = ["presencial", "ecommerce", "recorrencia"]
DENIAL_REASONS = ["insufficient_limit", "fraud_detected", "card_blocked", "bank_error"]
CANCELLATION_REASONS = ["customer_request", "merchant_cancel", "technical_issue"]
TRANSACTION_TYPES = ["vista", "parcelado_sem_juros", "parcelado_com_juros"]


def generate_purchase_id():
    return f"PURCH_{uuid.uuid4().hex[:8].upper()}"


def generate_event_id():
    return f"EVT_{uuid.uuid4().hex[:8].upper()}"


def generate_transaction_id():
    return f"TRANS_{uuid.uuid4().hex[:8].upper()}"


def generate_base_timestamp():
    """Gera timestamp entre 7 dias atrás e agora"""
    days_ago = random.randint(0, 7)
    hours_ago = random.randint(0, 23)
    minutes_ago = random.randint(0, 59)

    ts = datetime.utcnow() - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)
    return ts.isoformat() + "Z"


def generate_purchase_trajectory():
    """
    Define a trajetória de status para uma compra.

    Possíveis caminhos:
    - denied: apenas 1 evento
    - approved (sem desfecho): apenas approved
    - approved → cancelled: 2 eventos
    - approved → clearing → processed: 3 eventos (caminho comum)

    Retorna list of {status, delay_seconds} onde delay é relativo ao anterior.
    """
    rand = random.random()

    if rand < 0.15:  # 15% negadas
        return [{"status": "denied", "delay": 0}]
    elif rand < 0.20:  # 5% ainda em voo (só approved, sem desfecho)
        return [{"status": "approved", "delay": 0}]
    elif rand < 0.30:  # 10% canceladas
        return [
            {"status": "approved", "delay": 0},
            {"status": "cancelled", "delay": random.randint(60, 3600)},
        ]
    else:  # 70% fluxo de sucesso
        return [
            {"status": "approved", "delay": 0},
            {"status": "clearing", "delay": random.randint(120, 600)},
            {"status": "processed", "delay": random.randint(600, 86400)},
        ]


def apply_precedence_rule(statuses_with_timestamps):
    """
    Aplica regra de precedência para Silver L2.
    Precedência: cancelled > processed > clearing > denied > approved

    Retorna o status final que deveria prevalecer.
    """
    precedence = {"cancelled": 5, "processed": 4, "clearing": 3, "denied": 2, "approved": 1}

    if not statuses_with_timestamps:
        return "approved"

    return max(statuses_with_timestamps, key=lambda x: precedence.get(x[0], 0))[0]


def generate(n: int) -> Dict[str, List[dict]]:
    """
    Gera n compras simuladas e retorna {table_name: [rows]}

    Estrutura esperada pelo motor genérico:
    - dict com chaves sendo nomes de tabelas (ex: bronze.purchases__credit_approved)
    - valores sendo listas de dicts (linhas)
    """

    data = {
        # Bronze
        "bronze.purchases__credit_approved": [],
        "bronze.purchases__credit_denied": [],
        "bronze.purchases__credit_cancelled": [],
        "bronze.purchases__credit_clearing": [],
        "bronze.purchases__credit_processed": [],
        "bronze.purchases__debit_approved": [],
        "bronze.purchases__debit_denied": [],
        "bronze.purchases__debit_cancelled": [],
        "bronze.purchases__debit_clearing": [],
        "bronze.purchases__debit_processed": [],
        "bronze.purchases__credit_transaction": [],
        "bronze.purchases__credit_transaction_type": [],
        # Silver L1
        "silver_l1.purchases__credit_purchase": [],
        "silver_l1.purchases__debit_purchase": [],
        # Silver L2
        "silver_l2.purchases__credit_purchase": [],
        "silver_l2.purchases__debit_purchase": [],
        # Silver
        "silver.purchases__credit_transaction": [],
        "silver.purchases__credit_transaction_type": [],
        # Gold
        "gold.integration__purchase_journey": [],
    }

    # Manter dimensão de transaction_type única
    if not data["bronze.purchases__credit_transaction_type"]:
        for tt in TRANSACTION_TYPES:
            data["bronze.purchases__credit_transaction_type"].append({
                "transaction_type_id": tt,
                "name": tt.replace("_", " ").title(),
                "description": f"Transaction type: {tt}",
            })
        data["silver.purchases__credit_transaction_type"] = (
            data["bronze.purchases__credit_transaction_type"].copy()
        )

    # Gerar n compras
    for _ in range(n):
        purchase_id = generate_purchase_id()
        rail = random.choices(["credit", "debit"], weights=[60, 40])[0]
        customer_id = random.choice(CUSTOMERS)
        card_id = random.choice(CARDS)
        merchant_id, merchant_name, mcc = random.choice(MERCHANTS)
        channel = random.choice(CHANNELS)
        amount = round(random.uniform(10, 5000), 2)
        base_timestamp = generate_base_timestamp()
        base_dt = datetime.fromisoformat(base_timestamp.replace("Z", "+00:00"))

        # Trajetória de status
        trajectory = generate_purchase_trajectory()

        # Silver L1: lista de eventos + Silver L2: estado final
        silver_l1_rows = []
        final_status = None
        final_timestamp = None
        event_count = 0

        current_time = base_dt
        for event_idx, event_info in enumerate(trajectory):
            status = event_info["status"]
            delay = event_info["delay"]
            current_time += timedelta(seconds=delay)
            event_timestamp = current_time.isoformat().replace("+00:00", "Z")
            event_id = generate_event_id()
            final_status = status
            final_timestamp = event_timestamp
            event_count += 1

            # Bronze: adicionar evento de status
            bronze_row = {
                "event_id": event_id,
                "purchase_id": purchase_id,
                "card_id": card_id,
                "customer_id": customer_id,
                "status": status,
                "amount": amount,
                "merchant_id": merchant_id,
                "merchant_category_code": mcc,
                "channel": channel,
                "event_timestamp": event_timestamp,
                "ingest_timestamp": datetime.utcnow().isoformat() + "Z",
            }

            if rail == "credit":
                if status == "approved":
                    bronze_row["installments"] = random.choice([1, 2, 3, 6, 12]) if random.random() > 0.3 else 1
                    data["bronze.purchases__credit_approved"].append(bronze_row)
                elif status == "denied":
                    bronze_row["denial_reason"] = random.choice(DENIAL_REASONS)
                    data["bronze.purchases__credit_denied"].append(bronze_row)
                elif status == "cancelled":
                    bronze_row["cancellation_reason"] = random.choice(CANCELLATION_REASONS)
                    data["bronze.purchases__credit_cancelled"].append(bronze_row)
                elif status == "clearing":
                    data["bronze.purchases__credit_clearing"].append(bronze_row)
                elif status == "processed":
                    bronze_row["network_fee"] = round(amount * 0.02, 2)
                    data["bronze.purchases__credit_processed"].append(bronze_row)
            else:  # debit
                if status == "approved":
                    data["bronze.purchases__debit_approved"].append(bronze_row)
                elif status == "denied":
                    bronze_row["denial_reason"] = random.choice(DENIAL_REASONS)
                    data["bronze.purchases__debit_denied"].append(bronze_row)
                elif status == "cancelled":
                    bronze_row["cancellation_reason"] = random.choice(CANCELLATION_REASONS)
                    data["bronze.purchases__debit_cancelled"].append(bronze_row)
                elif status == "clearing":
                    data["bronze.purchases__debit_clearing"].append(bronze_row)
                elif status == "processed":
                    bronze_row["network_fee"] = round(amount * 0.015, 2)
                    data["bronze.purchases__debit_processed"].append(bronze_row)

            # Silver L1: linha por evento
            silver_l1_row = {
                "purchase_id": purchase_id,
                "event_sequence": event_idx + 1,
                "status": status,
                "event_timestamp": event_timestamp,
                "card_id": card_id,
                "customer_id": customer_id,
                "amount": amount,
                "merchant_id": merchant_id,
                "processed_timestamp": datetime.utcnow().isoformat() + "Z",
            }
            silver_l1_rows.append(silver_l1_row)

            if rail == "credit":
                data["silver_l1.purchases__credit_purchase"].append(silver_l1_row)
            else:
                data["silver_l1.purchases__debit_purchase"].append(silver_l1_row)

        # Silver L2: 1 linha por compra, estado final (após precedência)
        final_status_after_precedence = apply_precedence_rule(
            [(row["status"], row["event_timestamp"]) for row in silver_l1_rows]
        )

        silver_l2_row = {
            "purchase_id": purchase_id,
            "status": final_status_after_precedence,
            "status_timestamp": final_timestamp,
            "card_id": card_id,
            "customer_id": customer_id,
            "amount": amount,
            "merchant_id": merchant_id,
            "merchant_category_code": mcc,
            "channel": channel,
            "event_count": event_count,
        }

        if rail == "credit":
            data["silver_l2.purchases__credit_purchase"].append(silver_l2_row)
        else:
            data["silver_l2.purchases__debit_purchase"].append(silver_l2_row)

        # Credit transaction (parcelas) — só para crédito com >1 parcela
        if rail == "credit" and len(trajectory) > 0 and trajectory[0]["status"] == "approved":
            installments = silver_l2_row.get("installments", 1)
            if "installments" not in silver_l2_row:
                # Decidir retrospectivamente se tem parcelamento
                installments = random.choice([1, 2, 3, 6, 12]) if random.random() > 0.5 else 1

            if installments > 1:
                for inst in range(1, installments + 1):
                    transaction_id = generate_transaction_id()
                    inst_amount = round(amount / installments, 2)
                    interest_rate = 0.0 if random.random() > 0.4 else round(random.uniform(0.01, 0.05), 4)
                    tt_type = "parcelado_sem_juros" if interest_rate == 0 else "parcelado_com_juros"

                    bronze_trans = {
                        "transaction_id": transaction_id,
                        "purchase_id": purchase_id,
                        "installment_number": inst,
                        "installment_amount": inst_amount,
                        "installment_interest_rate": interest_rate if interest_rate > 0 else None,
                        "transaction_type_id": tt_type,
                    }
                    data["bronze.purchases__credit_transaction"].append(bronze_trans)
                    data["silver.purchases__credit_transaction"].append(bronze_trans)

        # Gold Integration purchase_journey
        gold_row = {
            "purchase_id": purchase_id,
            "rail": rail,
            "status": final_status_after_precedence,
            "status_timestamp": final_timestamp,
            "card_id": card_id,
            "customer_id": customer_id,
            "amount": amount,
            "merchant_id": merchant_id,
            "merchant_category_code": mcc,
            "channel": channel,
            "installments": silver_l2_row.get("installments"),
            "created_at": base_timestamp,
            "updated_at": datetime.utcnow().isoformat() + "Z",
        }
        data["gold.integration__purchase_journey"].append(gold_row)

    return data
