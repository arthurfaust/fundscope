import pytest

from fundscope import pipeline

CABECALHO = "CNPJ_FUNDO_CLASSE;DT_COMPTC;VL_QUOTA;VL_PATRIM_LIQ"


@pytest.fixture
def carga_simulada(monkeypatch):
    """Substitui a carga no PostgreSQL e guarda o que seria carregado."""
    carregados = []

    def carregar(df):
        carregados.append(df)
        return len(df)

    monkeypatch.setattr(pipeline, "carregar_informes", carregar)
    return carregados


def _csv(tmp_path, linhas):
    arquivo = tmp_path / "inf_diario.csv"
    arquivo.write_text("\n".join([CABECALHO, *linhas]), encoding="latin1")
    return arquivo


def test_processa_arquivo_e_informa_descartados(tmp_path, carga_simulada, capsys):
    arquivo = _csv(
        tmp_path,
        [
            "12.345.678/0001-99;2026-09-01;1.5;1000",
            "12.345.678/0001-99;2026-09-01;1.5;1000",
            "-;2026-09-01;1.5;1000",
            "11.111.111/0001-11;data-invalida;1.5;1000",
        ],
    )

    quantidade = pipeline.processar_arquivo(arquivo)

    assert quantidade == 1
    assert len(carga_simulada[0]) == 1
    assert "1 registros validos, 3 descartados" in capsys.readouterr().out


def test_sem_descartes(tmp_path, carga_simulada, capsys):
    arquivo = _csv(tmp_path, ["12.345.678/0001-99;2026-09-01;1.5;1000"])

    pipeline.processar_arquivo(arquivo)

    assert "1 registros validos, 0 descartados" in capsys.readouterr().out


def test_arquivo_inexistente(tmp_path, carga_simulada):
    with pytest.raises(FileNotFoundError, match="Arquivo nao encontrado"):
        pipeline.processar_arquivo(tmp_path / "nao-existe.csv")

    assert carga_simulada == []
