import csv
import gzip
from collections import Counter
from pathlib import Path


def pregunta_04():
    """
    Cuente cuántos registros hay en cada mes, usando la fecha de la tercera
    columna (`date`). Represente el mes como un texto de dos dígitos y retorne
    una lista de tuplas `(mes, cantidad)` ordenada por el mes.

    Ejemplo del formato de la respuesta:

        [("01", 3), ("02", 4), ("03", 2), ...]
    """

    path = Path(__file__).parents[1] / "data" / "data.csv.gz"
    with gzip.open(path, "rt", encoding="utf-8", newline="") as file:
        counts = Counter(row[2][5:7] for row in csv.reader(file, delimiter="\t"))
    return sorted(counts.items())
