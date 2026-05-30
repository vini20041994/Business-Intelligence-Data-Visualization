from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns

from shared import load_data, style_axis


def build_part1_figure(df):
    cinema = (
        df[df["Tipo"] == "Cinema"]
        .groupby(["Ano", "Nome_Item"], as_index=False)["Receita_Bilhoes"]
        .sum()
        .sort_values("Ano")
    )

    sns.set_theme(style="whitegrid")
    palette = {
        "Ação": "#0b7285",
        "Drama": "#c92a2a",
        "Comédia": "#f08c00",
        "Terror": "#5f3dc4",
    }

    fig, ax = plt.subplots(figsize=(14, 7), facecolor="#f6f8fc")
    ax.set_facecolor("#f6f8fc")

    sns.lineplot(
        data=cinema,
        x="Ano",
        y="Receita_Bilhoes",
        hue="Nome_Item",
        palette=palette,
        marker="o",
        linewidth=2.8,
        markersize=7,
        ax=ax,
    )

    style_axis(ax)
    ax.set_title("Bilheteria de cinema por gênero: antes, durante e depois da ruptura de 2020", loc="left", pad=18, fontsize=18, fontweight="bold")
    ax.set_xlabel("Ano")
    ax.set_ylabel("Receita (bilhões)")
    ax.legend(title="Gênero", frameon=False, ncol=4, loc="upper center", bbox_to_anchor=(0.5, 1.10))

    ax.axvspan(2019.5, 2020.5, color="#ffe3e3", alpha=0.45, zorder=0)
    ax.axvline(2020, color="#b02a37", linestyle="--", linewidth=1.6)
    ax.text(
        2020.08,
        ax.get_ylim()[1] * 0.96,
        "2020: choque da pandemia",
        color="#8b1e2d",
        fontsize=11,
        fontweight="bold",
        va="top",
    )

    pivot = cinema.pivot(index="Ano", columns="Nome_Item", values="Receita_Bilhoes").sort_index()
    shock = pivot.loc[2019] - pivot.loc[2020]
    worst_genre = shock.idxmax()
    worst_value = shock.max()
    y_2020 = pivot.loc[2020, worst_genre]
    ax.annotate(
        f"Maior queda: {worst_genre} (-{worst_value:.2f})",
        xy=(2020, y_2020),
        xytext=(2014.3, y_2020 + 1.8),
        arrowprops=dict(arrowstyle="->", color="#b02a37", lw=1.5),
        bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#cfd8e3", alpha=0.96),
        fontsize=10.5,
        color="#243447",
    )

    for genre, color in palette.items():
        series = pivot[genre].dropna()
        ax.text(
            series.index.max() + 0.12,
            series.iloc[-1],
            genre,
            color=color,
            fontsize=10,
            va="center",
            fontweight="bold",
        )

    ax.margins(x=0.04)
    return fig


def export_part1(path: str | Path = "part1.png") -> Path:
    df = load_data()
    figure = build_part1_figure(df)
    target = Path(path)
    figure.savefig(target, dpi=180, bbox_inches="tight")
    plt.close(figure)
    return target


if __name__ == "__main__":
    output = export_part1()
    print(f"Parte 1 exportada para {output}")
