from pathlib import Path
from urllib.request import urlretrieve


def baixar_arquivo(url: str, destino: str | Path) -> Path:
    """Baixa um arquivo e o salva na camada Bronze."""
    caminho = Path(destino)

    caminho.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    urlretrieve(url, caminho)

    return caminho
