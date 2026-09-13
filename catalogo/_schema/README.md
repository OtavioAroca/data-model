# Contrato do Catálogo — Schema e Validação

## O que é o contrato?

O **contrato** define a estrutura esperada de cada arquivo YAML no catálogo:
- Quais campos são obrigatórios vs. opcionais
- Quais valores são permitidos (enums: "Core", "Integration", "Analytics"; "Bronze", "Silver", etc)
- Quais formatos são esperados (ex: nome de produto sempre começa com `core_`, `integration_` ou `analytics_`)

O contrato é um **acordo entre humanos e máquinas** — garante que:
1. Um novo subdomínio/produto adicionado (à mão ou por agente de IA) segue o mesmo padrão que os outros.
2. Quando o padrão evolui, o contrato documenta a mudança uma única vez — o validador avisa exatamente quais arquivos precisam se adequar.

Sem contrato, o catálogo tende a divergir aos poucos (campos faltando, nomes inconsistentes, valores inválidos).

---

## Onde estão os schemas?

- **`catalogo.schema.json`** — Contrato de `catalogo/<slug>/catalogo.yaml` (produtos de dados de um subdomínio)
- **`mapeamento-tecnico.schema.json`** — Contrato de `catalogo/<slug>/mapeamento-tecnico.yaml` (mapeamento para tabelas físicas)
- **`index.schema.json`** — Contrato de `catalogo/index.yaml` (índice dos 15 subdomínios)

---

## Como validar?

### Uma vez

```bash
python3 scripts/validate_catalogo.py
```

Termina com exit code 0 se passou, ≠ 0 se houver problemas.

### Sempre (CI/Pre-commit)

Adicione a um hook de Git (`.git/hooks/pre-commit` ou via ferramenta como `pre-commit`):

```bash
#!/bin/bash
python3 scripts/validate_catalogo.py || exit 1
```

Assim, nenhum commit com dados inconsistentes entra no repo.

---

## Estrutura de pastas de um subdomínio

Todo subdomínio (`catalogo/<slug>/`) tem uma estrutura padrão:

```
catalogo/<slug>/
├── catalogo.md              # Documentação em Markdown (gerada)
├── catalogo.yaml            # Produtos de dados (Core/Integration/Analytics)
├── mapeamento-tecnico.md    # Documentação em Markdown (gerada, se houver mapeamento)
├── mapeamento-tecnico.yaml  # Mapeamento para tabelas físicas (opcional)
└── schema-fisico/           # Subpasta opcionalmente adicionada quando há DDL+simulação
    ├── schema-fisico.yaml       # Definição de colunas das tabelas
    ├── ddl.sql                  # SQL das tabelas (gerado por ddl_generator.py)
    ├── simulate.py              # Lógica de simulação de dados
    └── mock.db                  # Banco de dados gerado (regenerável, gitignored)
```

**Observações:**
- `catalogo.md`, `catalogo.yaml`: obrigatório em todo subdomínio.
- `mapeamento-tecnico.md/yaml`: adicionado quando o subdomínio documenta o mapeamento para tabelas físicas.
- `schema-fisico/`: criada apenas quando o subdomínio passa pela etapa de "schema físico + DDL + simulação" (não é obrigatória para todos). Os 4 arquivos dentro dela são agrupados por afinidade: não vivem soltos na raiz, mantendo a estrutura organizada.
- `mock.db` é gitignored (regenerável rodando `python3 scripts/simulate_data.py --subdominio <slug> --n 50`).

---

## Como adicionar um novo subdomínio?

### 1. Copiar template

```bash
cp catalogo/_schema/catalogo.template.yaml catalogo/<novo-slug>/catalogo.yaml
```

Substitua `<novo-slug>` por um nome em kebab-case sem acentos (ex: `meio-de-pagamento`, `rede-de-parceiros`).

### 2. Editar arquivo

Abra `catalogo/<novo-slug>/catalogo.yaml` em um editor com suporte a YAML Schema (VSCode + YAML extension):

- O editor **automaticamente** carrega o schema (via comentário `$schema` no topo) e oferece **autocomplete** e **erro em tempo real**.
- Campos obrigatórios aparecem com ⚠ se faltarem.
- Valores inválidos (ex: `camada: Invalida`) ficam com squiggle vermelho imediatamente.

### 3. Adicionar a index.yaml

Abra `catalogo/index.yaml` e adicione uma entrada em `subdominios[]`:

