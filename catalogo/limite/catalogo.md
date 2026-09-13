# Limite

## Bounded Context

Concede, ajusta e controla o limite de crédito disponível na conta cartão

**Sistemas de origem típicos**: Motor de crédito/limite

**Tipo (DDD)**: Core

---

## Produtos de Dados

| Camada | Produto de dados | Descrição | Consumidores | Dono | Status |
|--------|-----------------|-----------|--------------|------|--------|
| Core | `core_credit_limit` | Limite concedido e histórico de alterações (aumento, redução, bloqueio) | Compras/autorização, cobrança, Time de Performance | Time de Crédito/Limite | V0 — a validar |
| Integration | `integration_limit_utilization` | Cruza limite concedido com transações e fatura para calcular limite disponível em tempo real | Autorização, app do cliente, Time de Performance | Time de Crédito/Limite | V0 — a validar |
| Analytics | `analytics_limit_policy` | Efetividade de políticas de aumento/redução de limite sobre inadimplência e uso | Risco, crédito, Time de Performance | Time de Crédito/Limite | V0 — a validar |
