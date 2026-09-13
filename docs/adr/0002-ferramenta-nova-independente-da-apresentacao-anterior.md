# 0002 — Ferramenta de visualização nova, independente da apresentação anterior

## Status

Aceito

## Contexto

Já existia uma apresentação interativa gerada
(`scripts/build_apresentacao.py` → `presentation/apresentacao.template.html` →
`presentation/apresentacao.html`), documentada em `presentation/README.md`.
Ela cobria início/conceitos, um grid dos 15 subdomínios, um estudo de caso de
Compras/Autorização (pipeline, explorador de tabelas, relacionamentos
inferidos por nome de coluna) e uma seção de benefícios.

O usuário apagou os três arquivos (`git status` mostrou os 3 como `deleted`
no início desta sessão) e pediu explicitamente uma ferramenta nova, **sem
relação com a anterior**, para o mapa do parque de dados.

## Decisão

Construir uma ferramenta desacoplada, com nomes próprios (não reaproveitar
nem os nomes nem o código dos arquivos apagados):

- `scripts/build_mapa_parque_dados.py` (script de build novo)
- `presentation/parque-de-dados.template.html` (template novo)
- `presentation/parque-de-dados.html` (saída gerada)
- `presentation/README.md` (novo, documentando só esta ferramenta)

Mantém-se a convenção de arquitetura já documentada no README raiz do
repositório — página única, offline, zero build, dados embutidos como `const
DATA = {...}` — porque essa convenção é do repositório como um todo (citada no
README raiz, não é específica dos arquivos apagados) e não foi questionada
pelo usuário.

## Consequências

- Não há reaproveitamento de código entre a apresentação antiga (apagada) e o
  mapa novo — cada leitura dos YAMLs de catálogo é reimplementada do zero no
  novo script.
- Se no futuro se quiser voltar a ter uma apresentação mais ampla (conceitos,
  benefícios, os 15 subdomínios lado a lado), ela pode ser uma ferramenta
  separada que eventualmente embuta ou linka o mapa gerado aqui — não é papel
  deste ADR decidir isso agora.
