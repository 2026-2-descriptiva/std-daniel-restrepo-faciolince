def pregunta_03():
    """
    Usando `data/tbl0.tsv`, cuente cuántos registros hay para cada categoría
    de la columna `c1`. Retorne una Serie de Pandas cuyo índice son las
    categorías, en orden alfabético, y cuyos valores son las cantidades.

    Ejemplo del formato de la respuesta:

        c1
        A     8
        B     7
        C     5
        ...
    """

    from pathlib import Path

    import pandas as pd

    path = Path(__file__).parents[1] / "data" / "tbl0.tsv"
    return pd.read_csv(path, sep="\t").groupby("c1")["c1"].count()
