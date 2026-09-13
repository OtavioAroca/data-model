# Camada Medalhão — Bronze / Silver / Gold

## Visão geral

A **camada medalhão** classifica tabelas físicas em um data lake pelo estágio de processamento e qualidade dos dados:

- **Bronze**: dados brutos, logo após ingestão (staging/raw).
- **Silver**: dados limpos, conformados, com qualidade garantida.
- **Gold**: dados prontos para consumo, já agregados e/ou otimizados para casos de uso específicos.

Cada camada tem um custo/benefício diferente: Bronze é barato de escrever (imutável, append-only) mas caro de ler sem reprocessamento; Gold é caro de atualizar mas muito rápido de consultar.

---

## Bronze

Dados imediatos após ingestão de um sistema de origem ou streaming.

- **Nenhum** processamento — preserva layout nativo da fonte.
- **Imutável** — só append (histórico completo de eventos).
- **Barato** de escrever, **caro** de reprocessar em toda leitura.

### Exemplo

No Mapeamento Técnico do piloto (subdomínio Compras / Autorização):

```
bronze.purchases__credit_approved     ← Tópico "approved" do rail de crédito
bronze.purchases__credit_denied       ← Tópico "denied" do rail de crédito
bronze.purchases__credit_cancelled    ← Tópico "cancelled" do rail de crédito
bronze.purchases__credit_clearing     ← Tópico "clearing" do rail de crédito
bronze.purchases__credit_processed    ← Tópico "processed" do rail de crédito
```

Cada tabela é um tópico Kafka/streaming que chega bruto do sistema de autorização de crédito.

---

## Silver

Dados limpos, padronizados, com garantias de qualidade e completude.

- **Processado** — aplicada transformação de negócio.
- **Mutável** — permite atualizações, correções retroativas.
- **Uma camada Silver pode conter dois sub-padrões**: **L1** (append-only histórico de eventos) e **L2** (estado atual materializado).

### Silver L1 — Histórico de eventos

Histórico **completo e imutável** de todos os eventos/mudanças de estado de um objeto de negócio.

Cada objeto (ex: uma compra) pode ter **N linhas** — uma por cada evento ou status anterior.

**Por quê L1 existe:**
- Auditoria e investigação exigem histórico completo.
- Risco e fraude às vezes precisam saber a sequência de eventos (ex: "esta compra foi initially denied, depois approved?").

**No piloto:**
```
silver_l1.purchases__credit_purchase  ← Histórico de eventos: cada compra tem N linhas (1 por status: approved, cleared, processed, etc)
silver_l1.purchases__debit_purchase   ← Mesmo para débito
```

### Silver L2 — Estado atual materializado

Estado **atual** de cada objeto, calculado via uma regra de negócio que define a precedência entre status.

Cada objeto tem **exatamente 1 linha**.

**Por quê L2 existe:**
- A maioria das consultas quer só saber "qual é o status atual desta compra?" — não o histórico.
- Se essa lógica fosse recalculada a cada leitura em cima dos N eventos de L1, custaria caro em CPU e criaria risco de times implementarem a regra de forma diferente (divergência de métricas).
- Materializar uma única vez em L2 economiza custo de leitura e garante consistência.

**A regra de precedência é de NEGÓCIO, não técnica**: ex: "um status `cancelled` deve prevalecer sobre `clearing` mesmo que chegue depois no tempo?". Isso define o dono do subdomínio, não o engenheiro de dados.

**No piloto:**
```
silver_l2.purchases__credit_purchase  ← 1 linha por compra, com status final definido pela regra de precedência
silver_l2.purchases__debit_purchase   ← Mesmo para débito
```

### Ponto de compreensão

L1 e L2 **não são redundância** — são dois públicos diferentes:

- L1 para auditoria/investigação (consulta rara, aceita custo computacional).
- L2 para o caso comum (operação em minutos, rápido).

O time de Integration que monta o `integration_purchase_journey` lê de **L2** (estado final), não L1. O time de Analytics que precisa calcular latência entre eventos (`analytics_latencia_liquidacao_compra`) lê de **L1** (múltiplos timestamps).

---

## Gold

Dados prontos para consumo, agregados e/ou otimizados para um caso de uso específico.

- **Altamente processado** — aplicadas todas as transformações de negócio, agregações, enriquecimentos.
- **Mutável** — atualizações/correções são frequentes.
- **Caro** de atualizar, mas muito **rápido** de consultar.

### Exemplo

No piloto:

```
gold.integration__purchase_journey
```

Cruza `silver_l2.purchases__credit_purchase`, `silver_l2.purchases__debit_purchase`, `silver.purchases__credit_transaction` e `silver.purchases__credit_transaction_type` em uma única tabela — grão de compra, com parcelas relacionadas quando existirem — pronta para consumo por Risco, Fraude, Atendimento.

Outputs de Analytics também são Gold:
```
gold.analytics__extrato_cliente           ← Legalmente completo e ordenado
gold.analytics__comportamento_gasto       ← Agregado por cliente, categoria, ticket médio
gold.analytics__taxa_aprovacao_compra     ← Taxa de aprovação/negação por segmento
```

---

## Frequência de atualização

- **Bronze**: Streaming contínuo (em minutos ou segundos).
- **Silver L1**: Incremental na mesma cadência do Bronze (em minutos ou segundos).
- **Silver L2**: Incremental, mas com delay aceitável (ex: aprovação em minutos, status final em D+1).
- **Gold**: Batch diário ou mais frequente, dependendo do caso de uso (ex: Analytics é batch diário; Integration herda o SLA do Silver que alimenta).

---

## Nota: não confundir com Core / Integration / Analytics (produto de dados)

A camada medalhão (Bronze/Silver/Gold) classifica **tabelas físicas** por processamento.

A camada de produto de dados (Core/Integration/Analytics) classifica **produtos de dados** por escopo de negócio.

Uma mesma tabela física pode conter um ou mais produtos:
- `silver_l2.purchases__credit_purchase` = uma tabela Silver L2 que é o produto `core_credit_purchase`.
- `gold.integration__purchase_journey` = uma tabela Gold que é o produto `integration_purchase_journey`.

Ver [core-integration-analytics.md](./core-integration-analytics.md) para a distinção completa.
