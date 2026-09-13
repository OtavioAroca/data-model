# Fatura

## Bounded Context

Gera e fecha a fatura periódica com as transações e encargos do ciclo

**Sistemas de origem típicos**: Billing engine

**Tipo (DDD)**: Core

---

## Produtos de Dados

| Camada | Produto de dados | Descrição | Consumidores | Dono | Status |
|--------|-----------------|-----------|--------------|------|--------|
| Core | `core_statement_closing` | Fechamento de fatura: valores, datas e encargos do ciclo | Pagamento, cobrança, app do cliente, Time de Performance | Time de Faturamento | V0 — a validar |
| Integration | `integration_statement_detail` | Fatura cruzada com transações, parcelamento e encargos linha a linha | App do cliente, atendimento, Time de Performance | Time de Faturamento | V0 — a validar |
| Analytics | `analytics_statement_delinquency` | Indicadores de atraso e inadimplência por fatura | Cobrança, risco, Time de Performance | Time de Faturamento | V0 — a validar |
