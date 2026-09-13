# 0005 — Relação estrutural sem cardinalidade explícita

## Status

Aceito — supersede [0003](./0003-fk-e-cardinalidade-explicitas-no-schema-fisico.md)

## Contexto

[0003](./0003-fk-e-cardinalidade-explicitas-no-schema-fisico.md) introduziu um
campo `cardinalidade` (`1:1`/`1:N`) dentro de `chave_estrangeira`, populado nas
7 relações estruturais do schema físico de Compras/Autorização, e exibido no
mapa como rótulo `1`/`N` em cada ponta da seta relacional.

Depois de ver o mapa gerado, o usuário pediu para remover essa indicação de
cardinalidade.

## Decisão

Reverter a parte de cardinalidade de 0003:

- `catalog/_schema/schema-fisico.schema.json`: `chave_estrangeira` volta a ter
  só `tabela` + `coluna` (sem `cardinalidade`, sem enum, sem exigir esse
  campo).
- `catalog/compras-autorizacao/schema-fisico/schema-fisico.yaml`: removida a
  linha `cardinalidade` das 7 declarações de `chave_estrangeira` existentes —
  as referências (`tabela`/`coluna`) continuam.
- `scripts/validate_catalog.py`: removida a checagem de consistência entre
  `cardinalidade` e `chave_primaria`. A checagem de que toda
  `chave_estrangeira` aponta para uma coluna que existe e é `chave_primaria`
  na tabela referenciada **continua** — é uma checagem estrutural da FK em si,
  independente de cardinalidade.
- `scripts/build_mapa_parque_dados.py` e o mapa
  (`presentation/parque-de-dados.template.html`): a seta relacional (linha
  roxa tracejada) continua sendo desenhada a partir de `chave_estrangeira`,
  só sem o rótulo `1`/`N` em cada ponta.

## Consequências

- O mapa mostra que duas tabelas se relacionam por uma coluna específica, mas
  não afirma a cardinalidade dessa relação — evita expor uma leitura (1:1 vs
  1:N) que o usuário não quis exibir.
- Se cardinalidade explícita for necessária de novo no futuro, o campo pode
  ser reintroduzido no contrato — o histórico de 0003 documenta o desenho
  original (inclusive a distinção entre FK estrutural, lineage e referência
  externa, que continua válida).
