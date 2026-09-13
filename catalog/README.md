# Catálogo de Produtos de Dados — Domínio Cartão

## Como usar

Primeira versão (V0) do catálogo de produtos de dados propostos para todos os subdomínios do domínio Cartão, seguindo o modelo Core / Integration / Analytics.

### O que é este arquivo

Cada subdomínio (bounded context do negócio) tem sua própria pasta com:
- **catalog.md/yaml**: lista de produtos de dados propostos (Core, Integration, Analytics).
- **mapeamento-tecnico.md/yaml** (quando disponível): mapeamento de produtos para tabelas físicas (Bronze/Silver/Gold), pipeline e lineage.
- **schema-fisico/** (quando o subdomínio tem DDL+simulação): subpasta com definição de colunas, DDL, lógica de simulação e banco de dados mock.

### O que este V0 NÃO é

Não é uma lista definitiva nem exaustiva de tabelas físicas. Nomes, donos e consumidores são propostas iniciais para validação com cada time de domínio — esperado que mude bastante entre V0 e V1.

Alguns subdomínios provavelmente têm produtos adicionais que só quem opera o sistema de origem vai enxergar — use este catálogo como ponto de partida da conversa, não como inventário fechado.

### Convenção de cores da camada (produto de dados)

| Camada | Significado |
|--------|-------------|
| **Core** | Produto alinhado a um único bounded context / sistema de origem |
| **Integration** | Produto que cruza mais de um bounded context |
| **Analytics** | Produto moldado para um caso de uso de consumo final |

Para entender os conceitos — DDD, Bounded Context, Camada Medalhão (Bronze/Silver/Gold) e a distinção entre Core/Integration/Analytics — ver [Conhecimento Base (KB)](../kb/README.md).

### Contrato e Validação

Cada arquivo YAML no catálogo segue um **contrato** (JSON Schema) que define campos obrigatórios, tipos permitidos e formatos. Isso garante que novos produtos/subdomínios adicionados (à mão ou por agente de IA) seguem o mesmo padrão.

**Para adicionar um novo subdomínio, mapeamento técnico ou validar alterações:**

Veja [`_schema/README.md`](./_schema/README.md) — tem templates, guia passo a passo, e como rodar a validação.

Quick start:
```bash
# Validar todo o catálogo
python3 scripts/validate_catalog.py

# Adicionar novo subdomínio
cp catalog/_schema/catalog.template.yaml catalog/<novo-slug>/catalog.yaml
# Editar, adicionar a index.yaml, e validar
```

---

## Subdomínios

| Subdomínio | O que resolve | Sistemas de origem | Tipo (DDD) | Mapeamento Técnico |
|------------|---------------|-------------------|-----------|-------------------|
| Elegibilidade | Avalia se um cliente pode receber uma oferta de cartão, e sob quais condições | Motor de elegibilidade / bureaus de crédito | Core | — |
| Onboarding | Conduz a proposta, validação de identidade (KYC) e abertura da conta cartão | Sistema de proposta, KYC/antifraude cadastral | Core | — |
| Conta Cartão | Representa o relacionamento contratual entre cliente e produto cartão | Core banking de contas | Core | — |
| Cartão | Gerencia o ciclo de vida do plástico/virtual: emissão, ativação, bloqueio, reemissão | Sistema de emissão de cartões | Core | — |
| Limite | Concede, ajusta e controla o limite de crédito disponível na conta cartão | Motor de crédito/limite | Core | — |
| Compras / Autorização | Autoriza e captura as transações realizadas com o cartão, incluindo o plano de parcelamento decidido no ato da compra | Switch de autorização, rede/bandeira | Core | ✅ |
| Fatura | Gera e fecha a fatura periódica com as transações e encargos do ciclo | Billing engine | Core | — |
| Pagamento da Fatura | Registra e concilia os pagamentos feitos pelo cliente contra a fatura, e estrutura o saldo devedor em parcelas (rotativo) quando o pagamento é parcial | Sistema de pagamentos/liquidação | Support | — |
| Disputas / Chargeback | Processa contestações de transações e o fluxo de chargeback com a bandeira | Sistema de disputas | Support | — |
| Fraude | Avalia risco de fraude em tempo real e retroativamente | Motor antifraude | Core | — |
| Cobrança | Trata contas em atraso, régua de contato e negociação | Sistema de cobrança/régua | Support | — |
| Benefícios / Rewards | Administra pontos, cashback e resgates associados ao uso do cartão | Plataforma de rewards | Generic | — |
| Encerramento | Processa o cancelamento definitivo de cartão ou conta | Core banking de contas | Support | — |
| Anuidade | Calcula, cobra e administra isenções/negociação da anuidade do cartão | Motor de anuidade (regras de isenção e negociação) | Support | — |
| Entrega | Rastreia a entrega física do cartão, do despacho até a confirmação de recebimento | Integração com transportadora/Correios | Support | — |

