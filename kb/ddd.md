# DDD — Domain-Driven Design (essencial)

## Bounded Context

Um **bounded context** é um domínio claro e bem delimitado do negócio, com sua própria linguagem, regras e modelos de dados.

No domínio Cartão, cada linha da aba "Subdomínios" é um bounded context — por exemplo:

- **Compras / Autorização**: "Autoriza e captura as transações realizadas com o cartão, incluindo o plano de parcelamento decidido no ato da compra". Tem seus próprios sistemas de origem (Switch de autorização, rede/bandeira), seus próprios conceitos (status: approved, denied, cancelled, clearing, processed) e alimenta seus próprios produtos de dados.

Cada bounded context pode ter um dono técnico, definir sua própria linguagem ubíqua (ver próxima seção) e evoluir de forma independente dos outros.

### Por que isso importa pra engenharia de dados

Bounded context não é só um agrupamento conceitual — na prática, ele tende a ser a **fronteira de ownership de pipeline**. Cada bounded context normalmente tem seu próprio sistema de origem, seu próprio time responsável, e alimenta seu próprio [produto de dados](./produto-de-dados.md) Core (ex: o bounded context "Compras / Autorização" alimenta `core_credit_purchase` e `core_debit_purchase`).

Isso importa na hora de desenhar pipeline: um produto Core não deveria misturar dados de dois bounded contexts diferentes (isso já seria um produto Integration — ver [core-integration-analytics.md](./core-integration-analytics.md)), e uma mudança de schema dentro de um bounded context é decisão do dono daquele contexto, não de quem consome o dado a partir de Integration ou Analytics.

---

## Subdomínio: Core / Support / Generic

Uma classificação **estratégica** de como cada bounded context importa para o negócio.

### Core

O subdomínio é um **diferencial competitivo** — a empresa quer estar melhor nele do que a concorrência. Vale investimento técnico e complexidade.

Exemplos no catálogo:
- **Elegibilidade**: decisão de crédito é o coração da estratégia bancária.
- **Fraude**: reduzir fraude é diferencial de segurança.
- **Compras / Autorização**: fluxo de transação é crítico.

### Support

O subdomínio é **necessário mas não diferencial** — tem de funcionar bem, mas não é o ponto de vantagem competitiva. Investe-se menos em customização.

Exemplos no catálogo:
- **Cobrança**: todo banco precisa cobrar, mas a abordagem é padrão.
- **Pagamento da Fatura**: infraestrutura conhecida.
- **Encerramento**: processo straightforward.

### Generic

O subdomínio é **comum a qualquer negócio** — usa-se solução off-the-shelf (ou copia-se de outros). Não vale reinventar.

Exemplos no catálogo:
- **Benefícios / Rewards**: lógica de pontos/cashback é genérica, existem soluções prontas no mercado.

---

## Linguagem Ubíqua

A **linguagem ubíqua** é o vocabulário compartilhado entre time técnico, time de negócio e stakeholders — sem tradução, sem ambiguidade, sem sinônimos.

No catálogo, a linguagem ubíqua aparece nos nomes dos produtos de dados:

- `purchase` (não `transaction` ou `order`): o termo exato que o negócio usa para "compra feita com o cartão".
- `statement` (não `invoice` ou `billing`): o termo exato para "fatura periódica".
- `dispute` (não `chargeback` ou `claim`): contestação de transação.
- `collection` (não `recovery` ou `arrear`): cobrança de atrasos.

Por que isso importa? Porque quando um analista de risco fala em "temos alta taxa de disputes", o time técnico sabe exatamente qual tabela abrir (ex: `analytics_dispute_rate` no ouro) sem interpretar ou perguntar "você quer dizer chargeback?".

Na prática, o catálogo do domínio Cartão **preserva a linguagem ubíqua em português** em nomes de produtos (`analytics_extrato_cliente`, `analytics_comportamento_gasto`), mas usa **inglês em produtos Core e Integration** porque o público desses produtos é engenharia (mais técnico e com convenção de inglês). Analytics fica em português porque seus consumidores finais (risco, marketing, financeiro) são menos técnicos.

---

## Nota: não confundir com Core (produto de dados)

A classificação DDD de "**Core** subdomínio" é diferente da classificação de "**Core** produto de dados".

- **Core (DDD)** = subdomínio com importância estratégica elevada para o negócio.
- **Core (produto de dados)** = produto que representa exatamente um bounded context, sem cruzamento com outros.

Um subdomínio Support (ex: Cobrança) pode gerar produtos Core de dados (`core_collections_status`), e um subdomínio Core (ex: Compras / Autorização) gera produtos em todas as camadas (Core, Integration, Analytics).

Ver [core-integration-analytics.md](./core-integration-analytics.md) para a distinção completa.
