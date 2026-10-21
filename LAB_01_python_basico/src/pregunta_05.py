import csv
import gzip
from pathlib import Path


def pregunta_05():
    """
    Para cada letra de la primera columna (`letter`), encuentre el valor
    máximo y el valor mínimo de la segunda columna (`value`). Retorne una lista
    de tuplas `(letra, máximo, mínimo)` ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 9, 2), ("B", 9, 1), ...]
    """

    values = {}
    path = Path(__file__).parents[1] / "data" / "data.csv.gz"
    with gzip.open(path, "rt", encoding="utf-8", newline="") as file:
        for row in csv.reader(file, delimiter="\t"):
            letter, value = row[0], int(row[1])
            if letter not in values:
                values[letter] = [value, value]
            else:
                values[letter][0] = max(values[letter][0], value)
                values[letter][1] = min(values[letter][1], value)
    return [(letter, maximum, minimum) for letter, (maximum, minimum) in sorted(values.items())]
