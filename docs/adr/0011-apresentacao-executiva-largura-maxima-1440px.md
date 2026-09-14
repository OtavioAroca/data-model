# 0011 — Apresentação Executiva com largura máxima de 1440px

## Status

Aceito

## Contexto

`presentation/apresentacao-executiva.html` (gerado a partir de
`presentation/apresentacao-executiva.template.html` por
`scripts/build_apresentacao_executiva.py`) usava
`main { max-width: 980px; margin: 0 auto; padding: 8px 24px 60px; }`. Em
telas comuns de notebook/monitor (1440–1920px de largura), isso deixava
bordas laterais grandes e desperdiçava espaço horizontal em uma página que já
tem grids de 2–3 colunas (`.grid-2`, `.grid-3`, `.sub-grid`), tabela de
desambiguação e o mapa interativo embutido via `<iframe class="mapa-embed">`
(que ocupa 100% da largura do `main` — ver
[ADR 0010](./0010-mapa-interativo-embutido-no-estudo-de-caso.md)). O usuário
pediu para a página "preencher toda a tela", apontando a borda excessiva
atual.

Duas opções foram consideradas: remover o `max-width` por completo
(full-bleed) ou apenas aumentá-lo. `presentation/parque-de-dados.html` já é
full-viewport, mas é uma ferramenta de canvas/pan-zoom — não é o padrão a
seguir aqui, pois `apresentacao-executiva.html` é uma página de
texto/relatório, e cards/tabelas/parágrafos ficam ilegíveis se esticados até
a borda em monitores ultrawide/4K. Optou-se por aumentar o teto para 1440px,
mantendo o `main` centralizado — elimina a borda excessiva nas larguras mais
comuns sem esticar demais o conteúdo em telas muito grandes.

## Decisão

1. Alterado, em **`presentation/apresentacao-executiva.template.html`**
   (fonte de verdade — nunca editar o `.html` gerado diretamente):
   ```css
   main { max-width: 1440px; margin: 0 auto; padding: 8px 32px 60px; }
   ```
   (era `max-width: 980px` com `padding: 8px 24px 60px`; o padding lateral
   subiu de `24px` para `32px` para não colar o conteúdo na borda da janela
   nas larguras maiores agora disponíveis.)
2. `presentation/apresentacao-executiva.html` foi regenerado rodando
   `python3 scripts/build_apresentacao_executiva.py` — o diff resultante do
   `.html` é só essa mesma linha de CSS, sem tocar em dados/JS.
3. Mantido sem alteração: `.lede { max-width: 720px }` (largura de leitura de
   parágrafo, independente da largura do `main`) e os breakpoints
   responsivos existentes (`@media` em `.grid-3`/`.grid-2`/`.sub-grid`), que
   continuam a colapsar para menos colunas em telas estreitas.

## Consequências

- Em monitores comuns (1440–1920px), a borda lateral vazia diminui
  visivelmente; cards dos grids e a tabela de desambiguação ficam
  proporcionalmente mais largos, e o iframe do mapa (`.mapa-embed`, 100% da
  largura do `main`) ganha mais espaço horizontal.
- Ainda existe um teto (1440px, não full-bleed) — em monitores 4K/ultrawide
  continua havendo borda lateral, deliberadamente, para não esticar
  demais texto e cards em colunas fixas.
- Qualquer ajuste futuro de layout deve continuar sendo feito no
  `.template.html` e propagado via `scripts/build_apresentacao_executiva.py`,
  nunca direto no `.html` gerado (mesma armadilha já documentada no
  [ADR 0010](./0010-mapa-interativo-embutido-no-estudo-de-caso.md) para o
  outro template deste diretório).
