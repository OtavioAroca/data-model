# Knowledge Base — Conceitos Fundamentais

## Índice

| Conceito | O que é | Arquivo |
|----------|---------|---------|
| **DDD (Domain-Driven Design)** | Classificação dos subdomínios do negócio por importância estratégica (Core, Support, Generic) e conceitos compartilhados entre time técnico e negócio | [ddd.md](./ddd.md) |
| **Camada Medalhão** | Estágios de processamento de dados (Bronze, Silver, Gold) com a nuance Silver L1 vs L2 descoberta no piloto | [camada-medalhao.md](./camada-medalhao.md) |
| **Core / Integration / Analytics** | Classificação dos produtos de dados por escopo (quantos bounded contexts) e público-alvo | [core-integration-analytics.md](./core-integration-analytics.md) |

---

## Como esses conceitos se relacionam

O catálogo usa três classificações diferentes que às vezes usam os mesmos nomes — aqui está a distinção:

| Conceito | O que classifica? | Valores | Exemplo do domínio Cartão |
|----------|------------------|---------|---------------------------|
| **DDD — Subdomínio** | Um bounded context do negócio (ex: um sistema de origem) | Core, Support, Generic | `Compras / Autorização` = Core (diferencial competitivo) |
| **Camada Medalhão** | Uma tabela física no data lake, por estágio de processamento | Bronze (raw), Silver (limpo), Gold (pronto) | `bronze.purchases__credit_approved` → `silver_l2.purchases__credit_purchase` → `gold.integration__purchase_journey` |
| **Core / Integration / Analytics** | Um produto de dados, por quantos bounded contexts ele cruza | Core (1 bounded context), Integration (cruza >1), Analytics (moldado para caso de uso final) | `core_credit_purchase` (1 contexto) vs `integration_purchase_journey` (cruza crédito + débito + disputas) |

### Por que "Core" aparece em dois places?

- **Core (DDD)**: significa que o subdomínio é um diferencial competitivo do negócio — a empresa quer estar melhor nele do que a concorrência (ex: Elegibilidade, Fraude).
- **Core (produto de dados)**: significa que o produto de dados representa **exatamente um** bounded context, sem cruzamento com outros (ex: `core_credit_purchase` = só compras de crédito, sem misturar com débito ou outras dimensões).

Não são mutuamente dependentes — um `Core` subdomínio (DDD) pode gerar produtos em qualquer das três camadas (`Core`, `Integration`, `Analytics`), e vice-versa.

---

## Próximos passos

Leia os tópicos na ordem que preferir. Se está vindo do catálogo ([`catalogo/`](../catalogo/README.md)), comece por [camada-medalhao.md](./camada-medalhao.md) se tem dúvida sobre `bronze`/`silver`/`gold`, ou [ddd.md](./ddd.md) se quer entender subdomínios.
