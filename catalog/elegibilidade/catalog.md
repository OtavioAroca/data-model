# Elegibilidade

## Bounded Context

Avalia se um cliente pode receber uma oferta de cartão, e sob quais condições

**Sistemas de origem típicos**: Motor de elegibilidade / bureaus de crédito

**Tipo (DDD)**: Core

---

## Produtos de Dados

| Camada | Produto de dados | Descrição | Consumidores | Dono | Status |
|--------|-----------------|-----------|--------------|------|--------|
| Core | `core_eligibility_assessment` | Resultado da avaliação de política de crédito para uma oferta de cartão | Onboarding, motor de ofertas, Time de Performance | Time de Crédito/Elegibilidade | V0 — a validar |
| Integration | `integration_customer_offer` | Cruza elegibilidade com dados cadastrais e histórico para consolidar a oferta personalizada | Marketing, canais de venda, Time de Performance | Time de Crédito/Elegibilidade | V0 — a validar |
| Analytics | `analytics_eligibility_conversion` | Taxa de conversão de elegíveis em propostas iniciadas | Growth, marketing, Time de Performance | Time de Crédito/Elegibilidade | V0 — a validar |
