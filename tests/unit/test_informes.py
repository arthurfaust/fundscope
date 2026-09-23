import pandas as pd
import pytest

from fundscope.validation.informes import (
    contar_duplicados,
    validar_informes,
)

COLUNAS = [
    "CNPJ_FUNDO_CLASSE",
    "DT_COMPTC",
    "VL_QUOTA",
    "VL_PATRIM_LIQ",
]


def test_validar_informes_valido():
    df = pd.DataFrame(
        [
            {
                "CNPJ_FUNDO_CLASSE": "12345678000199",
                "DT_COMPTC": "2026-09-01",
                "VL_QUOTA": 1.23,
                "VL_PATRIM_LIQ": 1000000,
            }
        ]
    )

    validar_informes(df)


def test_validar_informes_vazio():
    df = pd.DataFrame(columns=COLUNAS)

    with pytest.raises(
        ValueError,
        match="arquivo de informes esta vazio",
    ):
        validar_informes(df)


def test_validar_informes_coluna_ausente():
    df = pd.DataFrame(
        [
            {
                "CNPJ_FUNDO_CLASSE": "12345678000199",
                "DT_COMPTC": "2026-09-01",
            }
        ]
    )

    with pytest.raises(
        ValueError,
        match="Colunas obrigatórias ausentes",
    ):
        validar_informes(df)


def test_contar_duplicados():
    df = pd.DataFrame(
        {
            "valor": [1, 1, 2],
        }
    )

    assert contar_duplicados(df) == 1
