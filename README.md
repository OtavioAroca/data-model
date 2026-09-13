# data-model

Catálogo de produtos de dados (V0) do domínio **Cartão**, organizado por subdomínio (bounded context) segundo os modelos **DDD** (Core/Support/Generic), **Camada Medalhão** (Bronze/Silver/Gold) e **Core/Integration/Analytics** (escopo do produto de dados).

O objetivo é servir de ponto de partida para conversas com os times de domínio sobre quais produtos de dados deveriam existir, quem os consome e como se mapeiam para tabelas físicas — não é um inventário definitivo.

## Estrutura do repositório

```
catalog/            Catálogo de produtos de dados por subdomínio (15 subdomínios do domínio Cartão)
├── _schema/         Contratos JSON Schema + templates para catalog/mapeamento-tecnico/schema-fisico
├── index.yaml        Índice dos 15 subdomínios
└── <slug>/           Um por subdomínio (ex: compras-autorizacao, fatura, limite...)
    ├── catalog.md/yaml            Produtos de dados propostos (Core/Integration/Analytics)
    ├── mapeamento-tecnico.md/yaml  Mapeamento produto → tabela física, pipeline, lineage (quando disponível)
    └── schema-fisico/               DDL, colunas, simulação de dados e banco mock (quando disponível)

kb/                  Base de conhecimento com os conceitos fundamentais (DDD, Camada Medalhão, Core/Integration/Analytics)
presentation/                Apresentação executiva e mapa interativo do parque de dados (HTML, offline, zero build) gerados a partir do catálogo
scripts/             Scripts Python de build, validação, geração de DDL e simulação de dados
docs/adr/            Registros de decisão arquitetural (ADR)
```

Hoje, **Compras/Autorização** é o único subdomínio com mapeamento técnico completo (produtos → 29 tabelas físicas → DDL → simulação), servindo de piloto para os demais.

## Por onde começar

- **Entender os conceitos**: [`kb/README.md`](kb/README.md)
- **Ver o catálogo e como usá-lo**: [`catalog/README.md`](catalog/README.md)
- **Adicionar/validar um subdomínio, mapeamento técnico ou schema físico**: [`catalog/_schema/README.md`](catalog/_schema/README.md)
- **Ver a apresentação executiva e o mapa interativo do parque de dados**: [`presentation/README.md`](presentation/README.md)
- **Ver as decisões arquiteturais**: [`docs/adr/README.md`](docs/adr/README.md)

## Setup

```bash
pip install -r requirements.txt
```

## Comandos principais

```bash
# Validar todo o catálogo contra o contrato (schemas)
python3 scripts/validate_catalog.py

# Gerar DDL SQL a partir de um schema-fisico.yaml
python3 scripts/ddl_generator.py <slug>

# Popular um mock.db (SQLite) com dados simulados
python3 scripts/simulate_data.py --subdominio <slug> --n 50

# Regenerar o mapa do parque de dados (presentation/parque-de-dados.html)
python3 scripts/build_mapa_parque_dados.py

# Regenerar a apresentação executiva (presentation/apresentacao-executiva.html)
python3 scripts/build_apresentacao_executiva.py
```

## Subdomínios do domínio Cartão

Elegibilidade, Onboarding, Conta Cartão, Cartão, Limite, Compras/Autorização, Fatura, Pagamento da Fatura, Disputas/Chargeback, Fraude, Cobrança, Benefícios/Rewards, Encerramento, Anuidade, Entrega.

Detalhes de cada um (o que resolve, sistemas de origem, tipo DDD) em [`catalog/README.md`](catalog/README.md#subdomínios).
