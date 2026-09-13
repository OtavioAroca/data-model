# Compras / Autorização — Mapeamento Técnico

## Contexto

Piloto de mapeamento técnico — subdomínio Compras / Autorização (Core + Integration).

Para entender a camada medalhão (Bronze/Silver/Gold) e Silver L1 vs L2, ver [Conhecimento Base](../../kb/camada-medalhao.md).

---

## Notas do Piloto

### Correção de nomenclatura

Os 5 tópicos de status (approved/denied/cancelled/clearing/processed) alimentam a fonte 'purchase' (grão de compra), não 'transaction'. A fonte 'transaction' é outra coisa — só existe em crédito, tópico único, carrega o detalhamento de parcelas (grão de parcela, N por compra). Dentro de 'transaction', o ID da compra vem preenchido na linha da compra e nulo nas linhas de parcela — sugere mistura de cabeçalho e detalhe na mesma fonte, a resolver no desenho de schema físico.

### Pendências de validação

(1) A regra de precedência de status em L2 é regra de NEGÓCIO, não dedup técnico por timestamp de chegada — precisa ser definida pelo time de domínio (ex: um cancelled deve sempre prevalecer mesmo chegando depois de um clearing?). (2) Se risco/fraude/atendimento também precisam do histórico completo, além do estado atual — hoje não confirmado. (3) Se débito tem equivalente ao tópico transaction_type do crédito — hoje não confirmado.

### Produto vs. insumo interno

Sem consumidor externo confirmado, core_credit_transaction e core_credit_transaction_type não aparecem como linha própria no Catálogo V0 — continuam Core (fonte única, sem cruzamento de domínio), só não são produtos expostos com contrato/SLA próprio; são insumo interno de integration_purchase_journey. Padrão aplicado na dúvida: só expor como produto quando houver evidência real de consumo externo; promover depois se aparecer.

---

## Tabela Técnica

