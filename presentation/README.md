# Presentation

Duas ferramentas independentes, ambas página única HTML/CSS/JS offline (zero
build, zero CDN, zero servidor):

- [**Apresentação Executiva**](#apresentação-executiva) — forma de modelar,
  benefícios e estudo de caso, para stakeholders.
- [**Mapa do Parque de Dados**](#mapa-do-parque-de-dados) — diagrama
  interativo das tabelas físicas do piloto (Compras/Autorização).

A apresentação executiva linka o mapa (botão "Abrir mapa interativo" na aba
Estudo de Caso) em vez de reimplementar o diagrama — ver
[`docs/adr/0008`](../docs/adr/0008-apresentacao-executiva-como-ferramenta-separada.md).

---

## Apresentação Executiva

**Arquivo gerado:** `apresentacao-executiva.html`

Abra `apresentacao-executiva.html` direto no navegador (duplo-clique ou
arraste para o navegador). Funciona 100% offline via `file://`.

### Conteúdo

Página única (rolagem contínua, sem abas), com navegação por âncora entre
três seções:

- **Forma de Modelar** — os três eixos de classificação (DDD, Camada
  Medalhão, Core/Integration/Analytics), a desambiguação "Core tem 3
  significados", e o grid dos 15 subdomínios do domínio Cartão (com filtro
  Core/Integration/Analytics — quais camadas de produto já têm produto
  proposto no catálogo) — dados lidos de `catalog/index.yaml` e de cada
  `catalog/<slug>/catalog.yaml`.
- **Benefícios** — por que modelar dessa forma (Silver L1 vs L2, Integration,
  Analytics em português, alinhamento com bounded contexts, escalabilidade).
- **Estudo de Caso** — narrativa do piloto Compras/Autorização (pipeline
  Bronze→Silver L1/L2→Gold, contagem real de tabelas físicas por camada, os
  13 produtos de dados propostos com descrição, ressalvas registradas nos
  ADRs) com link para o mapa interativo — produtos e contagens lidos de
  `catalog/compras-autorizacao/catalog.yaml` e `mapeamento-tecnico.yaml`, não
  hardcoded no template.

### Como Regenerar

Se `catalog/index.yaml`, algum `catalog/<slug>/catalog.yaml` ou
`catalog/compras-autorizacao/mapeamento-tecnico.yaml` for editado, regenere
com:

```bash
python3 scripts/build_apresentacao_executiva.py
```

O script lê `catalog/index.yaml` (dados dos subdomínios), para cada um
`catalog/<slug>/catalog.yaml` (camadas Core/Integration/Analytics já
propostas) e, para o estudo de caso, `catalog/compras-autorizacao/catalog.yaml`
(lista completa de produtos) e `mapeamento-tecnico.yaml` (contagem de
tabelas físicas por camada medalhão) — injetando tudo em
`apresentacao-executiva.template.html` e escrevendo
`apresentacao-executiva.html`. O restante do conteúdo (conceitos,
benefícios, texto introdutório do estudo de caso) é texto estático no
template — editar o `.template.html` diretamente e regerar.

### Verificação

1. Abra `presentation/apresentacao-executiva.html` no navegador.
2. Clique nos links de navegação (Forma de Modelar / Benefícios / Estudo de
   Caso) e confirme que a página rola até a seção correspondente, com o link
   ativo destacado.
3. Teste o filtro Core/Integration/Analytics no grid de subdomínios.
4. Clique em "Abrir mapa interativo" e confirme que `parque-de-dados.html`
   abre em nova aba.
5. Console do navegador (`F12`) sem erros de JS.

---

## Mapa do Parque de Dados

### Abertura

**Arquivo gerado:** `parque-de-dados.html`

Abra `parque-de-dados.html` direto no navegador (duplo-clique ou arraste para o
navegador). Funciona 100% offline via `file://` — não precisa de servidor.

### Conteúdo

As 29 tabelas físicas de Compras/Autorização (único subdomínio com schema
físico definido — ver
[`docs/adr/0001`](../docs/adr/0001-escopo-detalhado-so-compras-autorizacao.md)
e [`docs/adr/0006`](../docs/adr/0006-mapa-sem-outros-subdominios-e-sem-chips-externos.md)),
organizadas em colunas por camada medalhão (Bronze / Silver L1 / Silver L2 /
Silver / Gold):

- Clique em uma tabela para ver colunas, tipos, nullability, chave primária,
  lineage (de onde vem / para onde vai) e relações.
- **Setas azuis animadas** = lineage/pipeline (Bronze→Silver→Gold), com um
  ponto viajando ao longo da seta simulando o dado trafegando.
- **Setas roxas tracejadas** = relação estrutural (chave estrangeira) — sem
  indicação de cardinalidade (ver [`docs/adr/0005`](../docs/adr/0005-fk-sem-cardinalidade-explicita.md)).
- **Cartões pontilhados** ("externo — outro subdomínio") = tabelas citadas
  como fonte de lineage mas pertencentes a outro subdomínio, ainda sem schema
  físico neste catálogo.
- Busca por nome de tabela e três filtros suspensos (multi-seleção, todos
  marcados por padrão) — **Camadas**, **Produto de dados** e
  **Core/Integration/Analytics** — na barra de ferramentas. Setas de lineage
  e relacional, e a animação de fluxo, ficam sempre visíveis/ativas (sem
  toggle).

### Como Regenerar

Se os YAMLs de catálogo forem editados, regenere com:

```bash
python3 scripts/build_mapa_parque_dados.py
```

O script:
- Lê `catalog/index.yaml` e identifica quais subdomínios já têm
  `schema-fisico/schema-fisico.yaml` (hoje só `compras-autorizacao`).
- Monta tabelas + colunas (`schema-fisico.yaml`) + lineage
  (`mapeamento-tecnico.yaml`) + relações estruturais (`chave_estrangeira` em
  `schema-fisico.yaml`).
- Injeta tudo em `parque-de-dados.template.html` e escreve `parque-de-dados.html`.

Saída inclui um resumo de contagens para verificação rápida (tabelas,
relações, arestas de lineage, tabelas externas).

### Tecnologia

- **Arquivo único, zero CDN** — CSS/JS inline em `parque-de-dados.html`.
  Offline, abre direto via `file://`.
- **Dados embutidos** — JSON injetado como `const DATA = {...}`.
- **Sem frameworks** — SVG + JS vanilla; pan & zoom, animação de lineage
  (`stroke-dashoffset` + `<animateMotion>`) e layout implementados à mão.
- Ferramenta independente da apresentação anterior deste repositório — ver
  [`docs/adr/0002`](../docs/adr/0002-ferramenta-nova-independente-da-apresentacao-anterior.md).

### Verificação

1. Abra `presentation/parque-de-dados.html` no navegador.
2. Clique em algumas tabelas, confira colunas/tipos, confira que as setas
   azuis animam.
3. Teste busca e os filtros suspensos (Camadas, Produto de dados,
   Core/Integration/Analytics).
4. Console do navegador (`F12`) sem erros de JS.
