# 0008 — Apresentação executiva como ferramenta separada, linkando o mapa do parque de dados

## Status

Aceito

> Nasceu como `Proposto` (o primeiro ADR do repositório usado para guiar um
> desenvolvimento em andamento, atualizado neste mesmo arquivo em vez de
> gerar um novo ADR a cada revisão) e foi aceito após aprovação da
> [PR #9](https://github.com/OtavioAroca/data-model/pull/9).

## Contexto

O usuário pediu uma apresentação executiva cobrindo três coisas: (1) a forma
como o time pensa em modelar os dados do domínio Cartão, (2) os benefícios
dessa modelagem, (3) um exemplo de caso de uso — para apresentar a
stakeholders e usar como referência de desenvolvimento.

Já existiu uma apresentação com exatamente esse escopo
(`scripts/build_apresentacao.py` → `presentation/apresentacao.template.html`
→ `presentation/apresentacao.html`), apagada no commit `b9f1f00`
(`feature/rephrasing-presentation/20260913`). O
[ADR 0002](./0002-ferramenta-nova-independente-da-apresentacao-anterior.md)
documenta essa remoção: o usuário pediu uma ferramenta nova e desacoplada
para o mapa do parque de dados, e o ADR 0002 decidiu não reaproveitar nomes
nem código da apresentação apagada. A "Consequências" do ADR 0002 já
antecipava este momento:

> Se no futuro se quiser voltar a ter uma apresentação mais ampla (conceitos,
> benefícios, os 15 subdomínios lado a lado), ela pode ser uma ferramenta
> separada que eventualmente embute ou linka o mapa gerado aqui — não é papel
> deste ADR decidir isso agora.

Este ADR é essa decisão.

## Decisão

Construir `presentation/apresentacao-executiva.html`, gerada por
`scripts/build_apresentacao_executiva.py` a partir de
`presentation/apresentacao-executiva.template.html`, como ferramenta
**separada** do mapa do parque de dados (nomes próprios, script próprio —
mesmo precedente do ADR 0002), com três seções, na ordem pedida:

1. **Forma de Modelar** — os três eixos de classificação (DDD, Camada
   Medalhão, Core/Integration/Analytics), a desambiguação "Core tem 3
   significados" e o grid dos 15 subdomínios do domínio Cartão. Conteúdo
   redigido a partir de `kb/*.md`; dados do grid lidos de
   `catalog/index.yaml` (mesmo padrão de leitura de YAML usado em
   `build_mapa_parque_dados.py` — nada hardcoded no HTML).
2. **Benefícios** — cards com o racional de por que modelar assim (Silver
   L1 vs L2, Integration para reduzir integrações N×M, Analytics em
   português, alinhamento com bounded contexts, escalabilidade por
   subdomínio), redigidos a partir do racional em `kb/*.md`.
3. **Estudo de Caso — Compras/Autorização** — narrativa do pipeline
   (Bronze → Silver L1/L2 → Gold, produtos Core/Integration propostos) e as
   ressalvas já registradas nos ADRs
   [0001](./0001-escopo-detalhado-so-compras-autorizacao.md),
   [0003](./0003-fk-e-cardinalidade-explicitas-no-schema-fisico.md),
   [0005](./0005-fk-sem-cardinalidade-explicita.md),
   [0006](./0006-mapa-sem-outros-subdominios-e-sem-chips-externos.md) e
   [0007](./0007-integration-purchase-journey-sem-disputas.md) — sem
   reconstruir diagrama, explorador de tabelas ou notas de piloto dentro
   desta ferramenta. Em vez disso, um link/botão abre
   `parque-de-dados.html` (a ferramenta que já faz isso) em nova aba.

O conteúdo é redigido do zero a partir de `kb/` e `catalog/` — não reaproveita
a redação da apresentação apagada, que pode estar desalinhada do KB atual
(ajustado recentemente em `feature/adjustment-kb`). Mantém-se a convenção de
arquitetura do repositório: página única HTML+CSS+JS, offline, zero build,
zero CDN, dados injetados como `const DATA = {...}`, sem frameworks.

## Consequências

- Sem duplicação de código de diagrama/lineage entre as duas ferramentas —
  `apresentacao-executiva.html` depende de `parque-de-dados.html` existir e
  estar atualizado para o link do estudo de caso funcionar; se um dia o mapa
  for renomeado ou movido, o link precisa ser atualizado aqui também.
- Alguma duplicação de conteúdo conceitual entre `kb/*.md` (fonte canônica,
  redação técnica) e a apresentação (redação executiva, mais curta) é
  esperada e aceitável — quando o KB mudar de forma relevante, revisar a
  seção "Forma de Modelar" desta apresentação.
- O grid de subdomínios continua mostrando só Compras/Autorização com
  mapeamento técnico completo — mesma limitação já aceita nos ADRs 0001 e
  0006, não é reaberta aqui.
- Enquanto o Status for `Proposto`, este arquivo pode ser editado
  diretamente (seção Decisão/Consequências) para refletir ajustes de escopo
  pedidos durante a revisão — só passa a seguir a regra de "nunca reescrever,
  sempre superseder" depois de `Aceito`.
