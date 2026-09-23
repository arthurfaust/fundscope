import pandas as pd

COLUNAS_NUMERICAS = [
    "VL_QUOTA",
    "VL_PATRIM_LIQ",
]


def transformar_informes(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Limpa e padroniza os informes da CVM."""

    resultado = df.copy()

    # Padroniza nomes das colunas
    resultado.columns = [coluna.strip().upper() for coluna in resultado.columns]

    # Normaliza CNPJ
    resultado["CNPJ_FUNDO_CLASSE"] = (
        resultado["CNPJ_FUNDO_CLASSE"].astype(str).str.replace(r"\D", "", regex=True)
    )

    # Converte data
    resultado["DT_COMPTC"] = pd.to_datetime(
        resultado["DT_COMPTC"],
        errors="coerce",
    )

    # Converte valores numéricos
    for coluna in COLUNAS_NUMERICAS:
        resultado[coluna] = pd.to_numeric(
            resultado[coluna],
            errors="coerce",
        )

    # Remove registros sem informações essenciais
    resultado = resultado.dropna(
        subset=[
            "CNPJ_FUNDO_CLASSE",
            "DT_COMPTC",
        ]
    )

    # Remove duplicados
    resultado = resultado.drop_duplicates()

    return resultado
