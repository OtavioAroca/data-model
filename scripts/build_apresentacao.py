#!/usr/bin/env python3
"""
Build script: Gera docs/apresentacao.html a partir dos YAMLs de catálogo e KB.
Lê: catalogo/index.yaml, catalogo/*/catalogo.yaml, mapeamento-tecnico.yaml,
    schema-fisico.yaml, kb/*.md (conteúdo curado à mão).
Escreve: docs/apresentacao.html (injetando DATA no template).
"""

import json
import yaml
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
CATALOGO_DIR = REPO_ROOT / "catalogo"
KB_DIR = REPO_ROOT / "kb"
DOCS_DIR = REPO_ROOT / "docs"

def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)

def load_text(path):
    with open(path) as f:
        return f.read()

def build_data():
    # === Ler catalogo/index.yaml (15 subdomínios) ===
    index = load_yaml(CATALOGO_DIR / "index.yaml")
    subdominios = index["subdominios"]

    # === Enriquecer cada subdomínio com seus produtos (catalogo.yaml) ===
    for sub in subdominios:
        slug = sub["slug"]
        catalogo_yaml = CATALOGO_DIR / slug / "catalogo.yaml"
        if catalogo_yaml.exists():
            cat = load_yaml(catalogo_yaml)
            sub["produtos"] = cat.get("produtos", [])
        else:
            sub["produtos"] = []

    # === Ler compras-autorizacao: mapeamento-tecnico + schema-fisico ===
    map_tecnico_yaml = CATALOGO_DIR / "compras-autorizacao" / "mapeamento-tecnico.yaml"
    schema_fisico_yaml = CATALOGO_DIR / "compras-autorizacao" / "schema-fisico" / "schema-fisico.yaml"

    map_tecnico = load_yaml(map_tecnico_yaml) if map_tecnico_yaml.exists() else {}
    schema_fisico = load_yaml(schema_fisico_yaml) if schema_fisico_yaml.exists() else {}

    notas = map_tecnico.get("notas", [])
    tabelas_tecnicas = map_tecnico.get("tabelas_fisicas", [])
    tabelas_colunas = {t["nome"]: t for t in schema_fisico.get("tabelas", [])}

    # === Merge: tabelas_tecnicas + colunas ===
    tabelas_merged = []
    for tt in tabelas_tecnicas:
        nome_tab = tt.get("tabela_fisica", "")
        colunas_info = tabelas_colunas.get(nome_tab, {})

        merged = {
            "nome": nome_tab,
            "produto": tt.get("produto", ""),
            "camada_produto": tt.get("camada_produto", ""),
            "camada_medalhao": tt.get("camada_medalhao", ""),
            "papel": tt.get("papel", ""),
            "pipeline": tt.get("pipeline", ""),
            "frequencia": tt.get("frequencia", ""),
            "fonte_origem": tt.get("fonte_origem", ""),
            "lineage_upstream": tt.get("lineage", []),
            "colunas": colunas_info.get("colunas", [])
        }
        tabelas_merged.append(merged)

    # === Calcular lineage_downstream (reverso) ===
    lineage_map = {}
    for t in tabelas_merged:
        for upstream in t["lineage_upstream"]:
            if upstream not in lineage_map:
                lineage_map[upstream] = []
            lineage_map[upstream].append(t["nome"])

    for t in tabelas_merged:
        t["lineage_downstream"] = lineage_map.get(t["nome"], [])

    # === Detectar tabelas externas não mapeadas (em lineage mas não em schema-fisico) ===
    tabelas_referenciadas = set()
    for t in tabelas_merged:
        tabelas_referenciadas.add(t["nome"])
        for upstream in t["lineage_upstream"]:
            tabelas_referenciadas.add(upstream)

    tabelas_mapeadas = set(tabelas_colunas.keys())
    tabelas_externas_nao_mapeadas = sorted(tabelas_referenciadas - tabelas_mapeadas)

    # === Inferência de relacionamentos: colunas _id compartilhadas ===
    id_columns = {}
    for t in tabelas_merged:
        for col in t["colunas"]:
            col_name = col.get("nome", "")
            if col_name.endswith("_id") or col_name in ["event_id", "transaction_id"]:
                if col_name not in id_columns:
                    id_columns[col_name] = []
                id_columns[col_name].append(t["nome"])

    relacionamentos_inferidos = [
        {"coluna": col, "tabelas": list(set(tabs))}
        for col, tabs in sorted(id_columns.items())
        if len(tabs) > 1  # só coluna que aparece em >1 tabela
    ]

    # === Conteúdo de conceitos (curado à mão de kb/*.md) ===
    # Extrair conteúdo literalmente de ddd.md, camada-medalhao.md, etc.
    ddd_content = load_text(KB_DIR / "ddd.md")
    medalhao_content = load_text(KB_DIR / "camada-medalhao.md")
    cia_content = load_text(KB_DIR / "core-integration-analytics.md")

    conceitos = {
        "ddd_markdown": ddd_content,
        "medalhao_markdown": medalhao_content,
        "core_integration_analytics_markdown": cia_content,
        # Tabela de desambiguação (editada à mão do kb/README.md, mas já levantada)
        "desambiguacao_core": [
            {
                "conceito": "Core (DDD)",
                "classifica": "Um bounded context do negócio",
                "valores": "Core, Support, Generic",
                "exemplo": "Compras / Autorização = Core (diferencial competitivo)"
            },
            {
                "conceito": "Camada Medalhão",
                "classifica": "Uma tabela física no data lake, por estágio de processamento",
                "valores": "Bronze (raw), Silver (limpo), Gold (pronto)",
                "exemplo": "bronze.purchases__credit_approved → silver_l2.purchases__credit_purchase → gold.integration__purchase_journey"
            },
            {
                "conceito": "Core / Integration / Analytics",
                "classifica": "Um produto de dados, por quantos bounded contexts ele cruza",
                "valores": "Core (1), Integration (>1), Analytics (caso de uso final)",
                "exemplo": "core_credit_purchase (1 contexto) vs integration_purchase_journey (cruza crédito + débito + disputas)"
            }
        ]
    }

    # === Estrutura final DATA ===
    data = {
        "meta": {
            "gerado_em": "build_apresentacao.py",
            "fonte": "kb/ + catalogo/"
        },
        "conceitos": conceitos,
        "subdominios": subdominios,
        "compras_autorizacao": {
            "notas": notas,
            "tabelas": tabelas_merged,
            "tabelas_externas_nao_mapeadas": tabelas_externas_nao_mapeadas,
            "relacionamentos_inferidos": relacionamentos_inferidos
        }
    }

    return data

