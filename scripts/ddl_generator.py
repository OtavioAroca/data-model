#!/usr/bin/env python3

import sys
import yaml
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
CATALOG_DIR = REPO_ROOT / "catalog"

def generate_ddl(subdominio_slug):
    """Gera DDL SQL a partir de schema-fisico.yaml"""

    schema_file = CATALOG_DIR / subdominio_slug / "schema-fisico" / "schema-fisico.yaml"
    if not schema_file.exists():
        print(f"Erro: {schema_file} não encontrado", file=sys.stderr)
        sys.exit(1)

    with open(schema_file) as f:
        schema = yaml.safe_load(f)

    ddl_statements = []

    for tabela in schema.get("tabelas", []):
        nome = tabela["nome"]
        # SQLite não suporta esquemas, converter bronze.purchases__x para bronze_purchases__x
        nome_sql = nome.replace(".", "_")
        colunas_def = []
        pk_cols = []

        for col in tabela.get("colunas", []):
            col_name = col["nome"]
            col_type = col["tipo"]
            nullable = col.get("nullable", True)

            col_def = f"  {col_name} {col_type}"

            if not nullable:
                col_def += " NOT NULL"

            # Coletar PKs para constraint composta (se houver múltiplas)
            if col.get("chave_primaria", False):
                pk_cols.append(col_name)
                # Só adicionar PRIMARY KEY inline se for a única PK
                if len([c for c in tabela.get("colunas", []) if c.get("chave_primaria")]) == 1:
                    col_def += " PRIMARY KEY"

            if "chave_estrangeira" in col:
                fk = col["chave_estrangeira"]
                col_def += f" REFERENCES {fk['tabela'].replace('.', '_')}({fk['coluna']})"

            colunas_def.append(col_def)

        # Se houver múltiplas PKs, adicionar constraint composta
        if len(pk_cols) > 1:
            colunas_def.append(f"  PRIMARY KEY ({', '.join(pk_cols)})")

        create_stmt = f"CREATE TABLE {nome_sql} (\n"
        create_stmt += ",\n".join(colunas_def)
        create_stmt += "\n);"

        ddl_statements.append(create_stmt)

    return "\n\n".join(ddl_statements)

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 ddl_generator.py <subdominio-slug>")
        print("Exemplo: python3 ddl_generator.py compras-autorizacao")
        sys.exit(1)

    subdominio = sys.argv[1]
    ddl = generate_ddl(subdominio)

    # Salvar em arquivo
    output_file = CATALOG_DIR / subdominio / "schema-fisico" / "ddl.sql"
    with open(output_file, "w") as f:
        f.write(ddl)

    print(f"✓ DDL gerado: {output_file}")

if __name__ == "__main__":
    main()
