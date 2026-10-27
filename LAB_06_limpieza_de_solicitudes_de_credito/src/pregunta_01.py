from pathlib import Path

import pandas as pd


OUTPUT_COLUMNS = [
    "sexo",
    "tipo_de_emprendimiento",
    "idea_negocio",
    "barrio",
    "estrato",
    "comuna_ciudadano",
    "fecha_de_beneficio",
    "monto_del_credito",
    "línea_credito",
]
TEXT_COLUMNS = [
    "sexo",
    "tipo_de_emprendimiento",
    "idea_negocio",
    "barrio",
    "línea_credito",
]


def _normalize_text(series: pd.Series) -> pd.Series:
    return (
        series.str.lower()
        .str.strip()
        .str.replace("-", " ", regex=False)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )


def _parse_dates(values: pd.Series) -> pd.Series:
    dates = pd.to_datetime(values, format="%d/%m/%Y", errors="coerce")
    for date_format in ["%Y-%m-%d", "%Y/%m/%d"]:
        dates = dates.fillna(
            pd.to_datetime(values, format=date_format, errors="coerce")
        )
    return dates.dt.strftime("%Y-%m-%d")


def pregunta_01():
    """
    El archivo `data/solicitudes_de_credito.csv.gz` contiene las solicitudes de
    un programa de crédito, pero llegó sucio: tiene una columna de índice que
    no pertenece a los datos, registros duplicados, registros incompletos y
    valores que representan lo mismo escritos de formas distintas en los
    campos de texto, las fechas, el estrato y el monto.

    Su tarea es limpiarlo y guardar el resultado en
    `submission/solicitudes_de_credito.csv`, usando punto y coma (`;`) como
    separador y sin el índice de Pandas.

    El archivo limpio debe cumplir lo siguiente:

    - Contiene solamente las nueve columnas `sexo`, `tipo_de_emprendimiento`,
      `idea_negocio`, `barrio`, `estrato`, `comuna_ciudadano`,
      `fecha_de_beneficio`, `monto_del_credito` y `línea_credito`, en ese
      orden.
    - Los campos de texto están en minúsculas y sus palabras separadas por
      espacios.
    - `estrato` y `monto_del_credito` son números enteros, sin símbolos ni
      separadores de miles.
    - Todas las fechas de `fecha_de_beneficio` usan un mismo formato, por
      ejemplo `AAAA-MM-DD`.
    - No hay registros incompletos. La única excepción es
      `comuna_ciudadano`: sus valores faltantes son parte de los datos
      originales y deben conservarse.
    - No hay registros duplicados.

    Ejemplo del formato del archivo:

        sexo;tipo_de_emprendimiento;idea_negocio;barrio;estrato;...
        femenino;comercio;almacen de ropa en;los cerros el vergel;2;...
        ...
    """

    activity_dir = Path(__file__).resolve().parents[1]
    data_path = activity_dir / "data" / "solicitudes_de_credito.csv.gz"
    submission_path = activity_dir / "submission" / "solicitudes_de_credito.csv"

    data = pd.read_csv(
        data_path,
        compression="gzip",
        sep=";",
        encoding="utf-8",
        dtype="string",
        keep_default_na=False,
        na_filter=False,
    )
    data = data.drop(columns=[data.columns[0]])

    for column in TEXT_COLUMNS:
        data[column] = _normalize_text(data[column])

    data["estrato"] = pd.to_numeric(data["estrato"], errors="coerce").astype(
        "Int64"
    )
    data["comuna_ciudadano"] = pd.to_numeric(
        data["comuna_ciudadano"], errors="coerce"
    ).astype("Int64")
    data["fecha_de_beneficio"] = _parse_dates(data["fecha_de_beneficio"])

    amount = (
        data["monto_del_credito"]
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.replace(".00", "", regex=False)
        .str.strip()
    )
    data["monto_del_credito"] = pd.to_numeric(
        amount, errors="coerce"
    ).astype("Int64")

    complete = data["tipo_de_emprendimiento"].ne("") & data["barrio"].ne("")
    data = data.loc[complete, OUTPUT_COLUMNS].drop_duplicates()

    submission_path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(submission_path, sep=";", index=False)
