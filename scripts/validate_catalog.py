#!/usr/bin/env python3

import sys
import json
import yaml
from pathlib import Path
import jsonschema

REPO_ROOT = Path(__file__).parent.parent
CATALOG_DIR = REPO_ROOT / "catalog"
SCHEMA_DIR = CATALOG_DIR / "_schema"

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
    catalog_schema = load_schema("catalog")
    mapeamento_schema = load_schema("mapeamento-tecnico")
    index_schema = load_schema("index")
    schema_fisico_schema = load_schema("schema-fisico")

    # Validar index.yaml
    print("Validando catalog/index.yaml...", end=" ")
    valid, err = validate_file(CATALOG_DIR / "index.yaml", index_schema)
    if valid:
        print("✓")
    else:
        print("✗")
        errors.append(f"catalog/index.yaml: {err}")

    # Carregar index para referência cruzada
    with open(CATALOG_DIR / "index.yaml") as f:
        index_data = yaml.safe_load(f)

    index_slugs = {s["slug"] for s in index_data["subdominios"]}
    index_has_mapeamento = {s["slug"]: s["tem_mapeamento_tecnico"] for s in index_data["subdominios"]}

    # Validar cada subdomínio
    all_products = {}  # Para checar duplicatas

    for subdir in sorted(CATALOG_DIR.iterdir()):
        if not subdir.is_dir() or subdir.name.startswith("_"):
            continue

        slug = subdir.name

        # Checar se está no índice
        if slug not in index_slugs:
            errors.append(f"Pasta catalog/{slug}/ não está listada em index.yaml")
            continue

        # Validar catalog.yaml
        catalog_file = subdir / "catalog.yaml"
        if not catalog_file.exists():
            errors.append(f"catalog/{slug}/catalog.yaml não existe")
            continue

        print(f"Validando catalog/{slug}/catalog.yaml...", end=" ")
        valid, err = validate_file(catalog_file, catalog_schema)
        if valid:
            print("✓")

            # Verificar prefixos de produto
            with open(catalog_file) as f:
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
                    errors.append(f"catalog/{slug}/catalog.yaml: produto '{nome}' tem prefixo errado (esperado: {expected_prefix})")

                # Checar duplicatas
                if nome in all_products:
                    errors.append(f"Produto '{nome}' é duplicado em {slug} e {all_products[nome]}")
                else:
                    all_products[nome] = slug
        else:
            print("✗")
            errors.append(f"catalog/{slug}/catalog.yaml: {err}")

        # Validar mapeamento-tecnico.yaml se existir
        mapeamento_file = subdir / "mapeamento-tecnico.yaml"
        if mapeamento_file.exists():
            print(f"Validando catalog/{slug}/mapeamento-tecnico.yaml...", end=" ")
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
                        errors.append(f"catalog/{slug}/mapeamento-tecnico.yaml: tabela '{tabela_fisica}' deveria começar com '{expected_prefix}.'")

                    # Verificar que produto existe no catalog.yaml
                    if catalog_file.exists():
                        with open(catalog_file) as f:
                            sub_data = yaml.safe_load(f)

                        produto_nomes = {p["nome"] for p in sub_data.get("produtos", [])}
                        if tabela["produto"] not in produto_nomes:
                            # Aviso, não erro (pode ser insumo interno)
                            warnings.append(f"catalog/{slug}/mapeamento-tecnico.yaml: produto '{tabela['produto']}' não existe em catalog.yaml (pode ser insumo interno)")
            else:
                print("✗")
                errors.append(f"catalog/{slug}/mapeamento-tecnico.yaml: {err}")

        # Validar schema-fisico/schema-fisico.yaml se existir
        schema_fisico_file = subdir / "schema-fisico" / "schema-fisico.yaml"
        if schema_fisico_file.exists():
            print(f"Validando catalog/{slug}/schema-fisico/schema-fisico.yaml...", end=" ")
            valid, err = validate_file(schema_fisico_file, schema_fisico_schema)
            if valid:
                print("✓")

                with open(schema_fisico_file) as f:
                    schema_fisico_data = yaml.safe_load(f)

                tabelas_por_nome = {t["nome"]: t for t in schema_fisico_data.get("tabelas", [])}

                for tabela in schema_fisico_data.get("tabelas", []):
                    for col in tabela.get("colunas", []):
                        fk = col.get("chave_estrangeira")
                        if not fk:
                            continue

                        prefixo = f"catalog/{slug}/schema-fisico/schema-fisico.yaml: {tabela['nome']}.{col['nome']} (chave_estrangeira)"
                        tabela_ref = tabelas_por_nome.get(fk["tabela"])

                        if tabela_ref is None:
                            errors.append(f"{prefixo}: tabela referenciada '{fk['tabela']}' não existe neste schema-fisico.yaml")
                            continue

                        col_ref = next((c for c in tabela_ref.get("colunas", []) if c["nome"] == fk["coluna"]), None)
                        if col_ref is None:
                            errors.append(f"{prefixo}: coluna referenciada '{fk['tabela']}.{fk['coluna']}' não existe")
                            continue

                        if not col_ref.get("chave_primaria"):
                            errors.append(f"{prefixo}: coluna referenciada '{fk['tabela']}.{fk['coluna']}' não é chave_primaria")
            else:
                print("✗")
                errors.append(f"catalog/{slug}/schema-fisico/schema-fisico.yaml: {err}")

        # Checar correspondência com index.yaml
        if index_has_mapeamento[slug]:
            if not mapeamento_file.exists():
                errors.append(f"index.yaml diz que {slug} tem mapeamento técnico, mas {mapeamento_file} não existe")
        else:
            if mapeamento_file.exists():
                errors.append(f"index.yaml diz que {slug} NÃO tem mapeamento técnico, mas {mapeamento_file} existe")

    # Checar pastas órfãs
    for slug in index_slugs:
        if not (CATALOG_DIR / slug).exists():
            errors.append(f"index.yaml lista {slug}, mas pasta catalog/{slug}/ não existe")

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
