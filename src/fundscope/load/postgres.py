import os

import pandas as pd
import psycopg


def obter_conexao() -> psycopg.Connection:
    """Cria conexão com o PostgreSQL."""

    return psycopg.connect(
        host=os.environ.get(
            "POSTGRES_HOST",
            "localhost",
        ),
        port=os.environ.get(
            "POSTGRES_PORT",
            "5432",
        ),
        dbname=os.environ.get(
            "POSTGRES_DB",
            "fundscope",
        ),
        user=os.environ.get(
            "POSTGRES_USER",
            "fundscope",
        ),
        password=os.environ.get(
            "POSTGRES_PASSWORD",
            "",
        ),
    )


def criar_tabela() -> None:
    """Cria a tabela Silver utilizada pelo exemplo."""

    sql = """
    CREATE TABLE IF NOT EXISTS silver.informe_diario (
        id BIGSERIAL PRIMARY KEY,

        cnpj_fundo_classe VARCHAR(14) NOT NULL,

        dt_comptc DATE NOT NULL,

        vl_quota NUMERIC(20, 10),

        vl_patrim_liq NUMERIC(20, 2),

        loaded_at TIMESTAMPTZ
            NOT NULL DEFAULT NOW(),

        UNIQUE (
            cnpj_fundo_classe,
            dt_comptc
        )
    );
    """

    with obter_conexao() as conexao, conexao.cursor() as cursor:
        cursor.execute(sql)


def carregar_informes(
    df: pd.DataFrame,
) -> int:
    """Carrega informes tratados na camada Silver."""

    criar_tabela()

    registros = []

    for _, linha in df.iterrows():
        registros.append(
            (
                linha["CNPJ_FUNDO_CLASSE"],
                linha["DT_COMPTC"],
                linha["VL_QUOTA"],
                linha["VL_PATRIM_LIQ"],
            )
        )

    if not registros:
        return 0

    sql = """
    INSERT INTO silver.informe_diario (
        cnpj_fundo_classe,
        dt_comptc,
        vl_quota,
        vl_patrim_liq
    )
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (
        cnpj_fundo_classe,
        dt_comptc
    )
    DO UPDATE SET
        vl_quota = EXCLUDED.vl_quota,
        vl_patrim_liq = EXCLUDED.vl_patrim_liq;
    """

    with obter_conexao() as conexao, conexao.cursor() as cursor:
        cursor.executemany(
            sql,
            registros,
        )

    return len(registros)
