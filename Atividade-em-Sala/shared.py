from __future__ import annotations

import base64
import io
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "mercado_entretenimento.csv"


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["Ano"] = df["Ano"].astype(int)
    df["Receita_Bilhoes"] = pd.to_numeric(df["Receita_Bilhoes"], errors="coerce")
    if "Churn_Rate" in df.columns:
        df["Churn_Rate"] = pd.to_numeric(df["Churn_Rate"], errors="coerce")
    return df


def figure_to_data_uri(fig: plt.Figure) -> str:
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def style_axis(ax: plt.Axes) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", color="#d8dee9", linewidth=0.8, alpha=0.8)
    ax.set_axisbelow(True)


def find_intersection(years: np.ndarray, cinema: np.ndarray, streaming: np.ndarray) -> tuple[float, float, int] | None:
    diff = streaming - cinema
    for idx in range(len(years) - 1):
        left = diff[idx]
        right = diff[idx + 1]

        if left == 0:
            return float(years[idx]), float(streaming[idx]), int(years[idx])

        if left < 0 <= right:
            weight = -left / (right - left) if right != left else 0.0
            x = years[idx] + weight * (years[idx + 1] - years[idx])
            y = cinema[idx] + weight * (cinema[idx + 1] - cinema[idx])
            return float(x), float(y), int(np.ceil(x))

    return None
