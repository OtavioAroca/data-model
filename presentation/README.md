# Mapa do Parque de Dados

## Abertura

**Arquivo gerado:** `parque-de-dados.html`

Abra `parque-de-dados.html` direto no navegador (duplo-clique ou arraste para o
navegador). Funciona 100% offline via `file://` — não precisa de servidor.

## Conteúdo

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
- Busca por nome de tabela, três filtros suspensos (multi-seleção, todos
  marcados por padrão) — **Camadas**, **Produto de dados** e
  **Core/Integration/Analytics** — e toggle por tipo de seta e liga/desliga da
  animação, tudo na barra de ferramentas.

## Como Regenerar

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

## Tecnologia

- **Arquivo único, zero CDN** — CSS/JS inline em `parque-de-dados.html`.
  Offline, abre direto via `file://`.
- **Dados embutidos** — JSON injetado como `const DATA = {...}`.
- **Sem frameworks** — SVG + JS vanilla; pan & zoom, animação de lineage
  (`stroke-dashoffset` + `<animateMotion>`) e layout implementados à mão.
- Ferramenta independente da apresentação anterior deste repositório — ver
  [`docs/adr/0002`](../docs/adr/0002-ferramenta-nova-independente-da-apresentacao-anterior.md).

## Verificação

1. Abra `presentation/parque-de-dados.html` no navegador.
2. Clique em algumas tabelas, confira colunas/tipos, confira que as setas
   azuis animam.
3. Teste busca e os filtros suspensos (Camadas, Produto de dados,
   Core/Integration/Analytics) e o toggle por tipo de seta.
4. Console do navegador (`F12`) sem erros de JS.
