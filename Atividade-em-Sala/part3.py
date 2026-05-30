from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec

from shared import load_data, style_axis


def build_part3_figure(df):
    streaming = df[df["Tipo"] == "Streaming"].copy()
    current_year = int(streaming["Ano"].max())
    current = streaming[streaming["Ano"] == current_year]

    churn = (
        streaming.dropna(subset=["Churn_Rate"])
        .groupby(["Ano", "Nome_Item"], as_index=False)["Churn_Rate"]
        .mean()
        .sort_values("Ano")
    )

    fig = plt.figure(figsize=(14, 9), facecolor="#f7fafc")
    grid = GridSpec(2, 3, figure=fig, height_ratios=[2.2, 1.1], hspace=0.38, wspace=0.24)

    ax_top = fig.add_subplot(grid[0, :])
    ax_top.set_facecolor("#f7fafc")

    palette = {"Netflix": "#e50914", "Prime Video": "#00a8e1", "Disney+": "#1c2f78"}
    sns.lineplot(
        data=churn,
        x="Ano",
        y="Churn_Rate",
        hue="Nome_Item",
        palette=palette,
        marker="o",
        linewidth=2.8,
        markersize=6.5,
        ax=ax_top,
    )
    style_axis(ax_top)
    ax_top.set_title("Tendência de churn das plataformas de streaming", loc="left", pad=16, fontsize=18, fontweight="bold")
    ax_top.set_xlabel("Ano")
    ax_top.set_ylabel("Churn rate")
    ax_top.legend(title="Plataforma", frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.12))
    ax_top.axvspan(current_year - 0.3, current_year + 0.3, color="#dbeafe", alpha=0.55)
    ax_top.text(current_year + 0.05, ax_top.get_ylim()[1] * 0.95, f"Ano atual: {current_year}", color="#1d4ed8", fontsize=10.5, fontweight="bold")

    share_colors = ["#0f766e", "#7c3aed", "#d97706", "#db2777", "#2563eb", "#16a34a"]
    players = ["Netflix", "Disney+", "Prime Video"]

    for idx, player in enumerate(players):
        ax = fig.add_subplot(grid[1, idx])
        ax.set_facecolor("#f7fafc")
        player_data = current[current["Nome_Item"] == player].groupby("Regiao", as_index=False)["Receita_Bilhoes"].sum()

        if player_data.empty:
            ax.text(0.5, 0.5, f"Sem dados de {player}", ha="center", va="center", fontsize=11)
            ax.axis("off")
            continue

        ax.pie(
            player_data["Receita_Bilhoes"],
            labels=player_data["Regiao"],
            colors=share_colors[: len(player_data)],
            autopct=lambda pct: f"{pct:.0f}%" if pct >= 8 else "",
            startangle=90,
            textprops={"fontsize": 9, "color": "#111827"},
            wedgeprops={"linewidth": 1.2, "edgecolor": "white"},
        )
        center = plt.Circle((0, 0), 0.60, fc="#f7fafc")
        ax.add_artist(center)
        ax.set_title(f"{player}\nparticipação regional {current_year}", fontsize=12, fontweight="bold")
        ax.axis("equal")

    fig.suptitle("Grid de contexto: churn acima e composição atual abaixo", x=0.01, y=0.98, ha="left", fontsize=19, fontweight="bold")
    return fig


def export_part3(path: str | Path = "part3.png") -> Path:
    df = load_data()
    figure = build_part3_figure(df)
    target = Path(path)
    figure.savefig(target, dpi=180, bbox_inches="tight")
    plt.close(figure)
    return target


if __name__ == "__main__":
    output = export_part3()
    print(f"Parte 3 exportada para {output}")
