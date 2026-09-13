# Core / Integration / Analytics — Camadas de Produto de Dados

## Visão geral

Este arquivo assume que você já sabe o que é um produto de dados — se não, comece por [produto-de-dados.md](./produto-de-dados.md).

A classificação **Core / Integration / Analytics** agrupa produtos de dados (as linhas da aba "Catálogo V0") por **escopo de negócio** — quantos bounded contexts (subdomínios) cada produto cruza e para quem ele foi moldado.

Cada camada tem um contrato, um dono, consumidores e uma cadência de atualização bem definidos.

---

## Core

Um produto **Core** representa exatamente um bounded context, sem cruzamento.

- **Escopo**: 1 subdomínio.
- **Contrato**: contém apenas dados que cabem naturalmente dentro de um bounded context específico.
- **Dono**: o time responsável pelo bounded context.
- **Consumidores**: principalmente outros produtos (Integration, Analytics) que o usam como insumo; às vezes consumo externo (ex: auditoria, sistemas vizinhos).

### Exemplo

**Subdomínio: Compras / Autorização**

- `core_credit_purchase` — histórico completo de compras de crédito (tabela física: `silver_l2.purchases__credit_purchase`).
- `core_debit_purchase` — histórico completo de compras de débito (tabela física: `silver_l2.purchases__debit_purchase`).

Cada um é isolado — não cruza com o outro, nem com Disputas, nem com Fatura. A tabela fica em Silver L2 (estado atual, materializado) porque é consumida **constantemente** por Integration e Analytics.

---

## Integration

Um produto **Integration** cruza dois ou mais bounded contexts.

- **Escopo**: ≥2 subdomínios.
- **Contrato**: padroniza schema entre múltiplas fontes (ex: crédito e débito têm layouts nativos diferentes em Bronze; Integration padroniza), enriquece com dados de outros contextos, estabelece relacionamentos de negócio.
- **Dono**: time responsável pela sinergia entre os contextos (muitas vezes uma equipe de plataforma de dados, não o dono de um único subdomínio).
- **Consumidores**: Analytics, e ocasionalmente aplicações finais (BI, atendimento, risco).

### Exemplo

**Subdomínio: Compras / Autorização (cruza Crédito + Débito + Disputas)**

- `integration_purchase_journey` — tabela physical: `gold.integration__purchase_journey`.

Cruza:
- `core_credit_purchase` (crédito)
- `core_debit_purchase` (débito)
- Detalhamento de parcelas de crédito (de `core_credit_transaction`)
- Estornos vindo de Disputas (de `core_dispute_chargeback`)

Resultado: um único grão de "compra com sua história completa", independente se é crédito ou débito, com parcelas relacionadas, com estornos já inclusos. Schema único (sem "é crédito? então essas colunas; é débito? então aquelas outras").

---

## Analytics

Um produto **Analytics** é moldado para um **caso de uso específico de consumo final**.

- **Escopo**: pode ser 1 bounded context, mas focado em um aspecto específico (ex: taxa de aprovação, latência, comportamento de gasto).
- **Contrato**: já agregado, pré-calculado, com dimensões e métricas prontas para o visualizar em dashboard ou report.
- **Dono**: time de Analytics ou de Dados, em coordenação com o dono do caso de uso (Risk, Marketing, Financeiro).
- **Consumidores**: stakeholders finais (analistas, gerentes, sistemas de decisão).
- **Nomenclatura**: em português (porque o público final é menos técnico).

### Exemplo

**Subdomínio: Compras / Autorização**

- `analytics_extrato_cliente` — extrair do cliente legalmente completo (tabela: `gold.analytics__extrato_cliente`). Consumidores: app do cliente, atendimento.
- `analytics_comportamento_gasto` — métricas agregadas (ticket médio, categorias, frequência). Consumidores: risco de crédito, marketing/rewards.
- `analytics_taxa_aprovacao_compra` — taxa de aprovação/negação por segmento, canal, bandeira. Consumidores: risco, produto.
- `analytics_latencia_liquidacao_compra` — tempo médio entre aprovação e liquidação. Consumidores: operações, financeiro (precisa de `silver_l1` com múltiplos timestamps, não `silver_l2`).

Cada um é seu próprio produto, com seu próprio propósito, consumidores claros e nomes em português.

---

## Convenção de nomenclatura

Produto Core e Integration usam **inglês**:
- `core_eligibility_assessment`
- `integration_purchase_journey`

Por quê? Porque a pessoa que lê é engenheiro/data engineer — tem convenção de inglês.

Analytics usa **português**:
- `analytics_extrato_cliente`
- `analytics_comportamento_gasto`
- `analytics_taxa_aprovacao_compra`

Por quê? Porque a pessoa que consulta é analista de risco, gerente de marketing, ou contador — menos técnica, menos acostumada a lê nomes em inglês. O termo português reduz fricção.

---

## Tabela resumo

| Camada | Escopo | Dono | Consumidores | Exemplo | Tabela física |
|--------|--------|------|--------------|---------|----------------|
| **Core** | 1 bounded context | Time do subdomínio | Integration, Analytics, ocasionalmente auditoria | `core_credit_purchase` (só crédito) | `silver_l2.purchases__credit_purchase` |
| **Integration** | ≥2 bounded contexts | Time de plataforma de dados | Analytics, ocasionalmente BI/app final | `integration_purchase_journey` (crédito + débito + disputas) | `gold.integration__purchase_journey` |
| **Analytics** | 1 ou ≥2, mas focado em caso de uso | Time de Analytics / Dados | Stakeholders finais (risco, marketing, financeiro, operações) | `analytics_taxa_aprovacao_compra` (taxa de aprovação) | `gold.analytics__taxa_aprovacao_compra` |

---

## Nota: não confundir com Core (DDD) nem Core (camada medalhão)

Três significados diferentes de "Core":

1. **Core (DDD)** = subdomínio com importância estratégica (ex: Elegibilidade é Core, Cobrança é Support).
   - Ver [ddd.md](./ddd.md).

2. **Core (camada medalhão)** — não existe explicitamente, mas seria "stage 0" de processamento. O termo usado é Bronze/Silver/Gold.
   - Ver [camada-medalhao.md](./camada-medalhao.md).

3. **Core (produto de dados)** = produto que representa exatamente 1 bounded context, sem cruzamento.
   - Este arquivo.

Um subdomínio Core (DDD) pode gerar produtos em qualquer camada (Core, Integration, Analytics). Um subdomínio Support pode gerar um produto Core (produto de dados). São eixos independentes.
