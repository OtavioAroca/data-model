# 0010 — Mapa interativo embutido no Estudo de Caso, template do mapa reconciliado com o arquivo gerado

## Status

Aceito

> Nasceu como `Proposto` (mesmo padrão dos ADRs 0008/0009) e foi aceito após
> aprovação da [PR #13](https://github.com/OtavioAroca/data-model/pull/13).

## Contexto

O Estudo de Caso da apresentação executiva
(`presentation/apresentacao-executiva.html`) já passou por três rodadas de
feedback tentando mostrar "todas as tabelas" de Compras/Autorização: primeiro
só 4 tabelas de exemplo (pipeline ilustrativo), depois uma contagem por
camada medalhão, depois os 29 nomes de tabela em texto (ver
[ADR 0009](./0009-grid-subdominios-por-camada-produto-pagina-unica-sem-emoji.md),
ponto 5). O usuário deixou claro que nada disso equivale ao que já existe em
`presentation/parque-de-dados.html` — o pedido explícito, confirmado por
pergunta direta, foi ter **as mesmas funcionalidades do mapa** (busca,
filtros, pan/zoom, arrastar, legenda, setas de lineage animadas, painel
lateral com colunas/tipos/relações) dentro do Estudo de Caso, só que as
tabelas comecem **recolhidas** (sem mostrar os campos) — diferente do padrão
atual do mapa (que abre com todas expandidas).

Isso reverte, para o Estudo de Caso, a decisão dos ADRs 0002/0008/0009 de
manter as duas ferramentas desacopladas (uma linka a outra, nenhuma embute).

### Achado durante a implementação: template do mapa estava desatualizado

Ao investigar como reaproveitar `parque-de-dados.html`, descobrimos que
`presentation/parque-de-dados.template.html` estava **dessincronizado** do
arquivo gerado. Dois commits (`adjustment-fields-explode/html`,
`1987598`, e `adjustment-02`, `b0b3f71`) editaram **só**
`presentation/parque-de-dados.html` diretamente, sem tocar no template —
violando a própria convenção do repositório (raiz do `README.md` e
`presentation/README.md`: o `.html` é gerado, não editado à mão). Isso
significava que rodar `scripts/build_mapa_parque_dados.py` teria
**regredido** o mapa em produção, removendo funcionalidades reais que os
usuários já usam: expandir/recolher colunas por cartão, arrastar tabelas
livremente (com resolução de colisão), legenda de cores, roteamento de setas
com cantos suaves e distribuição de múltiplas conexões, e ocultação em
cascata de tabelas downstream ao filtrar uma camada.

## Decisão

1. **Reconciliar o template com o arquivo gerado.** Reconstruímos
   `parque-de-dados.template.html` a partir do `parque-de-dados.html`
   atualmente commitado (substituindo o bloco `const DATA = {...}` pelo
   marcador `/*__PARQUE_DE_DADOS_DATA__*/`), em vez de tentar reaplicar os
   dois diffs manualmente — mais seguro, porque garante round-trip idêntico
   por construção. Verificado: `python3 scripts/build_mapa_parque_dados.py`
   a partir do template reconstruído produz um `parque-de-dados.html`
   byte-a-byte idêntico ao commitado (`git diff` vazio). A partir de agora, o
   template volta a ser a fonte de verdade real — qualquer ajuste futuro no
   mapa deve editar o template, não o `.html` gerado.

2. **Parâmetro `?compacto=1`.** Adicionado a
   `parque-de-dados.template.html`: uma constante
   `const COMPACTO = new URLSearchParams(location.search).has("compacto")`
   controla o estado inicial de cada cartão (`n.expanded = !COMPACTO`, nos
   dois lugares onde antes era fixo em `true` — layout inicial e handler do
   botão "Reorganizar"). Sem o parâmetro, o comportamento é idêntico ao atual
   (tabelas expandidas). Nenhuma outra mudança — busca, filtros, pan/zoom,
   arrastar, legenda, painel lateral continuam idênticos.

3. **Embutir via `<iframe>`.** `presentation/apresentacao-executiva.template.html`
   passa a ter, na seção Estudo de Caso:
   ```html
   <iframe src="parque-de-dados.html?compacto=1" class="mapa-embed" loading="lazy"></iframe>
   ```
   Zero duplicação de código de renderização — o iframe carrega literalmente
   o mesmo arquivo já gerado por `scripts/build_mapa_parque_dados.py`.
   `scripts/build_apresentacao_executiva.py` não precisou de nenhuma
   dependência nova (não importa nada do outro script) — a reutilização
   acontece no nível do HTML já publicado, não no nível do código Python.

4. **Removido, por redundância com o iframe:** o diagrama ilustrativo de 4
   caixas (`pipeline-flow`) e a lista de nomes de tabela em texto
   (`tabelas-grid`, introduzida no ADR 0009 ponto 5) — o mapa embutido já
   mostra as 29 tabelas de verdade, com colunas, tipos e lineage reais.
   Mantido: texto introdutório (dois rails, tabelas de parcelamento), a linha
   de estatísticas (`stats-row`, resumo rápido acima do iframe), a lista
   "Produtos de dados propostos" (dado de catálogo, não de tabela física —
   fora do escopo do iframe), "Ressalvas do piloto", e o link "Abrir mapa
   interativo" (agora reposicionado como opção de tela cheia).

## Consequências

- `apresentacao-executiva.html` passa a ter uma dependência de runtime forte
  de `parque-de-dados.html` estar na mesma pasta — já existia para o link,
  agora também para o iframe renderizar algo (sem ele, o iframe fica em
  branco, sem erro visível).
- Altura do iframe é fixa (`640px` — o mapa usa pan/zoom, não altura
  natural); quem precisar de mais espaço usa o link "abrir em nova aba".
- `?compacto=1` é uma pequena "API" pública de `parque-de-dados.html` — se o
  JS do mapa for reescrito no futuro, esse parâmetro precisa continuar
  funcionando (ou o embed volta a abrir expandido — degrada sem quebrar, só
  sem o efeito desejado).
- **A partir de agora, `parque-de-dados.template.html` é a fonte de verdade
  real de novo** — qualquer ajuste no mapa (inclusive os que só afetam
  `parque-de-dados.html` isoladamente) deve ser feito no template e
  regenerado via `scripts/build_mapa_parque_dados.py`, nunca direto no
  `.html`. Editar o `.html` direto voltaria a quebrar o embed na próxima vez
  que alguém rodasse o script sem perceber a dessincronização.
- Supersede parcialmente o [ADR 0008](./0008-apresentacao-executiva-como-ferramenta-separada.md)
  (Estudo de Caso "linka, não embute") e o
  [ADR 0009](./0009-grid-subdominios-por-camada-produto-pagina-unica-sem-emoji.md)
  (ponto 5, "lista simples sem colunas/lineage").
