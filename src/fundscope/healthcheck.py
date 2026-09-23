import os

import psycopg


def main() -> None:
    with (
        psycopg.connect(
            host=os.environ["POSTGRES_HOST"],
            port=5432,
            dbname=os.environ["POSTGRES_DB"],
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
            connect_timeout=5,
            options="-c statement_timeout=5000",
        ) as connection,
        connection.cursor() as cursor,
    ):
        cursor.execute("SELECT schema_name FROM information_schema.schemata")
        schemas = {row[0] for row in cursor.fetchall()}

    faltantes = {"silver", "gold", "metadata"} - schemas

    if faltantes:
        raise RuntimeError(f"Schemas ausentes: {', '.join(sorted(faltantes))}")

    print("OK: PostgreSQL acessivel e schemas obrigatorios presentes.")


if __name__ == "__main__":
    main()