| Subdomínio | Produto | Camada | Tabela Física | Camada Medalhão | Papel | Pipeline | Frequência | Lineage |
|------------|---------|--------|----------------|-----------------|-------|----------|-----------|---------|
| Compras / Autorização | core_credit_purchase | Core | `bronze.purchases__credit_approved` | Bronze | Tópico raw (staging) | Streaming ingestion (platform) | Streaming contínuo | Fonte: rail de crédito, tópico approved |
| Compras / Autorização | core_credit_purchase | Core | `bronze.purchases__credit_denied` | Bronze | Tópico raw (staging) | Streaming ingestion (platform) | Streaming contínuo | Fonte: rail de crédito, tópico denied |
| Compras / Autorização | core_credit_purchase | Core | `bronze.purchases__credit_cancelled` | Bronze | Tópico raw (staging) | Streaming ingestion (platform) | Streaming contínuo | Fonte: rail de crédito, tópico cancelled |
| Compras / Autorização | core_credit_purchase | Core | `bronze.purchases__credit_clearing` | Bronze | Tópico raw (staging) | Streaming ingestion (platform) | Streaming contínuo | Fonte: rail de crédito, tópico clearing |
| Compras / Autorização | core_credit_purchase | Core | `bronze.purchases__credit_processed` | Bronze | Tópico raw (staging) | Streaming ingestion (platform) | Streaming contínuo | Fonte: rail de crédito, tópico processed |
| Compras / Autorização | core_credit_purchase | Core | `silver_l1.purchases__credit_purchase` | Silver L1 | Histórico de eventos de status (append-only, N linhas por compra) | pipeline_core_purchases_credit_purchase | Incremental: aprovação em minutos, status final (processed) em D+1 | bronze.purchases__credit_approved, bronze.purchases__credit_denied, bronze.purchases__credit_cancelled, bronze.purchases__credit_clearing, bronze.purchases__credit_processed |
| Compras / Autorização | core_credit_purchase | Core | `silver_l2.purchases__credit_purchase` | Silver L2 | Interface exposta do produto — estado atual via regra de precedência de status (regra de negócio, não dedup técnico) — 1 linha por compra | pipeline_core_purchases_credit_purchase | Incremental: aprovação em minutos, status final (processed) em D+1 | silver_l1.purchases__credit_purchase |
| Compras / Autorização | core_debit_purchase | Core | `bronze.purchases__debit_approved` | Bronze | Tópico raw (staging) | Streaming ingestion (platform) | Streaming contínuo | Fonte: rail de débito, tópico approved |
| Compras / Autorização | core_debit_purchase | Core | `bronze.purchases__debit_denied` | Bronze | Tópico raw (staging) | Streaming ingestion (platform) | Streaming contínuo | Fonte: rail de débito, tópico denied |
| Compras / Autorização | core_debit_purchase | Core | `bronze.purchases__debit_cancelled` | Bronze | Tópico raw (staging) | Streaming ingestion (platform) | Streaming contínuo | Fonte: rail de débito, tópico cancelled |
| Compras / Autorização | core_debit_purchase | Core | `bronze.purchases__debit_clearing` | Bronze | Tópico raw (staging) | Streaming ingestion (platform) | Streaming contínuo | Fonte: rail de débito, tópico clearing |
| Compras / Autorização | core_debit_purchase | Core | `bronze.purchases__debit_processed` | Bronze | Tópico raw (staging) | Streaming ingestion (platform) | Streaming contínuo | Fonte: rail de débito, tópico processed |
| Compras / Autorização | core_debit_purchase | Core | `silver_l1.purchases__debit_purchase` | Silver L1 | Histórico de eventos de status (append-only, N linhas por compra) | pipeline_core_purchases_debit_purchase | Incremental: aprovação em minutos, status final (processed) em D+1 | bronze.purchases__debit_approved, bronze.purchases__debit_denied, bronze.purchases__debit_cancelled, bronze.purchases__debit_clearing, bronze.purchases__debit_processed |
| Compras / Autorização | core_debit_purchase | Core | `silver_l2.purchases__debit_purchase` | Silver L2 | Interface exposta do produto — estado atual via regra de precedência de status (regra de negócio, não dedup técnico) — 1 linha por compra | pipeline_core_purchases_debit_purchase | Incremental: aprovação em minutos, status final (processed) em D+1 | silver_l1.purchases__debit_purchase |
| Compras / Autorização | core_credit_transaction | Core | `bronze.purchases__credit_transaction` | Bronze | Tópico raw (staging) | Streaming ingestion (platform) | Streaming contínuo | Fonte: rail de crédito, tópico único 'transaction' (compra + parcelas) |
| Compras / Autorização | core_credit_transaction | Core | `silver.purchases__credit_transaction` | Silver | Insumo interno de integration_purchase_journey (não é produto catalogado) | pipeline_integration_purchase_journey | Incremental, mesma cadência da fonte | bronze.purchases__credit_transaction |
| Compras / Autorização | core_credit_transaction_type | Core | `bronze.purchases__credit_transaction_type` | Bronze | Tópico raw (staging) — dimensão | Streaming ingestion (platform) | Baixa frequência (dimensão muda pouco) | Fonte: rail de crédito, tópico 'transaction_type' |
| Compras / Autorização | core_credit_transaction_type | Core | `silver.purchases__credit_transaction_type` | Silver | Insumo interno de integration_purchase_journey (não é produto catalogado) | pipeline_integration_purchase_journey | Batch diário (dimensão de baixa mudança) | bronze.purchases__credit_transaction_type |
| Compras / Autorização | integration_purchase_journey | Integration | `gold.integration__purchase_journey` | Gold | Interface exposta do produto — grão de compra, com parcelas relacionadas quando existirem | pipeline_integration_purchase_journey | Herda o SLA incremental dos Core: parcial em minutos, completo em D+1 | silver_l2.purchases__credit_purchase, silver_l2.purchases__debit_purchase, silver.purchases__credit_transaction, silver.purchases__credit_transaction_type |
| Compras / Autorização | analytics_extrato_cliente | Analytics | `gold.analytics__extrato_cliente` | Gold | Interface exposta do produto | pipeline_analytics_extrato_cliente | Incremental, mesma cadência de integration_purchase_journey (completude legal) | gold.integration__purchase_journey |
| Compras / Autorização | analytics_comportamento_gasto | Analytics | `gold.analytics__comportamento_gasto` | Gold | Interface exposta do produto | pipeline_analytics_comportamento_gasto | Batch diário | gold.integration__purchase_journey |
| Compras / Autorização | analytics_taxa_aprovacao_compra | Analytics | `gold.analytics__taxa_aprovacao_compra` | Gold | Interface exposta do produto | pipeline_analytics_taxa_aprovacao_compra | Batch diário | silver_l2.purchases__credit_purchase, silver_l2.purchases__debit_purchase |
| Compras / Autorização | analytics_motivos_negacao_compra | Analytics | `gold.analytics__motivos_negacao_compra` | Gold | Interface exposta do produto | pipeline_analytics_motivos_negacao_compra | Batch diário | silver_l2.purchases__credit_purchase, silver_l2.purchases__debit_purchase |
| Compras / Autorização | analytics_ranking_lojista_categoria | Analytics | `gold.analytics__ranking_lojista_categoria` | Gold | Interface exposta do produto | pipeline_analytics_ranking_lojista_categoria | Batch diário/semanal | gold.integration__purchase_journey |
| Compras / Autorização | analytics_adocao_parcelamento | Analytics | `gold.analytics__adocao_parcelamento` | Gold | Interface exposta do produto — ATENÇÃO: consome core_credit_transaction diretamente, hoje marcado como insumo interno (não produto). Este é exatamente o tipo de consumidor externo real que justificaria promovê-lo a produto Core próprio, com contrato e dono formal. | pipeline_analytics_adocao_parcelamento | Batch diário | silver.purchases__credit_transaction, gold.integration__purchase_journey |
| Compras / Autorização | analytics_latencia_liquidacao_compra | Analytics | `gold.analytics__latencia_liquidacao_compra` | Gold | Interface exposta do produto — consome L1 (histórico de eventos), não L2, porque precisa de múltiplos timestamps por compra (approved_at, clearing_at, processed_at) para calcular a latência entre estágios | pipeline_analytics_latencia_liquidacao_compra | Batch diário | silver_l1.purchases__credit_purchase, silver_l1.purchases__debit_purchase |
| Compras / Autorização | analytics_mix_canal | Analytics | `gold.analytics__mix_canal` | Gold | Interface exposta do produto | pipeline_analytics_mix_canal | Batch diário | gold.integration__purchase_journey |
| Compras / Autorização | analytics_gasto_internacional | Analytics | `gold.analytics__gasto_internacional` | Gold | Interface exposta do produto — PENDÊNCIA: taxa de câmbio provavelmente vem de uma fonte de Tesouraria ainda não mapeada | pipeline_analytics_gasto_internacional | Batch diário | gold.integration__purchase_journey |
| Compras / Autorização | analytics_gasto_elegivel_rewards | Analytics | `gold.analytics__gasto_elegivel_rewards` | Gold | Interface exposta do produto — PENDÊNCIA: regra de elegibilidade depende do subdomínio Benefícios/Rewards, ainda não mapeado | pipeline_analytics_gasto_elegivel_rewards | Batch diário | gold.integration__purchase_journey |
