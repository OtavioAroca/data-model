# Conta Cartão

## Bounded Context

Representa o relacionamento contratual entre cliente e produto cartão

**Sistemas de origem típicos**: Core banking de contas

**Tipo (DDD)**: Core

---

## Produtos de Dados

| Camada | Produto de dados | Descrição | Consumidores | Dono | Status |
|--------|-----------------|-----------|--------------|------|--------|
| Core | `core_card_account` | Estado da conta cartão (ativa, bloqueada, encerrada) e seus atributos contratuais | Praticamente todos os demais subdomínios, Time de Performance | Time de Conta/Core Banking | V0 — a validar |
| Integration | `integration_customer_account_view` | Cruza a conta cartão com dados cadastrais do cliente (CRM) e outros produtos bancários | Atendimento, visão 360, Time de Performance | Time de Conta/Core Banking | V0 — a validar |
| Analytics | `analytics_account_health` | Indicadores de saúde da conta: atividade, atraso, engajamento | Risco, retenção, Time de Performance | Time de Conta/Core Banking | V0 — a validar |
