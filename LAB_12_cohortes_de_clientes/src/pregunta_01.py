import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def build_cohort_analysis() -> pd.DataFrame:
    """
    Una tienda quiere saber si sus clientes vuelven a comprar después de su
    primera compra. Para responder, agrupe a los clientes en cohortes según
    el mes de su primera compra y mida, mes a mes, qué proporción de cada
    cohorte vuelve a comprar. Use `data/sales.csv.gz`, que tiene una fila por
    orden con su cliente (`CustomerID`) y su fecha (`OrderDate`).

    Use estas definiciones:

    - `cohort_month`: el mes de la primera compra del cliente, escrito como
      `AAAA-MM`.
    - `period_index`: los meses transcurridos desde `cohort_month`; es 0 en el
      mes de la primera compra, 1 en el mes siguiente, y así sucesivamente.
    - `active_customers`: la cantidad de clientes distintos de la cohorte que
      compraron en ese período.
    - `cohort_size`: la cantidad de clientes de la cohorte, es decir, sus
      clientes activos en el período 0.
    - `retention_rate`: `active_customers` sobre `cohort_size`.

    Genere dos archivos en `submission/`:

    1. `cohort_retention.csv`, sin el índice de Pandas, con las columnas
       `cohort_month`, `period_index`, `active_customers`, `cohort_size` y
       `retention_rate`, y una fila por cada combinación cohorte–período
       observada, ordenadas por cohorte y período.

    2. `cohort_retention_heatmap.png`, un mapa de calor de `retention_rate`
       con una fila por cohorte (eje vertical) y una columna por período
       (eje horizontal). Muestre los valores como porcentajes. Los períodos
       que todavía no se pueden observar para una cohorte no significan
       retención cero: déjelos vacíos en el mapa.

    La función también debe retornar la tabla de retención.

    Ejemplo del formato de `cohort_retention.csv`:

        cohort_month,period_index,active_customers,cohort_size,retention_rate
        2022-01,0,100,100,1.0
        2022-01,1,26,100,0.26
        ...
    """

    activity_dir = Path(__file__).resolve().parents[1]
    data_path = activity_dir / "data" / "sales.csv.gz"
    submission_dir = activity_dir / "submission"
    submission_dir.mkdir(exist_ok=True)

    sales = pd.read_csv(data_path, compression="gzip")
    sales["order_month"] = pd.to_datetime(sales["OrderDate"]).dt.to_period("M")
    first_purchase = sales.groupby("CustomerID")["order_month"].transform("min")
    sales["cohort_month"] = first_purchase
    sales["period_index"] = (
        sales["order_month"].dt.year * 12
        + sales["order_month"].dt.month
        - first_purchase.dt.year * 12
        - first_purchase.dt.month
    )

    retention = (
        sales.groupby(["cohort_month", "period_index"], as_index=False)["CustomerID"]
        .nunique()
        .rename(columns={"CustomerID": "active_customers"})
    )
    cohort_sizes = (
        retention[retention["period_index"] == 0][
            ["cohort_month", "active_customers"]
        ]
        .rename(columns={"active_customers": "cohort_size"})
    )
    retention = retention.merge(cohort_sizes, on="cohort_month", how="left")
    retention["retention_rate"] = (
        retention["active_customers"] / retention["cohort_size"]
    )
    retention = retention.sort_values(
        ["cohort_month", "period_index"]
    ).reset_index(drop=True)
    retention["cohort_month"] = retention["cohort_month"].astype(str)
    retention = retention[
        [
            "cohort_month",
            "period_index",
            "active_customers",
            "cohort_size",
            "retention_rate",
        ]
    ]

    retention.to_csv(
        submission_dir / "cohort_retention.csv",
        index=False,
    )

    heatmap = retention.pivot(
        index="cohort_month",
        columns="period_index",
        values="retention_rate",
    )
    fig, ax = plt.subplots(figsize=(10, 6))
    image = ax.imshow(
        heatmap.to_numpy(dtype=float),
        aspect="auto",
        cmap="Blues",
        vmin=0,
        vmax=1,
    )
    ax.set_xlabel("Período desde la primera compra")
    ax.set_ylabel("Cohorte")
    ax.set_xticks(range(len(heatmap.columns)), heatmap.columns)
    ax.set_yticks(range(len(heatmap.index)), heatmap.index)
    for row in range(len(heatmap.index)):
        for column in range(len(heatmap.columns)):
            value = heatmap.iat[row, column]
            if pd.notna(value):
                ax.text(
                    column,
                    row,
                    f"{value:.0%}",
                    ha="center",
                    va="center",
                )
    fig.colorbar(image, ax=ax, format=lambda value, _: f"{value:.0%}")
    fig.tight_layout()
    fig.savefig(submission_dir / "cohort_retention_heatmap.png", dpi=150)
    plt.close(fig)

    return retention
