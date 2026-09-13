#!/usr/bin/env python3

import sys
import sqlite3
import argparse
import importlib.util
import yaml
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
CATALOGO_DIR = REPO_ROOT / "catalogo"

def load_simulator(subdominio_slug):
    """Importa dynamicamente catalogo/<slug>/schema-fisico/simulate.py"""

    simulate_file = CATALOGO_DIR / subdominio_slug / "schema-fisico" / "simulate.py"
    if not simulate_file.exists():
        print(f"Erro: {simulate_file} não encontrado", file=sys.stderr)
        sys.exit(1)

    spec = importlib.util.spec_from_file_location("simulate", simulate_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if not hasattr(module, "generate"):
        print(f"Erro: {simulate_file} deve implementar função generate(n)", file=sys.stderr)
        sys.exit(1)

    return module

def load_schema(subdominio_slug):
    """Carrega schema-fisico.yaml e retorna mapa de colunas por tabela"""

    schema_file = CATALOGO_DIR / subdominio_slug / "schema-fisico" / "schema-fisico.yaml"
    if not schema_file.exists():
        return {}

    with open(schema_file) as f:
        schema = yaml.safe_load(f)

    # Mapa: nome_tabela_original → set de colunas
    columns_map = {}
    for tabela in schema.get("tabelas", []):
        nome_original = tabela["nome"]
        colunas = {col["nome"] for col in tabela.get("colunas", [])}
        columns_map[nome_original] = colunas

    return columns_map

def create_database(subdominio_slug, db_file):
    """Cria banco a partir do DDL gerado"""

    ddl_file = CATALOGO_DIR / subdominio_slug / "schema-fisico" / "ddl.sql"
    if not ddl_file.exists():
        print(f"Erro: {ddl_file} não encontrado (rode ddl_generator.py primeiro)", file=sys.stderr)
        sys.exit(1)

    with open(ddl_file) as f:
        ddl = f.read()

    conn = sqlite3.connect(db_file)
    conn.executescript(ddl)
    conn.commit()

    return conn

def insert_data(conn, table_data, schema_columns):
    """Insere dados nas tabelas, filtrando colunas conforme o schema"""

    layer_order = ["bronze", "silver_l1", "silver_l2", "silver", "gold"]
    tables_by_layer = {}

    for table_name in table_data.keys():
        # Converter nome: bronze.purchases__x → bronze_purchases__x (SQLite format)
        table_name_sql = table_name.replace(".", "_")
        layer = table_name.split(".")[0].lower()
        if layer not in tables_by_layer:
            tables_by_layer[layer] = []
        tables_by_layer[layer].append((table_name, table_name_sql))

    cursor = conn.cursor()
    total_inserted = {}

    for layer in layer_order:
        if layer not in tables_by_layer:
            continue

        for table_name, table_name_sql in tables_by_layer[layer]:
            rows = table_data[table_name]

            if not rows:
                total_inserted[table_name] = 0
                continue

            # Filtrar colunas existentes no schema
            all_keys = set(rows[0].keys())
            allowed_columns = schema_columns.get(table_name, all_keys)
            columns = [k for k in rows[0].keys() if k in allowed_columns]

            if not columns:
                total_inserted[table_name] = 0
                continue

            placeholders = ", ".join(["?"] * len(columns))
            insert_sql = f"INSERT INTO {table_name_sql} ({', '.join(columns)}) VALUES ({placeholders})"

            for row in rows:
                values = [row.get(col) for col in columns]
                cursor.execute(insert_sql, values)

            total_inserted[table_name] = len(rows)

    conn.commit()
    return total_inserted

def main():
    parser = argparse.ArgumentParser(description="Simula dados para um subdomínio")
    parser.add_argument("--subdominio", required=True, help="Slug do subdomínio (ex: compras-autorizacao)")
    parser.add_argument("--n", type=int, default=50, help="Número de eventos/compras a simular")

    args = parser.parse_args()

    # Carregar simulador
    print(f"Carregando simulador para {args.subdominio}...")
    simulator = load_simulator(args.subdominio)

    # Gerar dados
    print(f"Gerando {args.n} registros...")
    table_data = simulator.generate(args.n)

    # Criar banco
    db_file = CATALOGO_DIR / args.subdominio / "schema-fisico" / "mock.db"
    print(f"Criando banco: {db_file}")
    conn = create_database(args.subdominio, db_file)

    # Inserir dados
    print("Inserindo dados...")
    schema_columns = load_schema(args.subdominio)
    totals = insert_data(conn, table_data, schema_columns)

    conn.close()

    # Resumo
    print(f"\n✓ Sucesso! Banco criado em {db_file}")
    print("\nResumo de linhas por tabela:")

    # Agrupar por camada
    by_layer = {}
    for table_name, count in sorted(totals.items()):
        layer = table_name.split(".")[0]
        if layer not in by_layer:
            by_layer[layer] = []
        if count > 0:
            by_layer[layer].append((table_name, count))

    for layer in ["bronze", "silver_l1", "silver_l2", "silver", "gold"]:
        if layer in by_layer:
            total_in_layer = sum(c for _, c in by_layer[layer])
            print(f"\n{layer.upper()}: {total_in_layer} linhas")
            for table_name, count in sorted(by_layer[layer]):
                print(f"  {table_name:<50} {count:>5}")

if __name__ == "__main__":
    main()
