from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from dash import Dash, Input, Output, dcc, html

from shared import figure_to_data_uri, find_intersection, load_data, style_axis


def build_part2_figure(df, region: str):
    regional = (
        df[df["Regiao"] == region]
        .groupby(["Ano", "Tipo"], as_index=False)["Receita_Bilhoes"]
        .sum()
        .pivot(index="Ano", columns="Tipo", values="Receita_Bilhoes")
        .sort_index()
    )

    years = regional.index.to_numpy(dtype=float)
    cinema = regional["Cinema"].to_numpy(dtype=float)
    streaming = regional["Streaming"].to_numpy(dtype=float)

    intersection = find_intersection(years, cinema, streaming)

    fig, ax = plt.subplots(figsize=(12, 6.6), facecolor="#fbfbfd")
    ax.set_facecolor("#fbfbfd")

    ax.plot(years, cinema, color="#0b7285", linewidth=3.0, marker="o", markersize=6.5, label="Cinema")
    ax.plot(years, streaming, color="#d9480f", linewidth=3.0, marker="o", markersize=6.5, label="Streaming")

    style_axis(ax)
    ax.set_title(f"Ponto de virada do mercado em {region}", loc="left", pad=16, fontsize=18, fontweight="bold")
    ax.set_xlabel("Ano")
    ax.set_ylabel("Receita (bilhões)")
    ax.legend(frameon=False, loc="upper left")

    caption = f"Sem cruzamento identificado em {region}."
    if intersection is not None:
        x_cross, y_cross, label_year = intersection
        caption = f"Em {label_year}, o Streaming tornou-se a força dominante nesta região."

        ax.scatter([x_cross], [y_cross], s=120, color="#111827", zorder=5)
        ax.axvline(x_cross, color="#111827", linestyle="--", linewidth=1.2, alpha=0.75)
        ax.axhline(y_cross, color="#111827", linestyle=":", linewidth=1.1, alpha=0.45)
        ax.annotate(
            caption,
            xy=(x_cross, y_cross),
            xytext=(x_cross + 0.55, y_cross + max(cinema.max(), streaming.max()) * 0.08),
            arrowprops=dict(arrowstyle="->", color="#111827", lw=1.4),
            bbox=dict(boxstyle="round,pad=0.45", fc="#fff7ed", ec="#f59e0b", alpha=0.98),
            fontsize=10.5,
            color="#1f2937",
        )
        ax.text(
            0.02,
            0.96,
            f"Interseção estimada: {x_cross:.2f} / {y_cross:.2f}",
            transform=ax.transAxes,
            ha="left",
            va="top",
            fontsize=10,
            color="#4b5563",
            bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="#d8dee9"),
        )
        ax.axvspan(x_cross, years.max(), color="#fde68a", alpha=0.18)
    else:
        ax.axvspan(2020, years.max(), color="#fde68a", alpha=0.18)

    ax.margins(x=0.03)
    return fig, caption


def create_app(df=None) -> Dash:
    data = load_data() if df is None else df
    regions = list(data["Regiao"].dropna().unique())

    default_fig, default_caption = build_part2_figure(data, regions[0])
    default_src = figure_to_data_uri(default_fig)

    app = Dash(__name__)

    app.layout = html.Div(
        style={
            "minHeight": "100vh",
            "background": "linear-gradient(180deg, #e9eef7 0%, #f7f9fc 38%, #eef2f7 100%)",
            "padding": "24px",
            "fontFamily": "Georgia, 'Times New Roman', serif",
            "color": "#0f172a",
        },
        children=[
            html.Div(
                style={"maxWidth": "1380px", "margin": "0 auto", "display": "grid", "gap": "18px"},
                children=[
                    html.Div(
                        style={
                            "background": "linear-gradient(135deg, #0f172a 0%, #1e3a8a 55%, #0f766e 100%)",
                            "borderRadius": "22px",
                            "padding": "28px 30px",
                            "boxShadow": "0 18px 40px rgba(15, 23, 42, 0.18)",
                            "color": "white",
                        },
                        children=[
                            html.Div("BI e DV - Mercado de Entretenimento", style={"fontSize": "15px", "letterSpacing": "0.12em", "textTransform": "uppercase", "opacity": 0.85}),
                            html.H1("Dashboard executivo das 3 atividades", style={"margin": "10px 0 8px", "fontSize": "34px", "lineHeight": 1.05}),
                            html.P(
                                "Uma leitura única para bilheteria, ponto de virada entre cinema e streaming e contexto de churn das plataformas.",
                                style={"margin": 0, "fontSize": "18px", "maxWidth": "900px", "opacity": 0.93},
                            ),
                        ],
                    ),
                    html.Div(
                        style={"display": "grid", "gridTemplateColumns": "1fr", "gap": "18px"},
                        children=[
                            html.Div(
                                style={"background": "white", "borderRadius": "20px", "padding": "22px 24px", "boxShadow": "0 12px 28px rgba(15, 23, 42, 0.08)"},
                                children=[
                                    html.H2("Parte 2 - Ponto de virada interativo", style={"marginTop": 0, "marginBottom": "10px", "fontSize": "24px"}),
                                    html.P("Selecione a região para cruzar cinema versus streaming e evidenciar o ponto de intersecção.", style={"marginTop": 0, "color": "#475569"}),
                                    html.Div(
                                        style={"display": "grid", "gridTemplateColumns": "280px 1fr", "gap": "16px", "alignItems": "end", "marginBottom": "16px"},
                                        children=[
                                            html.Div(
                                                children=[
                                                    html.Label("Região", style={"display": "block", "marginBottom": "8px", "fontWeight": "bold"}),
                                                    dcc.Dropdown(
                                                        id="region-dropdown",
                                                        options=[{"label": region, "value": region} for region in regions],
                                                        value=regions[0],
                                                        clearable=False,
                                                        style={"borderRadius": "12px"},
                                                    ),
                                                ]
                                            ),
                                            html.Div(id="turning-point-caption", children=default_caption, style={"fontSize": "16px", "color": "#334155", "paddingBottom": "4px"}),
                                        ],
                                    ),
                                    html.Img(id="turning-point-image", src=default_src, style={"width": "100%", "borderRadius": "16px", "border": "1px solid #e2e8f0"}),
                                ],
                            )
                        ],
                    ),
                ],
            )
        ],
    )

    @app.callback(
        Output("turning-point-image", "src"),
        Output("turning-point-caption", "children"),
        Input("region-dropdown", "value"),
    )
    def update_turning_point(region: str):
        fig, caption = build_part2_figure(data, region)
        return figure_to_data_uri(fig), caption

    return app


def export_part2(df=None, region: str | None = None, path: str | Path = "part2.png") -> Path:
    data = load_data() if df is None else df
    selected_region = region or data["Regiao"].dropna().iloc[0]
    figure, _ = build_part2_figure(data, selected_region)
    target = Path(path)
    figure.savefig(target, dpi=180, bbox_inches="tight")
    plt.close(figure)
    return target


if __name__ == "__main__":
    create_app().run(debug=True, host="0.0.0.0", port=8050)
