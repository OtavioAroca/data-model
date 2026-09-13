# 0009 — Grid de subdomínios por camada de produto, página única, sem emojis

## Status

Aceito — supersede parcialmente [0008](./0008-apresentacao-executiva-como-ferramenta-separada.md)
(a forma como o grid de subdomínios e a navegação da apresentação executiva
foram implementados)

## Contexto

Depois da aceitação da PR #9 (que implementou o [ADR 0008](./0008-apresentacao-executiva-como-ferramenta-separada.md)),
o usuário revisou a apresentação executiva gerada e pediu três ajustes:

1. O grid "Os 15 Subdomínios" (aba/seção Forma de Modelar) mostrava tags
   `Core`/`Support`/`Generic` — a classificação **DDD** de importância
   estratégica de cada subdomínio ([`kb/ddd.md`](../../kb/ddd.md)). O usuário
   apontou que a apresentação precisa mostrar os nomes acordados **Core,
   Integration e Analytics** — a classificação de **produto de dados** por
   escopo ([`kb/core-integration-analytics.md`](../../kb/core-integration-analytics.md)).
   Mostrar `Support`/`Generic` ali arrisca confundir os dois eixos, já que
   ambos reaproveitam a palavra "Core" com significados diferentes — o
   próprio callout de desambiguação da seção existe para alertar sobre essa
   confusão, e o grid estava reproduzindo-a visualmente.
2. A navegação por abas (mostra/esconde seção via JS) deveria virar uma
   página única, com rolagem contínua.
3. Remover emojis do conteúdo (título, callout, ícones dos cards de
   benefício) para um tom mais profissional.

## Decisão

- O grid de subdomínios agora mostra, por subdomínio, as camadas de produto
  (`Core`/`Integration`/`Analytics`) que já têm pelo menos um produto
  proposto em `catalog/<slug>/catalog.yaml` — não mais o `tipo_ddd` de
  `catalog/index.yaml`. O filtro acima do grid muda de
  `Todos/Core/Support/Generic` para `Todos/Core/Integration/Analytics`.
  `scripts/build_apresentacao_executiva.py` passa a ler, para cada um dos 15
  subdomínios, `catalog/<slug>/catalog.yaml` (camadas distintas em
  `produtos[].camada`), além de `catalog/index.yaml`.
- A classificação DDD (Core/Support/Generic) continua explicada em texto no
  card conceitual "Domain-Driven Design (DDD)" e na tabela de desambiguação
  — só deixou de aparecer como tag/filtro no grid, para não colidir
  visualmente com Core/Integration/Analytics.
- `presentation/apresentacao-executiva.template.html` deixa de usar
  `nav.tabs` com JS de mostra/esconde por seção. As três seções (Forma de
  Modelar, Benefícios, Estudo de Caso) ficam sempre visíveis, empilhadas
  verticalmente em uma página única; a barra no topo vira navegação por
  âncora (rolagem suave + destaque da seção ativa via `IntersectionObserver`
  quando ela entra na viewport), em vez de abas.
- Emojis removidos do conteúdo da apresentação (título, callout de
  desambiguação, ícones dos cards de Benefícios). Setas (`→`) são mantidas —
  não são emoji, e já são convenção do repositório para notação de pipeline
  (ex: [`kb/camada-medalhao.md`](../../kb/camada-medalhao.md)).

## Consequências

- Se no futuro alguém quiser voltar a mostrar a classificação DDD no grid
  (Core/Support/Generic), precisa de um design que deixe claro que é um eixo
  diferente do Core/Integration/Analytics já usado como tag principal — não
  é só adicionar de volta a tag antiga lendo `tipo_ddd`.
- 4 dos 15 subdomínios (Benefícios/Rewards, Cartão, Encerramento, Fraude)
  ainda não têm produto Integration proposto no catálogo V0 — o filtro
  "Integration" os deixa esmaecidos; isso reflete o estado atual do
  catálogo, não uma regra do modelo.
- `scripts/build_apresentacao_executiva.py` passa a depender de
  `catalog/<slug>/catalog.yaml` existir para os 15 subdomínios (não só o
  piloto) — se um subdomínio ficar sem esse arquivo, o build falha (mesma
  checagem estrita que os demais scripts do repositório já aplicam aos
  arquivos que leem).
