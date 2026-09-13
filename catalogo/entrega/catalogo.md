# Entrega

## Bounded Context

Rastreia a entrega física do cartão, do despacho até a confirmação de recebimento

**Sistemas de origem típicos**: Integração com transportadora/Correios

**Tipo (DDD)**: Support

---

## Produtos de Dados

| Camada | Produto de dados | Descrição | Consumidores | Dono | Status |
|--------|-----------------|-----------|--------------|------|--------|
| Core | `core_delivery_tracking` | Eventos de rastreio (despachado, em trânsito, entregue, tentativa falha) por transportadora | Atendimento, emissão, Time de Performance | Time de Logística | V0 — a validar |
| Integration | `integration_card_delivery` | Cruza o rastreio de entrega com o ciclo de vida do cartão (emissão → entrega → ativação) | Emissão, onboarding, Time de Performance | Time de Logística | V0 — a validar |
| Analytics | `analytics_delivery_sla` | Tempo médio de entrega e taxa de insucesso por transportadora e região | Operações, atendimento, Time de Performance | Time de Logística | V0 — a validar |
