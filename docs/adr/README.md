# Architecture Decision Records (ADR)

Registros das decisões arquiteturais deste repositório — o "porquê" por trás de
escolhas que não são óbvias só de ler o código ou o catálogo.

## Formato

Cada ADR segue uma versão enxuta do formato MADR:

- **Contexto** — o problema ou pergunta que motivou a decisão.
- **Decisão** — o que foi decidido.
- **Consequências** — o que isso implica (custos, trade-offs, o que fica em aberto).

Um ADR não é reescrito quando a decisão muda — cria-se um novo ADR que
supersede o anterior (linkando de volta), preservando o histórico de raciocínio.

## Índice

| ADR | Título | Status |
|-----|--------|--------|
| [0001](./0001-escopo-detalhado-so-compras-autorizacao.md) | Mapa detalhado só para Compras/Autorização; demais subdomínios como placeholder | Superseded parcialmente por [0006](./0006-mapa-sem-outros-subdominios-e-sem-chips-externos.md) |
| [0002](./0002-ferramenta-nova-independente-da-apresentacao-anterior.md) | Ferramenta de visualização nova, independente da apresentação anterior | Aceito |
| [0003](./0003-fk-e-cardinalidade-explicitas-no-schema-fisico.md) | FK e cardinalidade declaradas explicitamente no schema físico | Superseded por [0005](./0005-fk-sem-cardinalidade-explicita.md) |
| [0004](./0004-duas-categorias-de-seta-pipeline-vs-relacional.md) | Duas categorias de seta no mapa: pipeline (animada) vs relacional (estática) | Aceito |
| [0005](./0005-fk-sem-cardinalidade-explicita.md) | Relação estrutural sem cardinalidade explícita | Aceito |
| [0006](./0006-mapa-sem-outros-subdominios-e-sem-chips-externos.md) | Mapa cobre só a rede de tabelas de Compras/Autorização, sem outros subdomínios nem chips externos | Superseded parcialmente por [0007](./0007-integration-purchase-journey-sem-disputas.md) |
| [0007](./0007-integration-purchase-journey-sem-disputas.md) | integration_purchase_journey sem estorno/lineage de Disputas | Aceito |
| [0008](./0008-apresentacao-executiva-como-ferramenta-separada.md) | Apresentação executiva como ferramenta separada, linkando o mapa do parque de dados | Proposto |

## Quando criar um novo ADR

Ao tomar uma decisão que outra pessoa (ou agente de IA) precisaria conhecer
para não desfazê-la sem querer — especialmente quando a decisão tem trade-offs
não óbvios ou foi tomada depois de descartar uma alternativa razoável.
