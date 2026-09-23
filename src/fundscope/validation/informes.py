import pandas as pd

from fundscope.validation.schema import validar_colunas

COLUNAS_OBRIGATORIAS = {
    "CNPJ_FUNDO_CLASSE",
    "DT_COMPTC",
    "VL_QUOTA",
    "VL_PATRIM_LIQ",
}


def validar_informes(df: pd.DataFrame) -> None:
    """Valida os requisitos mínimos dos informes da CVM."""

    validar_colunas(
        df.columns,
        COLUNAS_OBRIGATORIAS,
    )

    if df.empty:
        raise ValueError("O arquivo de informes esta vazio.")


def contar_duplicados(df: pd.DataFrame) -> int:
    """Retorna a quantidade de registros duplicados."""
    return int(df.duplicated().sum())
