# Disputas / Chargeback

## Bounded Context

Processa contestações de transações e o fluxo de chargeback com a bandeira

**Sistemas de origem típicos**: Sistema de disputas

**Tipo (DDD)**: Support

---

## Produtos de Dados

| Camada | Produto de dados | Descrição | Consumidores | Dono | Status |
|--------|-----------------|-----------|--------------|------|--------|
| Core | `core_dispute_chargeback` | Registro de disputas abertas e status junto à bandeira | Atendimento, financeiro, Time de Performance | Time de Disputas | V0 — a validar |
| Integration | `integration_dispute_transaction` | Cruza a disputa com a transação original e as regras da bandeira aplicável | Fraude, financeiro, Time de Performance | Time de Disputas | V0 — a validar |
| Analytics | `analytics_dispute_rate` | Taxa de disputa por lojista, categoria e bandeira | Risco, relacionamento com bandeiras, Time de Performance | Time de Disputas | V0 — a validar |
