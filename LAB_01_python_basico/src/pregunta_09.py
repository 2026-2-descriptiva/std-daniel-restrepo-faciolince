import csv
import gzip
from collections import Counter
from pathlib import Path


def pregunta_09():
    """
    Cuente cuántas veces aparece cada clave en la quinta columna (`metrics`)
    de todo el archivo. Retorne un diccionario `{clave: cantidad}` con las
    claves en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"aaa": 13, "bbb": 16, "ccc": 23, ...}
    """

    counts = Counter()
    path = Path(__file__).parents[1] / "data" / "data.csv.gz"
    with gzip.open(path, "rt", encoding="utf-8", newline="") as file:
        for row in csv.reader(file, delimiter="\t"):
            counts.update(metric.split(":")[0] for metric in row[4].split(","))
    return {key: counts[key] for key in sorted(counts)}
