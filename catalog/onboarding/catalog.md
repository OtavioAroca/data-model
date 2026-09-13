# Onboarding

## Bounded Context

Conduz a proposta, validação de identidade (KYC) e abertura da conta cartão

**Sistemas de origem típicos**: Sistema de proposta, KYC/antifraude cadastral

**Tipo (DDD)**: Core

---

## Produtos de Dados

| Camada | Produto de dados | Descrição | Consumidores | Dono | Status |
|--------|-----------------|-----------|--------------|------|--------|
| Core | `core_card_application` | Dados da proposta e etapas do funil de abertura de conta | Integration de onboarding, auditoria, Time de Performance | Time de Onboarding | V0 — a validar |
| Core | `core_kyc_validation` | Resultado das validações de identidade e antifraude cadastral | Onboarding, compliance, Time de Performance | Time de Onboarding | V0 — a validar |
| Integration | `integration_onboarding_journey` | Une proposta, KYC e elegibilidade em uma linha do tempo única do funil | Produto, atendimento, BI, Time de Performance | Time de Onboarding | V0 — a validar |
| Analytics | `analytics_onboarding_funnel` | Taxa de conversão e abandono por etapa do funil de abertura | Produto, marketing, Time de Performance | Time de Onboarding | V0 — a validar |
