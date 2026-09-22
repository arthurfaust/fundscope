from collections.abc import Iterable


def validar_colunas(colunas: Iterable[str], obrigatorias: Iterable[str]) -> None:
    """Interrompe o processamento se faltarem colunas obrigatórias."""
    faltantes = set(obrigatorias) - set(colunas)

    if faltantes:
        nomes = ", ".join(sorted(faltantes))
        raise ValueError(f"Colunas obrigatórias ausentes: {nomes}")
