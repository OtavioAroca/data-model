# 0001 — Mapa detalhado só para Compras/Autorização; demais subdomínios como placeholder

## Status

Aceito

## Contexto

O pedido era um "mapa do parque de dados" com todas as tabelas, campos, tipos
e relações. O catálogo (`catalog/`) tem 15 subdomínios, mas só
**Compras/Autorização** passou pela etapa de schema físico
(`catalog/compras-autorizacao/schema-fisico/schema-fisico.yaml`, 29 tabelas
com colunas e tipos) e mapeamento técnico
(`catalog/compras-autorizacao/mapeamento-tecnico.yaml`, lineage Bronze→Silver→Gold).

Os outros 14 subdomínios (Elegibilidade, Onboarding, Conta Cartão, Cartão,
Limite, Fatura, Pagamento da Fatura, Disputas/Chargeback, Fraude, Cobrança,
Benefícios/Rewards, Encerramento, Anuidade, Entrega) só têm produtos de dados
**propostos** (`catalog.yaml`) — nenhuma tabela física, coluna ou tipo definido.
O próprio `catalog/README.md` já avisa: "não é uma lista definitiva nem
exaustiva de tabelas físicas [...] esperado que mude bastante entre V0 e V1".

Desenhar campos/tipos/relações para esses 14 exigiria inventar uma estrutura
física que ninguém validou com o time de domínio — contradiz o propósito do
catálogo V0, que é ponto de partida de conversa, não inventário fechado.

## Decisão

O mapa interativo (canvas com tabelas, campos, tipos, setas de relação e de
pipeline animado) cobre **só Compras/Autorização**, que é o único subdomínio
com dado físico real para desenhar com fidelidade.

Os outros 14 subdomínios aparecem em uma seção separada e mais simples: cartões
de produto de dados (Core/Integration/Analytics, descrição, consumidores,
dono), sem campo ou tabela física, com um aviso visível de "sem mapeamento
técnico — sem tabela física definida ainda".

## Consequências

- O mapa fica fiel ao que existe hoje — não corre o risco de alguém tomar uma
  coluna ou relação inventada como se fosse real.
- Quando um novo subdomínio ganhar `mapeamento-tecnico.yaml` +
  `schema-fisico.yaml` (seguindo o padrão já usado em Compras/Autorização),
  ele pode entrar na mesma seção detalhada do mapa — a ferramenta de build
  (`scripts/build_mapa_parque_dados.py`) deve ser escrita pensando nisso desde
  já: iterar sobre "subdomínios com schema físico" em vez de fixar
  `compras-autorizacao` como caso especial hardcoded onde for razoável.
- Por ora, o mapa não mostra tabelas físicas para 14 dos 15 subdomínios — quem
  quiser ver profundidade de detalhe similar precisa primeiro fazer o trabalho
  de modelagem física naquele subdomínio.
