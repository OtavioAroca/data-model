#!/usr/bin/env python3

import sys
import json
import yaml
from pathlib import Path
import jsonschema

REPO_ROOT = Path(__file__).parent.parent
CATALOGO_DIR = REPO_ROOT / "catalogo"
SCHEMA_DIR = CATALOGO_DIR / "_schema"

def load_schema(name):
    with open(SCHEMA_DIR / f"{name}.schema.json") as f:
        return json.load(f)

def validate_file(filepath, schema):
    with open(filepath) as f:
        data = yaml.safe_load(f)

    try:
        jsonschema.validate(instance=data, schema=schema)
        return True, None
    except jsonschema.ValidationError as e:
        return False, str(e)

def main():
    errors = []
    warnings = []

    # Schemas
    catalogo_schema = load_schema("catalogo")
    mapeamento_schema = load_schema("mapeamento-tecnico")
    index_schema = load_schema("index")

    # Validar index.yaml
    print("Validando catalogo/index.yaml...", end=" ")
    valid, err = validate_file(CATALOGO_DIR / "index.yaml", index_schema)
    if valid:
        print("✓")
    else:
        print("✗")
        errors.append(f"catalogo/index.yaml: {err}")

    # Carregar index para referência cruzada
    with open(CATALOGO_DIR / "index.yaml") as f:
        index_data = yaml.safe_load(f)

    index_slugs = {s["slug"] for s in index_data["subdominios"]}
    index_has_mapeamento = {s["slug"]: s["tem_mapeamento_tecnico"] for s in index_data["subdominios"]}

    # Validar cada subdomínio
    all_products = {}  # Para checar duplicatas

    for subdir in sorted(CATALOGO_DIR.iterdir()):
        if not subdir.is_dir() or subdir.name.startswith("_"):
            continue

        slug = subdir.name

        # Checar se está no índice
        if slug not in index_slugs:
            errors.append(f"Pasta catalogo/{slug}/ não está listada em index.yaml")
            continue

        # Validar catalogo.yaml
        catalogo_file = subdir / "catalogo.yaml"
        if not catalogo_file.exists():
            errors.append(f"catalogo/{slug}/catalogo.yaml não existe")
            continue

        print(f"Validando catalogo/{slug}/catalogo.yaml...", end=" ")
        valid, err = validate_file(catalogo_file, catalogo_schema)
        if valid:
            print("✓")

            # Verificar prefixos de produto
            with open(catalogo_file) as f:
                sub_data = yaml.safe_load(f)

            for prod in sub_data.get("produtos", []):
                nome = prod["nome"]
                camada = prod["camada"]

                # Prefixo deve corresponder à camada
                expected_prefix = f"{camada.lower().replace(' ', '_')}_"
                if camada == "Analytics":
                    expected_prefix = "analytics_"
                elif camada == "Integration":
                    expected_prefix = "integration_"
                else:  # Core
                    expected_prefix = "core_"

                if not nome.startswith(expected_prefix):
                    errors.append(f"catalogo/{slug}/catalogo.yaml: produto '{nome}' tem prefixo errado (esperado: {expected_prefix})")

                # Checar duplicatas
                if nome in all_products:
                    errors.append(f"Produto '{nome}' é duplicado em {slug} e {all_products[nome]}")
                else:
                    all_products[nome] = slug
        else:
            print("✗")
            errors.append(f"catalogo/{slug}/catalogo.yaml: {err}")

        # Validar mapeamento-tecnico.yaml se existir
        mapeamento_file = subdir / "mapeamento-tecnico.yaml"
        if mapeamento_file.exists():
            print(f"Validando catalogo/{slug}/mapeamento-tecnico.yaml...", end=" ")
            valid, err = validate_file(mapeamento_file, mapeamento_schema)
            if valid:
                print("✓")

                # Verificar que tabela_fisica corresponde a camada_medalhao
                with open(mapeamento_file) as f:
                    mapeamento_data = yaml.safe_load(f)

                for tabela in mapeamento_data.get("tabelas_fisicas", []):
                    tabela_fisica = tabela["tabela_fisica"]
                    camada_medalhao = tabela["camada_medalhao"]

                    # Bronze, Silver, Silver L1, Silver L2, Gold
                    expected_prefix = camada_medalhao.lower().replace(" ", "_")
                    if not tabela_fisica.startswith(expected_prefix + "."):
                        errors.append(f"catalogo/{slug}/mapeamento-tecnico.yaml: tabela '{tabela_fisica}' deveria começar com '{expected_prefix}.'")

                    # Verificar que produto existe no catalogo.yaml
                    if catalogo_file.exists():
                        with open(catalogo_file) as f:
                            sub_data = yaml.safe_load(f)

                        produto_nomes = {p["nome"] for p in sub_data.get("produtos", [])}
                        if tabela["produto"] not in produto_nomes:
                            # Aviso, não erro (pode ser insumo interno)
                            warnings.append(f"catalogo/{slug}/mapeamento-tecnico.yaml: produto '{tabela['produto']}' não existe em catalogo.yaml (pode ser insumo interno)")
            else:
                print("✗")
                errors.append(f"catalogo/{slug}/mapeamento-tecnico.yaml: {err}")

        # Checar correspondência com index.yaml
        if index_has_mapeamento[slug]:
            if not mapeamento_file.exists():
                errors.append(f"index.yaml diz que {slug} tem mapeamento técnico, mas {mapeamento_file} não existe")
        else:
            if mapeamento_file.exists():
                errors.append(f"index.yaml diz que {slug} NÃO tem mapeamento técnico, mas {mapeamento_file} existe")

    # Checar pastas órfãs
    for slug in index_slugs:
        if not (CATALOGO_DIR / slug).exists():
            errors.append(f"index.yaml lista {slug}, mas pasta catalogo/{slug}/ não existe")

    # Print warnings
    if warnings:
        print(f"\n⚠ Avisos ({len(warnings)}):")
        for w in warnings:
            print(f"  {w}")

    # Print errors
    if errors:
        print(f"\n✗ Erros ({len(errors)}):")
        for e in errors:
            print(f"  {e}")
        return 1

    print("\n✓ Validação completa!")
    print(f"  - {len(index_slugs)} subdomínios")
    print(f"  - {len(all_products)} produtos únicos")
    print(f"  - {sum(1 for s in index_data['subdominios'] if s['tem_mapeamento_tecnico'])} com mapeamento técnico")
    return 0

if __name__ == "__main__":
    sys.exit(main())