```yaml
- nome: "Novo Subdomínio"
  slug: "novo-slug"
  bounded_context: "Descrição do bounded context"
  sistemas_origem: "Sistemas que alimentam"
  tipo_ddd: "Core"  # ou Support, Generic
  tem_mapeamento_tecnico: false  # true depois de criar mapeamento-tecnico.yaml
```

### 4. Validar

```bash
python3 scripts/validate_catalogo.py
```

Deve passar sem erros. Se houver erros, o script aponta exatamente qual arquivo/campo está errado.

---

## Como adicionar mapeamento técnico a um subdomínio?

### 1. Copiar template

```bash
cp catalogo/_schema/mapeamento-tecnico.template.yaml catalogo/<slug>/mapeamento-tecnico.yaml
```

### 2. Editar arquivo

Use o mesmo fluxo: editor carrega o schema automaticamente.

Campos principais:
- **`contexto`**: uma frase sobre versão/piloto/observações deste mapeamento.
- **`notas[]`**: observações específicas (NÃO copie conceitos genéricos de `../kb/` — apenas notas do piloto).
- **`tabelas_fisicas[]`**: cada linha mapeia um produto a uma tabela física.

Para cada linha de tabela física:
- **Bronze**: use `fonte_origem` (texto livre) para descrever a fonte.
- **Silver/Gold**: use `lineage` (lista de nomes de tabelas que alimentam).

### 3. Atualizar index.yaml

```yaml
tem_mapeamento_tecnico: true
```

### 4. Validar

```bash
python3 scripts/validate_catalogo.py
```

---

## Como adicionar DDL + simulador de dados a um subdomínio?

Quando um subdomínio ganha uma passada de **schema físico + DDL + simulação**, siga este fluxo:

### 1. Preparar a subpasta

```bash
mkdir -p catalogo/<slug>/schema-fisico
```

### 2. Definir as colunas

Copie o template e edite com as colunas reais de cada tabela:

```bash
cp catalogo/_schema/schema-fisico.template.yaml catalogo/<slug>/schema-fisico/schema-fisico.yaml
# Edite catalogo/<slug>/schema-fisico/schema-fisico.yaml
# - Liste todas as tabelas físicas já documentadas em mapeamento-tecnico.yaml
# - Para cada tabela: nome, camada_medalhao, colunas (nome, tipo, nullable, descrição, PK/FK)
```

O arquivo tem `# yaml-language-server: $schema=../../_schema/schema-fisico.schema.json` no topo. Num editor com suporte a YAML Schema (ex: VSCode + YAML extension), editar o arquivo oferece autocomplete em tempo real e valida contra o contrato.

### 3. Escrever a lógica de simulação

Crie `catalogo/<slug>/schema-fisico/simulate.py` com uma função `generate(n)`:

```python
def generate(n: int) -> Dict[str, List[dict]]:
    """
    Gera n registros simulados.
    
    Retorna um dict: {nome_tabela: [linhas]}
    
    Nomes de tabela devem corresponder aos definidos em schema-fisico.yaml
    (ex: "bronze.purchases__credit_approved", não "bronze_purchases__credit_approved").
    """
    data = {
        "bronze.tabela1": [],
        "silver_l1.tabela2": [],
        "silver_l2.tabela3": [],
        "gold.tabela4": [],
    }
    
    # Sua lógica de negócio aqui
    for i in range(n):
        data["bronze.tabela1"].append({...})
        # ...
    
    return data
```

Referência: [`catalogo/compras-autorizacao/schema-fisico/simulate.py`](../../compras-autorizacao/schema-fisico/simulate.py).

### 4. Gerar DDL

```bash
python3 scripts/ddl_generator.py <slug>
```

Cria `catalogo/<slug>/schema-fisico/ddl.sql` com as `CREATE TABLE` statements (dialeto SQLite, com tipos, PK, FK, NOT NULL).

### 5. Popular com dados simulados

```bash
python3 scripts/simulate_data.py --subdominio <slug> --n 50
```

Cria `catalogo/<slug>/schema-fisico/mock.db` com:
- Banco SQLite com schema do `ddl.sql` aplicado
- N registros inseridos respeitando ordem de camadas (Bronze → Silver → Gold)
- Resumo de linhas por tabela

### 6. Validar

```bash
python3 scripts/validate_catalogo.py
```

Confirma que `schema-fisico.yaml` está válido e consistente com `mapeamento-tecnico.yaml`.

