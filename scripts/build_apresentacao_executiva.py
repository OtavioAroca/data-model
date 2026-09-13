#!/usr/bin/env python3
"""
Build script: gera presentation/apresentacao-executiva.html a partir de
catalog/index.yaml.

Ferramenta separada do mapa do parque de dados (ver docs/adr/0008) — cobre a
forma de modelar (DDD, Camada Medalhão, Core/Integration/Analytics),
benefícios e um estudo de caso (Compras/Autorização), este último linkando
presentation/parque-de-dados.html em vez de reconstruir o diagrama.

Lê:
  catalog/index.yaml
Escreve:
  presentation/apresentacao-executiva.html (injetando DATA no template)
"""

import json
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).parent.parent
CATALOG_DIR = REPO_ROOT / "catalog"
PRESENTATION_DIR = REPO_ROOT / "presentation"
TEMPLATE_PATH = PRESENTATION_DIR / "apresentacao-executiva.template.html"
OUTPUT_PATH = PRESENTATION_DIR / "apresentacao-executiva.html"


def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)


def load_camadas_produto(slug):
    """Camadas (Core/Integration/Analytics) com produto proposto no catalog.yaml do subdomínio."""
    catalog_path = CATALOG_DIR / slug / "catalog.yaml"
    if not catalog_path.exists():
        return []
    catalog = load_yaml(catalog_path)
    camadas = {p["camada"] for p in catalog.get("produtos", [])}
    ordem = ["Core", "Integration", "Analytics"]
    return [c for c in ordem if c in camadas]


def build_data():
    index_data = load_yaml(CATALOG_DIR / "index.yaml")

    subdominios = [
        {
            "nome": sub["nome"],
            "slug": sub["slug"],
            "bounded_context": sub["bounded_context"],
            "sistemas_origem": sub["sistemas_origem"],
            "tipo_ddd": sub["tipo_ddd"],
            "tem_mapeamento_tecnico": sub.get("tem_mapeamento_tecnico", False),
            "camadas_produto": load_camadas_produto(sub["slug"]),
        }
        for sub in index_data["subdominios"]
    ]

    return {
        "meta": {
            "gerado_por": "scripts/build_apresentacao_executiva.py",
            "fonte": "catalog/index.yaml",
        },
        "subdominios": subdominios,
    }


def main():
    print("Gerando apresentação executiva...")

    if not TEMPLATE_PATH.exists():
        print(f"Template não encontrado: {TEMPLATE_PATH}")
        sys.exit(1)

    data = build_data()
    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    marker = "/*__APRESENTACAO_EXECUTIVA_DATA__*/"
    if marker not in template:
        print(f"Marcador '{marker}' não encontrado no template.")
        sys.exit(1)

    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    output = template.replace(marker, f"const DATA = {json_str};")

    OUTPUT_PATH.write_text(output, encoding="utf-8")

    contagem_ddd = {}
    for sub in data["subdominios"]:
        contagem_ddd[sub["tipo_ddd"]] = contagem_ddd.get(sub["tipo_ddd"], 0) + 1

    print(f"\nGerado: {OUTPUT_PATH}")
    print(f"  - {len(data['subdominios'])} subdomínios "
          f"({', '.join(f'{v} {k}' for k, v in contagem_ddd.items())})")


if __name__ == "__main__":
    main()
