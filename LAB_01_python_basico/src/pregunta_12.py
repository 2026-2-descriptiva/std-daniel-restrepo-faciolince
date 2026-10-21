import csv
import gzip
from collections import defaultdict
from pathlib import Path


def pregunta_12():
    """
    Para cada letra de la primera columna (`letter`), sume todos los valores
    numéricos de los pares `clave:valor` de la quinta columna (`metrics`).
    Retorne un diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"A": 177, "B": 187, "C": 114, ...}
    """

    totals = defaultdict(int)
    path = Path(__file__).parents[1] / "data" / "data.csv.gz"
    with gzip.open(path, "rt", encoding="utf-8", newline="") as file:
        for row in csv.reader(file, delimiter="\t"):
            totals[row[0]] += sum(
                int(metric.split(":")[1]) for metric in row[4].split(",")
            )
    return {key: totals[key] for key in sorted(totals)}
