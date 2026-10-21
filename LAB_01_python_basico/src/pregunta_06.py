import csv
import gzip
from pathlib import Path


def pregunta_06():
    """
    La quinta columna (`metrics`) contiene pares `clave:valor` separados por
    comas. Para cada clave, encuentre el valor mínimo y el valor máximo que
    aparecen en todo el archivo. Retorne una lista de tuplas
    `(clave, mínimo, máximo)` ordenada alfabéticamente por la clave.

    Observe que el orden es mínimo y luego máximo, al contrario de la
    pregunta 5.

    Ejemplo del formato de la respuesta:

        [("aaa", 1, 9), ("bbb", 1, 9), ...]
    """

    values = {}
    path = Path(__file__).parents[1] / "data" / "data.csv.gz"
    with gzip.open(path, "rt", encoding="utf-8", newline="") as file:
        for row in csv.reader(file, delimiter="\t"):
            for metric in row[4].split(","):
                key, value = metric.split(":")
                number = int(value)
                if key not in values:
                    values[key] = [number, number]
                else:
                    values[key][0] = min(values[key][0], number)
                    values[key][1] = max(values[key][1], number)
    return [(key, minimum, maximum) for key, (minimum, maximum) in sorted(values.items())]
