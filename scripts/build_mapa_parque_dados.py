#!/usr/bin/env python3
"""
Build script: gera presentation/parque-de-dados.html a partir dos YAMLs do catálogo.

Ferramenta nova e independente da antiga apresentação (ver docs/adr/0002).
Cobre em detalhe (tabelas, colunas, tipos, lineage, relações estruturais) só o
subdomínio Compras/Autorização, único com schema físico definido — ver
docs/adr/0001 e docs/adr/0006.

Lê:
  catalog/index.yaml
  catalog/<slug>/mapeamento-tecnico.yaml (subdomínios com schema físico)
  catalog/<slug>/schema-fisico/schema-fisico.yaml (subdomínios com schema físico)
Escreve:
  presentation/parque-de-dados.html (injetando DATA no template)
"""

import json
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).parent.parent
CATALOG_DIR = REPO_ROOT / "catalog"
PRESENTATION_DIR = REPO_ROOT / "presentation"
TEMPLATE_PATH = PRESENTATION_DIR / "parque-de-dados.template.html"
OUTPUT_PATH = PRESENTATION_DIR / "parque-de-dados.html"


def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)


def load_subdominios_com_schema_fisico(index_data):
    """Subdomínios com schema-fisico.yaml presente, na ordem do index.yaml."""
    slugs = []
    for sub in index_data["subdominios"]:
        schema_path = CATALOG_DIR / sub["slug"] / "schema-fisico" / "schema-fisico.yaml"
        if schema_path.exists():
            slugs.append(sub["slug"])
    return slugs


def build_mapa_detalhado(slug):
    """Monta tabelas + colunas + lineage + relações para um subdomínio com schema físico."""
    mapeamento_path = CATALOG_DIR / slug / "mapeamento-tecnico.yaml"
    schema_path = CATALOG_DIR / slug / "schema-fisico" / "schema-fisico.yaml"

    mapeamento = load_yaml(mapeamento_path)
    schema_fisico = load_yaml(schema_path)

    tabelas_tecnicas = mapeamento.get("tabelas_fisicas", [])
    tabelas_colunas = {t["nome"]: t for t in schema_fisico.get("tabelas", [])}

    tabelas = []
    for tt in tabelas_tecnicas:
        nome_tab = tt["tabela_fisica"]
        colunas_info = tabelas_colunas.get(nome_tab, {})
        tabelas.append({
            "nome": nome_tab,
            "camada_medalhao": tt["camada_medalhao"],
            "produto": tt.get("produto", ""),
            "camada_produto": tt.get("camada_produto", ""),
            "papel": tt.get("papel", ""),
            "pipeline": tt.get("pipeline", ""),
            "frequencia": tt.get("frequencia", ""),
            "fonte_origem": tt.get("fonte_origem", ""),
            "colunas": colunas_info.get("colunas", []),
            "lineage_upstream": tt.get("lineage", []),
            "lineage_downstream": [],
        })

    nomes_definidos = {t["nome"] for t in tabelas}

    # lineage reverso
    lineage_map = {}
    for t in tabelas:
        for upstream in t["lineage_upstream"]:
            lineage_map.setdefault(upstream, []).append(t["nome"])
    for t in tabelas:
        t["lineage_downstream"] = lineage_map.get(t["nome"], [])

    # tabelas referenciadas em lineage mas sem schema físico (de outro subdomínio)
    referenciadas = set()
    for t in tabelas:
        referenciadas.update(t["lineage_upstream"])
    tabelas_externas_lineage = sorted(referenciadas - nomes_definidos)

    # relações estruturais (FK), lidas de chave_estrangeira
    relacoes = []
    for t in tabelas:
        for col in t["colunas"]:
            fk = col.get("chave_estrangeira")
            if fk:
                relacoes.append({
                    "tabela_origem": t["nome"],
                    "coluna_origem": col["nome"],
                    "tabela_destino": fk["tabela"],
                    "coluna_destino": fk["coluna"],
                })

    return {
        "slug": slug,
        "contexto": mapeamento.get("contexto", ""),
        "notas": mapeamento.get("notas", []),
        "tabelas": tabelas,
        "tabelas_externas_lineage": tabelas_externas_lineage,
        "relacoes": relacoes,
    }


def build_data():
    index_data = load_yaml(CATALOG_DIR / "index.yaml")
    slugs_detalhados = load_subdominios_com_schema_fisico(index_data)

    mapas_detalhados = [build_mapa_detalhado(slug) for slug in slugs_detalhados]

    return {
        "meta": {
            "gerado_por": "scripts/build_mapa_parque_dados.py",
            "fonte": "catalog/",
        },
        "mapas_detalhados": mapas_detalhados,
    }


def main():
    print("Gerando mapa do parque de dados...")

    if not TEMPLATE_PATH.exists():
        print(f"Template não encontrado: {TEMPLATE_PATH}")
        sys.exit(1)

    data = build_data()
    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    marker = "/*__PARQUE_DE_DADOS_DATA__*/"
    if marker not in template:
        print(f"Marcador '{marker}' não encontrado no template.")
        sys.exit(1)

    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    output = template.replace(marker, f"const DATA = {json_str};")

    OUTPUT_PATH.write_text(output, encoding="utf-8")

    print(f"\nGerado: {OUTPUT_PATH}")
    for mapa in data["mapas_detalhados"]:
        print(f"  - {mapa['slug']}: {len(mapa['tabelas'])} tabelas, "
              f"{len(mapa['relacoes'])} relações, "
              f"{sum(len(t['lineage_upstream']) for t in mapa['tabelas'])} arestas de lineage, "
              f"{len(mapa['tabelas_externas_lineage'])} tabelas externas (lineage)")


if __name__ == "__main__":
    main()
