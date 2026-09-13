# Produto de Dados — o que é

## Definição

Um **produto de dados** é um dataset **governado**, com **dono**, **contrato** (schema estável) e **consumidores conhecidos** — pensado e mantido para ser consumido por outras pessoas ou sistemas, não só um efeito colateral de um pipeline.

Isso é diferente de "uma tabela qualquer no data lake". Uma tabela solta pode existir só porque um pipeline precisou de um lugar para gravar um resultado intermediário — ninguém é responsável por ela, o schema pode mudar sem aviso, e não há garantia de que vai continuar existindo. Um produto de dados é o oposto: alguém assumiu a responsabilidade de mantê-lo estável e utilizável por terceiros.

## O que torna algo um produto de dados

- **Dono**: uma pessoa ou time responsável por manter o produto, responder por incidentes de qualidade e decidir mudanças de schema.
- **Contrato**: um schema documentado e (na prática) estável — quem consome sabe o que esperar, e mudanças que quebram o contrato são comunicadas antes de acontecer.
- **Consumidores conhecidos**: outros produtos, dashboards, aplicações ou pessoas que dependem dele — não é um dataset "órfão" que ninguém sabe quem usa.
- **Cadência de atualização definida**: streaming, incremental, batch diário — o consumidor sabe a frequência com que pode esperar dados novos (SLA).
- **Descoberta via catálogo**: está listado no [`catalog/`](../catalog/README.md), com essas informações documentadas, em vez de existir só no conhecimento tácito de quem o criou.

Sem essas propriedades, o que existe é só uma tabela — pode virar um produto de dados no futuro, mas hoje não é um.

## Produto de dados não é a mesma coisa que tabela física

Um produto de dados é um conceito de **negócio/contrato**; a tabela física é o **estágio de processamento** onde ele mora (Bronze, Silver ou Gold — ver [camada-medalhao.md](./camada-medalhao.md)).

Um produto pode:
- Ser servido por **mais de uma** tabela física ao longo do tempo (ex: uma migração de motor de processamento sem quebrar o contrato para o consumidor).
- Precisar de tabelas em **camadas diferentes** dependendo do consumidor (ex: um produto Analytics pode precisar ler de Silver L1 para calcular latência entre eventos, e não da versão materializada em L2).

### Exemplo no domínio Cartão

O produto de dados `core_credit_purchase` (histórico completo de compras de crédito) é materializado hoje na tabela física `silver_l2.purchases__credit_purchase`. O produto é a unidade que tem dono, contrato e consumidores; a tabela é onde ele está fisicamente armazenado agora.

## Por que classificar produtos de dados em Core / Integration / Analytics

Depois que um dataset é reconhecido como produto de dados (tem dono, contrato, consumidores), a pergunta seguinte é **para quem** ele foi moldado e **quantos bounded contexts** ele cruza — isso é o que a classificação Core/Integration/Analytics resolve. Ver [core-integration-analytics.md](./core-integration-analytics.md) para a distinção completa entre as três camadas.
