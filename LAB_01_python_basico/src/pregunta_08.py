import csv
import gzip
from collections import defaultdict
from pathlib import Path


def pregunta_08():
    """
    Repita la pregunta 7, pero ahora cada lista de letras debe contener cada
    letra una sola vez y estar ordenada alfabéticamente. Retorne una lista de
    tuplas `(valor, letras)` ordenada por el valor.

    Ejemplo del formato de la respuesta:

        [(0, ["C"]), (1, ["B", "E"]), (2, ["A", "E"]), ...]
    """

    letters_by_value = defaultdict(set)
    path = Path(__file__).parents[1] / "data" / "data.csv.gz"
    with gzip.open(path, "rt", encoding="utf-8", newline="") as file:
        for row in csv.reader(file, delimiter="\t"):
            letters_by_value[int(row[1])].add(row[0])
    return [(value, sorted(letters)) for value, letters in sorted(letters_by_value.items())]
