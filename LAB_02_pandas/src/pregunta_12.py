def pregunta_12():
    """
    En `data/tbl2.tsv`, cada valor de la columna `c0` aparece en varias
    filas. Construya un DataFrame con una fila por cada valor de `c0`, en
    orden ascendente, y las columnas `c0` y `c5`. En `c5`, forme un texto
    `c5a:c5b` para cada fila de ese `c0`, ordene esos textos alfabéticamente y
    únalos separados por comas.

    Ejemplo del formato de la respuesta:

            c0                             c5
        0    0  bbb:0,ddd:9,ggg:8,hhh:2,jjj:3
        1    1        aaa:3,ccc:2,ddd:0,hhh:9
        2    2        ccc:6,ddd:2,ggg:5,jjj:1
        ...
    """

    from pathlib import Path

    import pandas as pd

    path = Path(__file__).parents[1] / "data" / "tbl2.tsv"
    table = pd.read_csv(path, sep="\t")
    table["c5"] = table["c5a"] + ":" + table["c5b"].astype(str)
    return (
        table.groupby("c0", sort=True)["c5"]
        .agg(lambda values: ",".join(sorted(values)))
        .reset_index()
    )
