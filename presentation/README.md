# 📊 Apresentação Interativa — Modelagem de Dados Cartão

## Abertura

**Arquivo gerado:** `apresentacao.html`

Para visualizar a apresentação, abra `apresentacao.html` diretamente no seu navegador (duplo-clique no arquivo ou arraste para o navegador). Não requer servidor ou build step — funciona 100% offline via `file://`.

## Conteúdo

A página é dividida em 4 seções principais:

1. **Início & Conceitos** — Introdução ao catálogo, três conceitos-chave (DDD, Camada Medalhão, Core/Integration/Analytics) e tabela de desambiguação sobre o significado de "Core".

2. **Mapa dos 15 Subdomínios** — Grid interativo dos bounded contexts (Elegibilidade, Onboarding, Compras/Autorização, etc.), com filtro por tipo DDD (Core/Support/Generic), lista de produtos por camada e atalho para detalhes técnicos onde disponível.

3. **Estudo de Caso: Compras/Autorização** — O único subdomínio com mapeamento técnico completo, com 4 sub-abas:
   - **Pipeline** — Diagramas visuais do fluxo Bronze→Silver(L1/L2)→Gold (dois diagramas: ingestão core e fan-out de Analytics).
   - **Explorador de Tabelas** — Busca e seleção entre 29 tabelas, com detalhes de colunas, tipos, descrições, lineage upstream/downstream.
   - **Relacionamentos** — Grafo de relacionamentos inferidos por padrão de coluna (`_id`, `event_id`, `transaction_id`), com aviso de que não são FKs formais validados.
   - **Notas do Piloto** — Anotações técnicas e pendências do mapeamento.

4. **Benefícios** — Cards curtos explicando por que essa abordagem de produtos de dados é valiosa (eficiência Silver L1≠L2, redução de integrações N×N, alinhamento com negócio, etc.).

## Como Regenerar

Se os YAMLs de catálogo ou KB forem editados, regenere a página com:

```bash
python3 scripts/build_apresentacao.py
```

O script:
- Lê `catalog/index.yaml` (15 subdomínios)
- Lê cada `catalog/<slug>/catalog.yaml` (produtos por subdomínio)
- Lê `catalog/compras-autorizacao/mapeamento-tecnico.yaml` (mapeamento técnico)
- Lê `catalog/compras-autorizacao/schema-fisico/schema-fisico.yaml` (29 tabelas + colunas)
- Calcula lineage, relacionamentos inferidos e detecção de gaps
- Injeta tudo em `presentation/apresentacao.template.html`
- Escreve `presentation/apresentacao.html` (arquivo final)

Saída inclui um resumo de contagens para verificação rápida:
- 15 subdomínios
- Produtos em Compras/Autorização
- 29 tabelas físicas mapeadas
- Tabelas externas não mapeadas (ex: `silver_l2.disputes__chargeback`)
- Relacionamentos inferidos

## Tecnologia

- **Arquivo único, zero CDN** — toda a página está em `apresentacao.html`, incluindo CSS/JS inline. Funciona 100% offline e abre direto via `file://`.
- **Dados embutidos** — JSON dos YAMLs é injetado como constante JS (`const DATA = {...}`), não fetched de arquivos.
- **Sem frameworks** — HTML/CSS/JS vanilla (nada de React, Vue, Mermaid CDN, etc.).
- **Diagramas SVG** — renderizados dinamicamente por JS puro a partir dos dados.
- **Navegação por hash** — `location.hash` permite deep-linking e volta/avanço do navegador.

## Verificação

Após gerar ou editar:

1. Abra `presentation/apresentacao.html` no navegador
2. Clique em cada seção (Início, Mapa, Estudo de Caso, Benefícios)
3. No Estudo de Caso:
   - Clique em nós dos diagramas de pipeline e relacionamentos
   - Busque/selecione tabelas no explorador
   - Verifique que `silver_l2.disputes__chargeback` aparece como "externo não mapeado" no diagrama de relacionamentos
4. Console do navegador (`F12`) não deve ter erros de JS
