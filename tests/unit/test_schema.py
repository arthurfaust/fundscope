import pytest

from fundscope.validation.schema import validar_colunas


def test_aceita_colunas_obrigatorias():
    validar_colunas(
        colunas=["identificador", "data"],
        obrigatorias=["identificador", "data"],
    )


def test_aceita_colunas_extras_e_ordem_diferente():
    validar_colunas(
        colunas=["valor", "data", "identificador"],
        obrigatorias=["identificador", "data"],
    )


def test_rejeita_coluna_ausente():
    with pytest.raises(
        ValueError,
        match="Colunas obrigatórias ausentes: data",
    ):
        validar_colunas(
            colunas=["identificador"],
            obrigatorias=["identificador", "data"],
        )


def test_rejeita_cabecalho_vazio():
    with pytest.raises(
        ValueError,
        match="Colunas obrigatórias ausentes: data, identificador",
    ):
        validar_colunas(
            colunas=[],
            obrigatorias=["identificador", "data"],
        )
