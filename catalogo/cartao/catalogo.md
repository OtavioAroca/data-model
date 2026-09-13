# Cartão

## Bounded Context

Gerencia o ciclo de vida do plástico/virtual: emissão, ativação, bloqueio, reemissão

**Sistemas de origem típicos**: Sistema de emissão de cartões

**Tipo (DDD)**: Core

---

## Produtos de Dados

| Camada | Produto de dados | Descrição | Consumidores | Dono | Status |
|--------|-----------------|-----------|--------------|------|--------|
| Core | `core_card_lifecycle` | Eventos de emissão, ativação, bloqueio, reemissão e cancelamento do plástico/virtual | Atendimento, fraude, onboarding, Time de Performance | Time de Emissão | V0 — a validar |
| Analytics | `analytics_card_activation` | Tempo até ativação e taxa de ativação por canal de entrega | Produto, operações, Time de Performance | Time de Emissão | V0 — a validar |
