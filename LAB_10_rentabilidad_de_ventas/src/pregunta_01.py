import pandas as pd
from pathlib import Path


def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Una cadena de suministros de oficina vende mucho, pero la gerencia
    sospecha que parte de esas ventas no deja utilidad. El archivo
    `data/superstore_orders.csv.gz` tiene una fila por línea de pedido, con
    el número de pedido (`Order ID`), las ventas (`Sales`), la utilidad
    (`Profit`), el descuento aplicado (`Discount`, como proporción), el
    segmento del cliente (`Customer Segment`) y la categoría del producto
    (`Product Category`). Una utilidad negativa significa que la línea se
    vendió con pérdida.

    Use estas definiciones:

    - Margen (`profit_margin`): utilidad sobre ventas.
    - Línea con pérdida: una línea cuya utilidad es negativa.
    - `loss_line_rate`: la proporción de líneas con pérdida.
    - `lost_profit`: la suma de las pérdidas de las líneas con pérdida,
      escrita como número positivo.
    - Rango de descuento (`discount_band`): `0%` si no hubo descuento,
      `1%-5%` si fue mayor que 0 y hasta 5 %, `6%-10%` si fue mayor que 5 % y
      hasta 10 %, y `más de 10%` en otro caso.

    Genere tres archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `profitability_summary.csv`, con una sola fila: `lines` (cantidad de
       líneas), `orders` (pedidos distintos), `sales`, `profit`,
       `profit_margin`, `loss_lines` (cantidad de líneas con pérdida),
       `loss_line_rate` y `lost_profit`.

    2. `discount_summary.csv`, con una fila por rango de descuento, en el
       orden en que se definieron arriba: `discount_band`, `lines`, `sales`,
       `profit`, `profit_margin`, `loss_line_rate` y `lost_profit`.

    3. `priority_segments.csv`, con los cinco segmentos segmento–categoría
       que más utilidad pierden: `Customer Segment`, `Product Category`,
       `lines`, `sales`, `profit`, `profit_margin` y `lost_profit`. Considere
       solamente segmentos con al menos 100 líneas y ordénelos por
       `lost_profit` de mayor a menor.

    La función también debe retornar las tres tablas, en el mismo orden.

    Ejemplo del formato de `discount_summary.csv`:

        discount_band,lines,sales,profit,profit_margin,loss_line_rate,...
        0%,166,170539.05,29472.3789,0.1728,0.488,...
        ...
    """

    activity_dir = Path(__file__).resolve().parents[1]
    data_path = activity_dir / "data" / "superstore_orders.csv.gz"
    submission_dir = activity_dir / "submission"
    submission_dir.mkdir(exist_ok=True)

    orders = pd.read_csv(
        data_path,
        compression="gzip",
        sep=";",
        decimal=",",
        encoding="utf-8-sig",
    )
    loss = orders["Profit"] < 0

    def summarize(frame: pd.DataFrame) -> dict[str, float | int]:
        sales = frame["Sales"].sum()
        profit = frame["Profit"].sum()
        return {
            "lines": len(frame),
            "sales": sales,
            "profit": profit,
            "profit_margin": profit / sales,
            "loss_line_rate": (frame["Profit"] < 0).mean(),
            "lost_profit": -frame.loc[frame["Profit"] < 0, "Profit"].sum(),
        }

    overall = summarize(orders)
    profitability_summary = pd.DataFrame(
        [
            {
                "lines": overall["lines"],
                "orders": orders["Order ID"].nunique(),
                "sales": overall["sales"],
                "profit": overall["profit"],
                "profit_margin": overall["profit_margin"],
                "loss_lines": loss.sum(),
                "loss_line_rate": overall["loss_line_rate"],
                "lost_profit": overall["lost_profit"],
            }
        ],
        columns=[
            "lines",
            "orders",
            "sales",
            "profit",
            "profit_margin",
            "loss_lines",
            "loss_line_rate",
            "lost_profit",
        ],
    )

    orders["discount_band"] = pd.cut(
        orders["Discount"],
        bins=[-float("inf"), 0, 0.05, 0.10, float("inf")],
        labels=["0%", "1%-5%", "6%-10%", "más de 10%"],
    )
    discount_rows = []
    for band in orders["discount_band"].cat.categories:
        summary = summarize(orders[orders["discount_band"] == band])
        discount_rows.append({"discount_band": band, **summary})
    discount_summary = pd.DataFrame(
        discount_rows,
        columns=[
            "discount_band",
            "lines",
            "sales",
            "profit",
            "profit_margin",
            "loss_line_rate",
            "lost_profit",
        ],
    )

    segment_rows = []
    for (segment, category), frame in orders.groupby(
        ["Customer Segment", "Product Category"], observed=True
    ):
        segment_rows.append(
            {
                "Customer Segment": segment,
                "Product Category": category,
                **summarize(frame),
            }
        )
    segment_summary = pd.DataFrame(segment_rows)
    priority_segments = (
        segment_summary[segment_summary["lines"] >= 100]
        .sort_values("lost_profit", ascending=False)
        .head(5)
        [
            [
                "Customer Segment",
                "Product Category",
                "lines",
                "sales",
                "profit",
                "profit_margin",
                "lost_profit",
            ]
        ]
        .reset_index(drop=True)
    )

    profitability_summary.to_csv(
        submission_dir / "profitability_summary.csv", index=False
    )
    discount_summary.to_csv(submission_dir / "discount_summary.csv", index=False)
    priority_segments.to_csv(submission_dir / "priority_segments.csv", index=False)

    return profitability_summary, discount_summary, priority_segments
