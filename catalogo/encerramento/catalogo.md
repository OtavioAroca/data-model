# Encerramento

## Bounded Context

Processa o cancelamento definitivo de cartão ou conta

**Sistemas de origem típicos**: Core banking de contas

**Tipo (DDD)**: Support

---

## Produtos de Dados

| Camada | Produto de dados | Descrição | Consumidores | Dono | Status |
|--------|-----------------|-----------|--------------|------|--------|
| Core | `core_account_closure` | Registro e motivo de encerramento de cartão ou conta | Atendimento, compliance, Time de Performance | Time de Conta/Core Banking | V0 — a validar |
| Analytics | `analytics_card_churn` | Taxa e motivos de churn do produto cartão | Produto, retenção, Time de Performance | Time de Conta/Core Banking | V0 — a validar |
