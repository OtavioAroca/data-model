# 0007 — integration_purchase_journey sem estorno/lineage de Disputas

## Status

Aceito — supersede parcialmente [0006](./0006-mapa-sem-outros-subdominios-e-sem-chips-externos.md)
(o exemplo `disputes__chargeback` citado lá como card externo mantido)

## Contexto

`integration_purchase_journey` (`gold.integration__purchase_journey`) estava
modelado desde a v0 como união de purchase de crédito e débito **mais** o
estorno vindo de Disputas/Chargeback: a coluna `reversal_amount` no schema
físico, a lineage incluindo `silver_l2.disputes__chargeback`, e a descrição do
produto em `catalog.yaml` mencionando esse estorno.

O subdomínio Disputas/Chargeback não tem `schema-fisico.yaml` neste catálogo
(só Compras/Autorização tem, ver [0001](./0001-escopo-detalhado-so-compras-autorizacao.md)).
Por isso essa lineage aparecia no mapa como o único card externo tracejado
("externo — outro subdomínio"), inclusive quando filtrando só a camada
Integration — dando a impressão de que Disputas já está integrada, o que não
é o caso. `simulate.py` já refletia isso: `reversal_amount` era sempre `None`
com o comentário "Disputas não estão mapeadas yet".

O usuário pediu para remover essa referência: `integration_purchase_journey`
deve ser, por ora, só o vínculo entre crédito e débito.

## Decisão

- `catalog/compras-autorizacao/catalog.yaml`: descrição de
  `integration_purchase_journey` não menciona mais estorno/Disputas — só a
  união de crédito e débito com detalhamento de parcelas do crédito.
- `catalog/compras-autorizacao/mapeamento-tecnico.yaml`: removida
  `silver_l2.disputes__chargeback` da lineage de `integration_purchase_journey`.
- `catalog/compras-autorizacao/schema-fisico/schema-fisico.yaml`: removida a
  coluna `reversal_amount` de `gold.integration__purchase_journey`.
- `catalog/compras-autorizacao/schema-fisico/simulate.py`: removido o campo
  `reversal_amount` do registro gerado para o Gold.
- Artefatos derivados regenerados: `ddl.sql`, `mock.db` (via
  `scripts/ddl_generator.py` e `scripts/simulate_data.py`) e
  `presentation/parque-de-dados.html` (via
  `scripts/build_mapa_parque_dados.py`).
- `catalog.md`, `mapeamento-tecnico.md` e `kb/camada-medalhao.md` atualizados
  para espelhar os YAMLs.
- O card externo tracejado ("externo — outro subdomínio") continua existindo
  como recurso do mapa (decisão de [0006](./0006-mapa-sem-outros-subdominios-e-sem-chips-externos.md)
  não é revertida) — só não há hoje nenhuma lineage que o acione, já que
  `disputes__chargeback` era o único caso.

## Consequências

- `integration_purchase_journey` reflete só o que existe hoje: crédito +
  débito. O mapa, filtrando por Integration, não mostra mais nenhum vínculo
  com Disputas.
- Quando Disputas/Chargeback ganhar `schema-fisico.yaml` próprio, reintroduzir
  o estorno em `integration_purchase_journey` (coluna, lineage, descrição) é
  uma decisão nova — este ADR documenta que a remoção atual foi deliberada,
  não um esquecimento.
