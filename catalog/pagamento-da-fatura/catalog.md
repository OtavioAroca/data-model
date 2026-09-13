# Pagamento da Fatura

## Bounded Context

Registra e concilia os pagamentos feitos pelo cliente contra a fatura, e estrutura o saldo devedor em parcelas (rotativo) quando o pagamento é parcial

**Sistemas de origem típicos**: Sistema de pagamentos/liquidação

**Tipo (DDD)**: Support

---

## Produtos de Dados

| Camada | Produto de dados | Descrição | Consumidores | Dono | Status |
|--------|-----------------|-----------|--------------|------|--------|
| Core | `core_statement_payment` | Registros de pagamento: valor, data e forma de pagamento | Fatura, conciliação financeira, Time de Performance | Time de Pagamentos | V0 — a validar |
| Core | `core_revolving_balance_installments` | Estrutura de parcelas do saldo rotativo quando o pagamento é parcial, incluindo juros aplicados | Fatura, cobrança, financeiro, Time de Performance | Time de Pagamentos | V0 — a validar |
| Integration | `integration_payment_reconciliation` | Cruza pagamento com fatura para calcular saldo remanescente | Cobrança, financeiro, Time de Performance | Time de Pagamentos | V0 — a validar |
| Analytics | `analytics_payment_behavior` | Padrão de pagamento do cliente: mínimo, total ou parcial | Risco de crédito, cobrança, Time de Performance | Time de Pagamentos | V0 — a validar |
| Analytics | `analytics_revolving_revenue` | Receita de juros e encargos do saldo rotativo/parcelado | Financeiro/contabilidade, Time de Performance | Time de Pagamentos | V0 — a validar |
