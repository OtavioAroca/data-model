# 0006 — Mapa cobre só a rede de tabelas de Compras/Autorização, sem cartões de outros subdomínios e sem chips de referência externa

## Status

Aceito — supersede parcialmente [0001](./0001-escopo-detalhado-so-compras-autorizacao.md)
(a parte "os outros 14 subdomínios aparecem em uma seção separada")

## Contexto

A primeira versão do mapa (`presentation/parque-de-dados.html`) tinha duas
partes além da rede de tabelas de Compras/Autorização:

1. Uma aba "Outros subdomínios", com cartões de produto proposto
   (Core/Integration/Analytics) para os 14 subdomínios sem schema físico —
   decisão original de [0001](./0001-escopo-detalhado-so-compras-autorizacao.md).
2. Chips na base do canvas ("Cliente — externo", "Cartão — externo", "Lojista
   — externo") para as colunas `customer_id`/`card_id`/`merchant_id`, que
   referenciam entidades de outros subdomínios sem schema físico neste
   catálogo.

Depois de ver o mapa gerado, o usuário pediu para remover as duas coisas.

## Decisão

- Remover a aba/página "Outros subdomínios" e as abas de navegação do mapa —
  `presentation/parque-de-dados.html` volta a ser uma página única (só o mapa
  de Compras/Autorização), sem `nav.tabs`.
- Remover os chips de referência externa (`customer_id`/`card_id`/
  `merchant_id`) e a lógica que os desenha
  (`REFERENCIAS_EXTERNAS_CONHECIDAS`/`referencias_externas` em
  `scripts/build_mapa_parque_dados.py`, `renderExternalChips` no template).
- **Mantido**: o cartão tracejado "externo — outro subdomínio" dentro do
  próprio grafo (ex: `disputes__chargeback`) — isso representa uma tabela
  física real, citada como fonte de lineage, e não a mesma coisa que os chips
  removidos (que eram sobre colunas de referência, não tabelas).
- **Mantido**: o restante da decisão de [0001](./0001-escopo-detalhado-so-compras-autorizacao.md)
  — o mapa detalhado continua cobrindo só Compras/Autorização, único
  subdomínio com schema físico.

## Consequências

- `scripts/build_mapa_parque_dados.py` não lê mais `catalog/<slug>/catalog.yaml`
  dos subdomínios sem schema físico — só usa `index.yaml` para descobrir quais
  subdomínios têm `schema-fisico.yaml`.
- Os 14 subdomínios sem schema físico deixam de ter qualquer representação
  nesta ferramenta — para vê-los, o catálogo em `catalog/<slug>/catalog.md`
  continua sendo a fonte (ver `catalog/README.md`).
- Se no futuro fizer sentido voltar a mostrar os outros subdomínios ou as
  referências externas, é um novo ADR — este documenta que a remoção foi
  deliberada, não um esquecimento.
