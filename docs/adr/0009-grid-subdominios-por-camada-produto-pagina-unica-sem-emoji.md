# 0009 — Grid de subdomínios por camada de produto, página única, sem emojis, estudo de caso completo

## Status

Proposto

> Ajustes pedidos pelo usuário depois de revisar a apresentação executiva
> gerada pela PR #9 — ainda em rodada de revisão, atualizado neste mesmo
> arquivo até ser aceito (mesmo padrão do [ADR 0008](./0008-apresentacao-executiva-como-ferramenta-separada.md)
> antes de virar `Aceito`).

## Contexto

Depois da aceitação da PR #9 (que implementou o [ADR 0008](./0008-apresentacao-executiva-como-ferramenta-separada.md)),
o usuário revisou a apresentação executiva gerada e pediu quatro ajustes:

1. O grid "Os 15 Subdomínios" (seção Forma de Modelar) mostrava tags
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
4. A seção Estudo de Caso estava incompleta: o diagrama de pipeline mostrava
   só 4 das 29 tabelas físicas do piloto (só o rail de crédito), e a lista de
   "Produtos de dados propostos" citava só 3 dos 13 produtos do catálogo,
   resumindo o resto como "e outros". O usuário sinalizou que faltavam
   tabelas.
5. Depois de uma primeira correção do ponto 4 (produtos completos + linha de
   estatísticas com a contagem real de tabelas por camada), o usuário ainda
   viu tabelas faltando — a contagem por camada não bastava, faltava o
   **nome de cada uma das 29 tabelas físicas**. Confirmado via pergunta
   direta: o pedido é listar os nomes, não expandir o diagrama nem
   reconstruir o explorador interativo.

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
- A seção Estudo de Caso passa a ser parcialmente data-driven, em vez de
  texto hardcoded: `scripts/build_apresentacao_executiva.py` lê
  `catalog/compras-autorizacao/catalog.yaml` (os 13 produtos, com descrição
  real) e `mapeamento-tecnico.yaml` (contagem de tabelas físicas por camada
  medalhão), disponibilizando `DATA.estudo_caso` no template.
  - A lista "Produtos de dados propostos" renderiza todos os 13 produtos
    (não mais 3 + "e outros"), agrupados por camada com a descrição de
    `catalog.yaml`.
  - Uma linha de estatísticas (`29 tabelas físicas · 12 Bronze · 2 Silver L1
    · 2 Silver L2 · 2 Silver · 11 Gold`) mostra a contagem real de tabelas do
    piloto, deixando explícito que o diagrama ilustrativo abaixo do texto
    (4 caixas, rail de crédito) é só um exemplo, não a lista completa.
  - O diagrama de pipeline continua mostrando só o rail de crédito como
    exemplo (não os 29 nós) — reconstruir o diagrama completo aqui
    duplicaria `presentation/parque-de-dados.html`, o que os ADRs 0002/0008
    já decidiram evitar. O texto acima do diagrama agora descreve os dois
    rails (crédito e débito) e as tabelas de parcelamento por extenso, e o
    CTA para o mapa interativo usa a contagem real de tabelas.
  - Abaixo da linha de estatísticas, uma lista textual com o **nome de cada
    uma das 29 tabelas físicas**, agrupada por camada medalhão (Bronze,
    Silver L1, Silver L2, Silver, Gold), lida de
    `mapeamento-tecnico.yaml.tabelas_fisicas` (`DATA.estudo_caso.tabelas_por_camada`,
    calculada no mesmo loop que já produzia `contagem_camada`). É uma lista
    simples (nome da tabela, sem colunas/tipos/lineage/relações) — a
    exploração desses detalhes continua só no mapa interativo, mantendo a
    decisão de não reconstruir o explorador aqui.

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
- O script também passa a depender de
  `catalog/compras-autorizacao/mapeamento-tecnico.yaml` para o estudo de
  caso — se esse arquivo mudar de forma (ex: `tabelas_fisicas` renomeado), o
  build da apresentação executiva quebra junto com o do mapa
  (`build_mapa_parque_dados.py`), que já lê o mesmo arquivo.
- A lista de nomes de tabela precisou de `min-width: 0` no item de grid
  (`.tabelas-grupo`) e `overflow-wrap: anywhere` no texto (`.tabelas-grupo
  li`) — nomes como `silver_l1.purchases__credit_purchase` não têm espaço
  (uma "palavra" só para o algoritmo de quebra de linha do navegador), e o
  comportamento padrão de `min-width: auto` em itens de CSS Grid expande a
  coluna para caber o conteúdo inteiro sem quebrar, causando sobreposição
  entre colunas vizinhas. Vale lembrar disso se outra lista de identificadores
  longos (sem espaço) for adicionada a um grid neste template no futuro.
