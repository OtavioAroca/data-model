# Benefícios / Rewards

## Bounded Context

Administra pontos, cashback e resgates associados ao uso do cartão

**Sistemas de origem típicos**: Plataforma de rewards

**Tipo (DDD)**: Generic

---

## Produtos de Dados

| Camada | Produto de dados | Descrição | Consumidores | Dono | Status |
|--------|-----------------|-----------|--------------|------|--------|
| Core | `core_points_cashback` | Saldo e eventos de acúmulo/resgate de pontos ou cashback | App do cliente, parceiros, Time de Performance | Time de Rewards | V0 — a validar |
| Analytics | `analytics_rewards_engagement` | Uso de benefícios por segmento de cliente | Marketing, produto, Time de Performance | Time de Rewards | V0 — a validar |
