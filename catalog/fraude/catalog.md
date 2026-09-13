# Fraude

## Bounded Context

Avalia risco de fraude em tempo real e retroativamente

**Sistemas de origem típicos**: Motor antifraude

**Tipo (DDD)**: Core

---

## Produtos de Dados

| Camada | Produto de dados | Descrição | Consumidores | Dono | Status |
|--------|-----------------|-----------|--------------|------|--------|
| Core | `core_fraud_score` | Score bruto de risco de fraude calculado pelo motor antifraude | Autorização, disputas, Time de Performance | Time de Fraude | V0 — a validar |
| Analytics | `analytics_fraud_realtime` | Score de fraude consumido em tempo real na decisão de autorização | Motor antifraude, autorização, Time de Performance | Time de Fraude | V0 — a validar |
| Analytics | `analytics_fraud_losses` | Perdas financeiras por fraude, para relatório de risco | Risco, financeiro, compliance, Time de Performance | Time de Fraude | V0 — a validar |
