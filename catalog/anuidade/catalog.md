# Anuidade

## Bounded Context

Calcula, cobra e administra isenções/negociação da anuidade do cartão

**Sistemas de origem típicos**: Motor de anuidade (regras de isenção e negociação)

**Tipo (DDD)**: Support

---

## Produtos de Dados

| Camada | Produto de dados | Descrição | Consumidores | Dono | Status |
|--------|-----------------|-----------|--------------|------|--------|
| Core | `core_annual_fee_rule` | Regras de cálculo, isenção por gasto mínimo e negociação de anuidade aplicadas à conta | Fatura, atendimento, Time de Performance | Time de Anuidade | V0 — a validar |
| Integration | `integration_annual_fee_statement` | Cruza a decisão de anuidade (cobrar, isentar, parcelar) com a fatura onde ela é lançada | Faturamento, financeiro, Time de Performance | Time de Anuidade | V0 — a validar |
| Analytics | `analytics_annual_fee_waiver` | Taxa de isenção concedida e seu impacto em receita, por segmento de cliente | Financeiro, marketing/retenção, Time de Performance | Time de Anuidade | V0 — a validar |
