# 0003 — FK e cardinalidade declaradas explicitamente no schema físico

## Status

Superseded por [0005](./0005-fk-sem-cardinalidade-explicita.md) — a parte de
`cardinalidade` foi revertida a pedido do usuário. `chave_estrangeira`
(`tabela` + `coluna`, sem cardinalidade) continua valendo.

## Contexto

O contrato `catalog/_schema/schema-fisico.schema.json` já previa um campo
opcional `chave_estrangeira` (`{tabela, coluna}`) por coluna, mas ele nunca foi
preenchido em `catalog/compras-autorizacao/schema-fisico/schema-fisico.yaml`.
As únicas relações entre tabelas hoje são inferidas heuristicamente (no antigo
`build_apresentacao.py`, já removido): colunas terminando em `_id` que
aparecem em mais de uma tabela viram uma "relação inferida" sem cardinalidade
— não dá pra saber, só olhando o nome da coluna, se é 1:1, 1:N ou N:N, nem se
as duas tabelas realmente têm uma relação de negócio ou só coincidência de
nome.

Como o pedido explícito era desenhar setas com cardinalidade (1:1, 1:N) no
mapa, uma heurística por nome de coluna não é confiável o suficiente.

## Decisão

Estender o contrato para exigir `cardinalidade` (`1:1` ou `1:N`) dentro de
`chave_estrangeira` sempre que ela for declarada, e preencher
`chave_estrangeira` manualmente nas 29 tabelas de Compras/Autorização —
trabalho de modelagem real, não geração automática — distinguindo:

- **Relação estrutural (FK de verdade)**: uma coluna cujo valor deve existir
  como chave primária de outra tabela, independente do estágio do pipeline
  (ex: `transaction_type_id` → tabela de tipos; `purchase_id` em uma tabela de
  parcelas → tabela de compra). Isso vira `chave_estrangeira` +
  `cardinalidade`.
- **Lineage/pipeline (Bronze→Silver→Gold)**: já coberto pelo campo `lineage:`
  em `mapeamento-tecnico.yaml` — não é uma FK relacional, é proveniência de
  dado. Continua representado só como lineage, sem duplicar como FK.
- **Referência externa não resolvida**: colunas como `customer_id`, `card_id`,
  `merchant_id` apontam para entidades donas de outros subdomínios (Conta
  Cartão, Cartão) que não têm schema físico neste repositório — não viram
  `chave_estrangeira` (não há tabela para apontar), ficam listadas à parte
  para o mapa desenhar como referência externa.
- **Tabelas de agregação Gold** (rollups como `analytics__comportamento_gasto`,
  `analytics__mix_canal` etc.) não referenciam uma linha específica de outra
  tabela — não recebem `chave_estrangeira`, só lineage.

`N:N` fica fora do enum de `cardinalidade` por enquanto: não há evidência de
tabela associativa no piloto. Se aparecer, o padrão é modelar como duas FKs
1:N a partir da tabela de junção, não como uma cardinalidade N:N direta.

## Consequências

- As setas de relação no mapa mostram cardinalidade real, validada por quem
  modelou o schema — não uma suposição de nome de coluna.
- `scripts/validate_catalog.py` passa a checar que toda `chave_estrangeira`
  aponta para uma tabela/coluna que existe de fato, e que a cardinalidade é
  coerente com a coluna referenciada ser chave primária no lado apontado.
- Isso é trabalho manual que precisa ser revisitado sempre que uma tabela nova
  entrar no schema físico — não é gerado automaticamente a partir do nome das
  colunas.
