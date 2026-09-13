# Compras / Autorização

## Bounded Context

Autoriza e captura as transações realizadas com o cartão, incluindo o plano de parcelamento decidido no ato da compra

**Sistemas de origem típicos**: Switch de autorização, rede/bandeira

**Tipo (DDD)**: Core

---

## Produtos de Dados

| Camada | Produto de dados | Descrição | Consumidores | Dono | Status |
|--------|-----------------|-----------|--------------|------|--------|
| Core | `core_credit_purchase` | Ciclo de vida da compra de crédito (approved → denied/cancelled → clearing → processed) no rail de crédito, incluindo parcelamento decidido no ato da compra quando aplicável | Silver interno, auditoria, financeiro, Time de Performance | Time de Autorização · Crédito | V0 — a validar |
| Core | `core_debit_purchase` | Ciclo de vida da compra de débito (approved → denied/cancelled → clearing → processed) no rail de débito | Silver interno, auditoria, financeiro, Time de Performance | Time de Autorização · Débito | V0 — a validar |
| Integration | `integration_purchase_journey` | Une purchase de crédito e débito (schema padronizado) com o detalhamento de parcelas do crédito e o estorno vindo de Disputas — grão de compra, com parcelas relacionadas quando existirem | Risco, fraude, atendimento, Time de Performance | Time de Autorização | V0 — a validar |
| Analytics | `analytics_extrato_cliente` | Extrato do cliente com completude e ordenação cronológica exigidas legalmente | App, atendimento, Time de Performance | Time de Autorização | V0 — a validar |
| Analytics | `analytics_comportamento_gasto` | Métricas agregadas de gasto: ticket médio, categorias, frequência | Risco de crédito, marketing/rewards, Time de Performance | Time de Autorização | V0 — a validar |
| Analytics | `analytics_taxa_aprovacao_compra` | Taxa de aprovação/negação/cancelamento de compras por segmento, canal e bandeira | Risco, produto, Time de Performance | Time de Autorização | V0 — a validar |
| Analytics | `analytics_motivos_negacao_compra` | Motivos de negação de compra agregados, para calibrar políticas de crédito e limite | Risco de crédito, Time de Limite, Time de Performance | Time de Autorização | V0 — a validar |
| Analytics | `analytics_ranking_lojista_categoria` | Ranking de lojistas e categorias (MCC) mais usados pelos clientes | Marketing, parcerias comerciais, Time de Performance | Time de Autorização | V0 — a validar |
| Analytics | `analytics_adocao_parcelamento` | Adoção e perfil de parcelamento nas compras (nº de parcelas, ticket médio parcelado) | Produto, financeiro, Time de Performance | Time de Autorização | V0 — a validar |
| Analytics | `analytics_latencia_liquidacao_compra` | Tempo entre aprovação e liquidação (clearing/processed) da compra, para monitorar SLA operacional | Operações, financeiro, Time de Performance | Time de Autorização | V0 — a validar |
| Analytics | `analytics_mix_canal` | Mix de compras por canal (presencial, e-commerce, recorrência) | Produto, marketing, Time de Performance | Time de Autorização | V0 — a validar |
| Analytics | `analytics_gasto_internacional` | Volume e câmbio de compras internacionais | Tesouraria, compliance, Time de Performance | Time de Autorização | V0 — a validar |
| Analytics | `analytics_gasto_elegivel_rewards` | Volume de gasto elegível a cashback/pontos, por cliente e categoria | Rewards, marketing, Time de Performance | Time de Autorização | V0 — a validar |