def main():
    print("🔨 Gerando dados para apresentação...")
    data = build_data()

    # === Ler template ===
    template_path = DOCS_DIR / "apresentacao.template.html"
    if not template_path.exists():
        print(f"❌ Template não encontrado: {template_path}")
        return

    template = load_text(template_path)

    # === Injetar DATA como JSON embutido ===
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    output = template.replace("/*__CARTAO_DATA__*/", f"const DATA = {json_str};")

    # === Escrever arquivo final ===
    output_path = DOCS_DIR / "apresentacao.html"
    output_path.write_text(output, encoding="utf-8")

    # === Resumo de verificação ===
    print(f"\n✅ Sucesso! Arquivo gerado: {output_path}")
    print(f"\n📊 Resumo:")
    print(f"  • Subdomínios: {len(data['subdominios'])}")
    print(f"  • Produtos Compras/Autorização: {len(set(t['produto'] for t in data['compras_autorizacao']['tabelas']))}")
    print(f"  • Tabelas físicas mapeadas: {len(data['compras_autorizacao']['tabelas'])}")
    print(f"  • Tabelas externas não mapeadas: {len(data['compras_autorizacao']['tabelas_externas_nao_mapeadas'])}")
    if data['compras_autorizacao']['tabelas_externas_nao_mapeadas']:
        print(f"    {data['compras_autorizacao']['tabelas_externas_nao_mapeadas']}")
    print(f"  • Relacionamentos inferidos (por coluna _id): {len(data['compras_autorizacao']['relacionamentos_inferidos'])}")

if __name__ == "__main__":
    main()
