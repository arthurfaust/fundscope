import pandas as pd

from fundscope.transform.informes import transformar_informes


def _informes(cnpjs: list[object]) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "CNPJ_FUNDO_CLASSE": cnpjs,
            "DT_COMPTC": ["2026-09-01"] * len(cnpjs),
            "VL_QUOTA": ["1.5"] * len(cnpjs),
            "VL_PATRIM_LIQ": ["1000"] * len(cnpjs),
        }
    )


def test_normaliza_cnpj_removendo_pontuacao():
    resultado = transformar_informes(_informes(["12.345.678/0001-99"]))

    assert resultado["CNPJ_FUNDO_CLASSE"].tolist() == ["12345678000199"]


def test_descarta_cnpj_sem_digitos():
    resultado = transformar_informes(_informes(["12.345.678/0001-99", "-"]))

    assert resultado["CNPJ_FUNDO_CLASSE"].tolist() == ["12345678000199"]


def test_descarta_cnpj_com_tamanho_invalido():
    resultado = transformar_informes(
        _informes(["12.345.678/0001-99", "123", "123456789012345"])
    )

    assert resultado["CNPJ_FUNDO_CLASSE"].tolist() == ["12345678000199"]


def test_padroniza_nomes_e_converte_tipos():
    df = _informes(["12345678000199"]).rename(columns={"VL_QUOTA": " vl_quota "})

    resultado = transformar_informes(df)

    assert "VL_QUOTA" in resultado.columns
    assert resultado["VL_QUOTA"].iloc[0] == 1.5
    assert resultado["DT_COMPTC"].iloc[0] == pd.Timestamp("2026-09-01")


def test_remove_duplicados_e_datas_invalidas():
    df = pd.concat([_informes(["12345678000199"] * 2), _informes(["12345678000199"])])
    df.iloc[2, df.columns.get_loc("DT_COMPTC")] = "data-invalida"

    resultado = transformar_informes(df)

    assert len(resultado) == 1
