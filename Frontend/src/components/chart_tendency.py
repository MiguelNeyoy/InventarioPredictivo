import flet as ft
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import os

matplotlib.use("Agg")


def crear_grafico_tendencia(df_predicciones=None, df_historico=None):
    fig, ax = plt.subplots(figsize=(10, 3.5), facecolor="white")

    if df_historico is not None and not df_historico.empty:
        df_historico = df_historico.sort_values("ds")
        meses = df_historico["ds"].dt.strftime("%b").tolist()[-7:]
        valores_reales = df_historico["y"].tolist()[-7:]

        ax.plot(
            meses,
            valores_reales,
            color="#0058be",
            linewidth=3,
            marker="o",
            label="Real",
        )
    else:
        meses = ["ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL"]
        valores_reales = [50, 80, 40, 120, 90, 180, 140]
        ax.plot(
            meses,
            valores_reales,
            color="#0058be",
            linewidth=3,
            marker="o",
            label="Real",
        )

    if df_predicciones is not None and not df_predicciones.empty:
        productos_unicos = df_predicciones["Producto"].unique()
        if len(productos_unicos) > 0:
            producto = productos_unicos[0]
            df_prod = df_predicciones[df_predicciones["Producto"] == producto]
            ventas = df_prod["Venta_Estimada"].tolist()
            pronostico_meses = [f"P{i+1}" for i in range(len(ventas))]

            ax.plot(
                pronostico_meses[:5],
                ventas[:5],
                color="#ef4444",
                linewidth=2.5,
                linestyle="--",
                marker="o",
                label="Predicción",
            )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#cbd5e1")
    ax.spines["bottom"].set_color("#cbd5e1")
    ax.tick_params(colors="#505f76", labelsize=9)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.set_ylim(bottom=0)

    ax.legend(
        frameon=False, loc="upper right", ncol=3, fontsize=9, labelcolor="#505f76"
    )
    plt.tight_layout()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(base_dir, "..", "..", "tendencia_grafico.png")
    plt.savefig(filepath, format="png", dpi=100, bbox_inches="tight")
    plt.close(fig)

    return filepath


def crear_grafico_barras(df_predicciones=None):
    if df_predicciones is None or df_predicciones.empty:
        return None

    productos = df_predicciones["Producto"].tolist()[:5]
    ventas = df_predicciones["Venta_Estimada"].tolist()[:5]

    fig, ax = plt.subplots(figsize=(8, 4), facecolor="white")
    colores = ["#0058be" if i % 2 == 0 else "#4da6ff" for i in range(len(productos))]

    ax.barh(productos[::-1], ventas[::-1], color=colores[::-1])

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#cbd5e1")
    ax.spines["bottom"].set_color("#cbd5e1")
    ax.tick_params(colors="#505f76", labelsize=10)
    ax.grid(axis="x", linestyle="--", alpha=0.3)

    for i, v in enumerate(ventas[::-1]):
        ax.text(v + max(ventas) * 0.02, i, str(v), va="center", fontsize=10)

    plt.tight_layout()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(base_dir, "..", "..", "barras_productos.png")
    plt.savefig(filepath, format="png", dpi=100, bbox_inches="tight")
    plt.close(fig)

    return filepath