# 0004 — Duas categorias de seta no mapa: pipeline (animada) vs relacional (estática)

## Status

Aceito

## Contexto

O pedido tinha duas exigências que não são a mesma coisa: (1) setas indicando
cardinalidade de relação entre tabelas (1:1, 1:N) e (2) setas animadas
simulando dado trafegando no pipeline. Tentar desenhar as duas coisas com o
mesmo tipo de seta confundiria dois conceitos diferentes do próprio domínio
(ver `kb/camada-medalhao.md`):

- **Lineage** (proveniência): de onde uma tabela Silver/Gold busca seus dados
  — direção sempre Bronze → Silver → Gold, é o "cano" do pipeline.
- **Relação estrutural** (FK): como duas tabelas se referenciam por chave —
  pode existir dentro da mesma camada (ex: `transaction` → `transaction_type`,
  ambos Bronze) e não tem direção de "fluxo", tem cardinalidade.

## Decisão

O mapa desenha duas categorias de seta visualmente distintas e com toggle
independente:

1. **Pipeline/lineage** — seta grossa, colorida pela transição de camada
   medalhão de origem→destino, com animação de fluxo (dash-offset ou ponto
   viajando ao longo do path) tocando continuamente enquanto o mapa estiver
   aberto. Fonte de dado: `lineage:` em `mapeamento-tecnico.yaml`.
2. **Relacional** — linha fina tracejada, estática (sem animação), com rótulo
   `1:1` ou `1:N` em cada ponta. Fonte de dado: `chave_estrangeira` +
   `cardinalidade` em `schema-fisico.yaml` (ver ADR 0003).

## Consequências

- Quem olha o mapa consegue distinguir "de onde este dado veio no pipeline" de
  "como esta tabela se relaciona com aquela outra" sem precisar ler texto.
- Custo: mais um controle de UI (toggle por categoria de seta) e mais uma
  camada de estilo/animação SVG para manter.
- Uma tabela pode ter os dois tipos de seta ao mesmo tempo (ex:
  `silver.purchases__credit_transaction` recebe lineage de uma tabela Bronze e
  tem uma FK relacional para `transaction_type`) — o layout precisa acomodar
  isso sem sobrepor as duas.
