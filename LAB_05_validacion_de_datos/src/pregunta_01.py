import json
from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = [
    "supplier_id",
    "supplier",
    "country",
    "city",
    "purchase_date",
    "amount",
    "discount",
    "weight",
    "units",
    "unit_price",
    "contact_email",
]


def _normalize_column_name(column: str) -> str:
    """Normaliza un encabezado sin alterar los valores de las celdas."""
    return column.lstrip("\ufeff").strip().lower().replace(" ", "_")


def _missing_values(series: pd.Series) -> pd.Series:
    values = series.astype("string")
    return values.str.strip().eq("") | values.str.strip().str.upper().eq("N/A")


def main():
    """
    Antes de limpiar o analizar un conjunto de datos, un analista debe
    documentar qué problemas tiene. En este laboratorio usted no va a limpiar
    `data/ventas.csv.gz`: va a construir un reporte de calidad que deje evidencia
    de sus problemas, tal como están en el archivo.

    Lea `data/ventas.csv.gz` sin modificar sus valores. Para trabajar con los
    encabezados, normalícelos: páselos a minúsculas, elimine los espacios al
    inicio y al final (y cualquier marca BOM) y reemplace los espacios
    internos por `_`. Las columnas requeridas son `supplier_id`, `supplier`,
    `country`, `city`, `purchase_date`, `amount`, `discount`, `weight`,
    `units`, `unit_price` y `contact_email`.

    Escriba el reporte en `submission/data_quality_report.json` con estas
    claves:

    - `row_count`: cantidad de filas de datos.
    - `column_count`: cantidad de columnas.
    - `missing_required_columns`: lista ordenada de columnas requeridas que no
      están en el archivo.
    - `unexpected_columns`: lista ordenada de columnas del archivo que no son
      requeridas.
    - `duplicate_row_count`: cantidad de filas idénticas a una fila anterior.
    - `duplicate_supplier_id_row_count`: cantidad de filas cuyo `supplier_id`
      aparece más de una vez (cuente todas esas filas, no solo las
      repetidas).
    - `missing_value_count_by_column`: diccionario con la cantidad de valores
      faltantes de cada columna. Considere faltantes las celdas vacías y las
      que contienen `N/A`.
    - `invalid_email_count`: cantidad de valores de `contact_email` que no
      tienen la forma `usuario@dominio.extension`.
    - `invalid_unit_count`: cantidad de valores numéricos de `units` que no son
      enteros positivos. Los valores faltantes no se cuentan aquí.
    - `country_values`: lista ordenada de los valores distintos de `country`,
      escritos exactamente como aparecen en el archivo.

    La función también debe retornar el reporte como un diccionario.

    Ejemplo del formato del reporte:

        {
          "row_count": 103,
          "column_count": 11,
          "missing_required_columns": [],
          ...
          "country_values": [" Colombia ", "CO", ...]
        }
    """

    activity_dir = Path(__file__).resolve().parents[1]
    data_path = activity_dir / "data" / "ventas.csv.gz"
    report_path = activity_dir / "submission" / "data_quality_report.json"

    data = pd.read_csv(
        data_path,
        compression="gzip",
        dtype="string",
        keep_default_na=False,
        na_filter=False,
    )
    data.columns = [_normalize_column_name(column) for column in data.columns]

    missing_required_columns = sorted(
        set(REQUIRED_COLUMNS) - set(data.columns)
    )
    unexpected_columns = sorted(
        set(data.columns) - set(REQUIRED_COLUMNS)
    )

    missing_value_count_by_column = {
        column: int(_missing_values(data[column]).sum())
        for column in data.columns
    }

    if "supplier_id" in data.columns:
        supplier_id_counts = data["supplier_id"].value_counts(dropna=False)
        duplicate_supplier_id_row_count = int(
            data["supplier_id"].isin(
                supplier_id_counts[supplier_id_counts > 1].index
            ).sum()
        )
    else:
        duplicate_supplier_id_row_count = 0

    if "contact_email" in data.columns:
        email_pattern = r"[^@\s]+@[^@\s]+\.[^@\s]+"
        invalid_email_count = int(
            (~data["contact_email"].str.fullmatch(email_pattern, na=False)).sum()
        )
    else:
        invalid_email_count = 0

    if "units" in data.columns:
        units = pd.to_numeric(data["units"], errors="coerce")
        units_missing = _missing_values(data["units"])
        invalid_units = (
            ~units_missing
            & (units.isna() | (units <= 0) | (units % 1 != 0))
        )
        invalid_unit_count = int(invalid_units.sum())
    else:
        invalid_unit_count = 0

    if "country" in data.columns:
        country_values = sorted(
            data.loc[~_missing_values(data["country"]), "country"]
            .drop_duplicates()
            .tolist()
        )
    else:
        country_values = []

    report = {
        "row_count": int(len(data)),
        "column_count": int(len(data.columns)),
        "missing_required_columns": missing_required_columns,
        "unexpected_columns": unexpected_columns,
        "duplicate_row_count": int(data.duplicated().sum()),
        "duplicate_supplier_id_row_count": duplicate_supplier_id_row_count,
        "missing_value_count_by_column": missing_value_count_by_column,
        "invalid_email_count": invalid_email_count,
        "invalid_unit_count": invalid_unit_count,
        "country_values": country_values,
    }

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return report