---

## O que fazer quando o contrato muda?

Exemplo: suponha que resolvemos que todo produto precisa ter um campo `owner_email` obrigatório (hoje não existe).

### 1. Editar o schema

Abra `catalogo.schema.json` e adicione `owner_email` à lista `required`:

```json
{
  "type": "object",
  "required": ["camada", "nome", "descricao", "consumidores", "dono", "status", "owner_email"],
  "properties": {
    "owner_email": {
      "type": "string",
      "format": "email"
    }
  }
}
```

### 2. Rodar validador

```bash
python3 scripts/validate_catalogo.py
```

Ele aponta: "catalogo/elegibilidade/catalogo.yaml: 'owner_email' is a required property".

### 3. Corrigir os arquivos

Você vê exatamente quais 15 arquivos precisam do novo campo e por quê.

### 4. Commit do contrato + dados

Um commit com "Adicionar owner_email obrigatório ao contrato + atualizar todos os produtos" documenta a mudança e sua razão no git log.

---

## Regras adicionais (fora do JSON Schema)

O validador Python (`scripts/validate_catalogo.py`) também confere:

1. **Coerência de slugs**: todo slug em `index.yaml` tem pasta correspondente em `catalogo/`, e vice-versa.
2. **Mapeamento técnico**: se `index.yaml` diz que um subdomínio `tem_mapeamento_tecnico: true`, o arquivo deve existir (e vice-versa).
3. **Prefixos**: nome do produto com prefixo correto (`core_`, `integration_`, `analytics_`) e prefixo de tabela física corresponde a camada medalhão (`bronze.`, `silver.`, `gold.`).
4. **Unicidade**: nenhum nome de produto é duplicado em dois subdomínios diferentes.
5. **Avisos**: produtos no mapeamento técnico que não existem no `catalogo.yaml` geram aviso (não erro) — é proposital para "insumo interno".

---

## Boas práticas

1. **Sempre use os templates** — eles já trazem a estrutura correta e o comentário `$schema`.
2. **Rode o validador antes de commitear** — economiza volta depois.
3. **Se o editor não mostra erros**: reinicie o editor ou verifique que a extensão YAML está ativa (VSCode).
4. **Não altere o nome do slug após criado** — é a chave que liga o índice à pasta. Se precisar, atualize em 3 lugares: pasta, `nome` em `catalogo.yaml`, e `slug` em `index.yaml`.
5. **Notas do mapeamento técnico**: documentar apenas o que é específico daquele piloto/subdomínio. Conceitos genéricos (Silver L1/L2, convenção inglês/português, etc) estão em `kb/`.

---

## Exemplo: ciclo completo

```bash
# 1. Criar novo subdomínio "Investimentos"
mkdir catalogo/investimentos
cp catalogo/_schema/catalogo.template.yaml catalogo/investimentos/catalogo.yaml

# 2. Editar catalogo/investimentos/catalogo.yaml (editor valida em tempo real)

# 3. Adicionar a index.yaml:
# - nome: "Investimentos"
#   slug: "investimentos"
#   ...

# 4. Validar
python3 scripts/validate_catalogo.py
# ✓ Validação completa! — 16 subdomínios, 60 produtos

# 5. Commit
git add catalogo/ && git commit -m "Adicionar subdomínio Investimentos com 5 produtos"
```

---

## Troubleshooting

**P: Editei um arquivo, mas o editor não mostra erros do schema.**
R: Verifique que o comentário `# yaml-language-server: $schema=...` está no topo do arquivo. Se ainda não funcionar, reinicie o editor (VSCode especialmente).

**P: Validador diz que "prefixo está errado", mas eu acho que está certo.**
R: Lembre: `core_`, `integration_`, `analytics_` (lowercase, com underscore). "Core" → "core_", não "Core_".

**P: Posso ter dois produtos com nomes iguais em subdomínios diferentes?**
R: Não. Nomes de produtos são globais no catálogo. Se dois subdomínios precisam de um mesmo conceito, use nomes diferentes (ex: `core_transacao_credito` vs `core_transacao_investimento`).

**P: Como desfaço uma mudança no contrato?**
R: Git. `git log catalogo/_schema/catalogo.schema.json` mostra histórico, `git show <hash>` mostra o que mudou, `git revert <hash>` desfaz. Depois, rodeia validador e corrige os arquivos conforme a mudança anterior.
