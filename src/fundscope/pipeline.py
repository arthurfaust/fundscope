from pathlib import Path

import pandas as pd

from fundscope.load.postgres import carregar_informes
from fundscope.transform.informes import transformar_informes
from fundscope.validation.informes import validar_informes


def processar_arquivo(caminho: str | Path) -> int:
    """Executa o fluxo simples Bronze -> Silver."""

    arquivo = Path(caminho)

    if not arquivo.exists():
        raise FileNotFoundError(f"Arquivo nao encontrado: {arquivo}")

    print("1. Lendo arquivo Bronze")

    df = pd.read_csv(
        arquivo,
        sep=";",
        encoding="latin1",
    )

    print("2. Validando dados")
    validar_informes(df)

    print("3. Transformando dados")
    df_transformado = transformar_informes(df)

    print("4. Carregando dados no PostgreSQL")
    quantidade = carregar_informes(df_transformado)

    print(f"5. Pipeline finalizado: {quantidade} registros processados.")

    return quantidade
