# Cobrança

## Bounded Context

Trata contas em atraso, régua de contato e negociação

**Sistemas de origem típicos**: Sistema de cobrança/régua

**Tipo (DDD)**: Support

---

## Produtos de Dados

| Camada | Produto de dados | Descrição | Consumidores | Dono | Status |
|--------|-----------------|-----------|--------------|------|--------|
| Core | `core_collections_status` | Estágio de cobrança: régua, tentativas de contato, acordo firmado | Atendimento, financeiro, Time de Performance | Time de Cobrança | V0 — a validar |
| Integration | `integration_delinquent_customer` | Cruza cobrança com conta, fatura e limite para visão consolidada de risco | Risco, crédito, Time de Performance | Time de Cobrança | V0 — a validar |
| Analytics | `analytics_collections_effectiveness` | Taxa de recuperação por régua e canal de cobrança | Risco, operações de cobrança, Time de Performance | Time de Cobrança | V0 — a validar |
