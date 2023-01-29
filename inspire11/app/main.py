import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
from dash import html, dcc, dash_table
import plotly.express as px
import pandas as pd
import json
import os
import re
import urllib
from common_app import *
from dm.dm_movies_meta import *
from dm.dm_tab_overview import *

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

agg_df = get_agg_query(partition=[])
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
rank_df = get_rank_query(order_input="revenue", desc_input="desc")


app.layout = html.Div(
    [
        html.Div(
            [
                html.Img(
                    src="https://media.licdn.com/dms/image/D5603AQE6N9wcsFkQOg/profile-displayphoto-shrink_200_200/0/1668978080590?e=1680134400&v=beta&t=GNzsOIOZadsH8aaBXHyydEOBn1Tjr7PAqwxU_gbQiDY",
                    style={"width": "10%"},
                ),
                html.H2(
                    "Inspire11 Case Study",
                    style={"margin-top": "0%", "padding-top": "0px"},
                ),
                html.Div(
                    [
                        html.A(
                            "Developed By Alex Surin",
                            href="https://www.linkedin.com/in/alexandr-surin-59360773/",
                            target="_blank",
                        )
                    ]
                ),
            ],
            style={"textAlign": "center"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Br(),
                        html.Label("Select Data"),
                        dcc.RadioItems(
                            id="input-button-raw-data",
                            options=["Combined", "Movies Meta", "Ranking"],
                            value="Combined",
                        ),
                        html.Br(),
                        html.Label("Filter Input by movieID"),
                        dcc.Dropdown(
                            id="input-filter-data",
                            options=agg_df["movieID"],
                            multi=True,
                        ),
                    ],
                    style={
                        "background-color": "#F9F9F9",
                        "margin": "2px",
                        "padding": "2px",
                    },
                ),
                html.Div(
                    [
                        html.Label("Scatter Plot Data"),
                        html.Br(),
                        html.Div(
                            [
                                html.Label("(X)Scatter Plot Data"),
                                dcc.Dropdown(
                                    id="input-scatter-x",
                                    options=list(agg_df.columns),
                                    value="revenue",
                                ),
                            ]
                        ),
                        html.Div(
                            [
                                html.Label("(Y)Scatter Plot Data"),
                                dcc.Dropdown(
                                    id="input-scatter-y",
                                    options=list(agg_df.columns),
                                    value="budget",
                                ),
                            ]
                        ),
                        html.Div(
                            [
                                html.Label("Partition"),
                                dcc.Dropdown(
                                    id="input-scatter-partition",
                                    options=list(agg_df.columns),
                                    value=["production_company"],
                                    multi=True,
                                ),
                            ]
                        ),
                        html.Div(
                            [
                                html.Label("Scatter Plot Color"),
                                dcc.Dropdown(
                                    id="input-scatter-color",
                                    options=list(agg_df.columns),
                                    value="budget",
                                ),
                            ],  # style={"width": "90%"},
                        ),
                        html.Div(
                            [
                                html.Label("Scatter Plot Size"),
                                dcc.Dropdown(
                                    id="input-scatter-size",
                                    options=list(agg_df.columns),
                                    value="budget",
                                ),
                            ]
                        ),
                    ],
                    style={
                        "background-color": "#F9F9F9",
                        "margin": "2px",
                        "padding": "2px",
                        "display": "inline-block",
                        "width": "15%",
                    },
                ),
                html.Div(
                    [
                        html.Label("Rank Company"),
                        html.Br(),
                        html.Div(
                            [
                                html.Label("Order By (Rank)"),
                                dcc.Dropdown(
                                    id="input-rank-scatter-order_input",
                                    options=list(rank_df.columns),
                                    value="partitioned_avg_revenue",
                                ),
                            ]
                        ),
                        html.Div(
                            [
                                html.Label("Order Direction"),
                                dcc.RadioItems(
                                    id="input-rank-scatter-desc_input",
                                    options=["Desc", "Asc"],
                                    value="Desc",
                                ),
                            ]
                        ),
                    ],
                    style={
                        "background-color": "#F9F9F9",
                        "margin": "2px",
                        "padding": "2px",
                        "display": "inline-block",
                        "width": "15%",
                    },
                ),
            ],
            style={
                "background-color": "#ADD8E6",
                "margin": "15px",
                "padding": "15px",
                "border": "1px solid #ADD8E6",
                "border-radius": "10px",
                "display": "flex",
            },
        ),
        html.Div(
            [
                dcc.Tabs(
                    id="tabs-example-graph",
                    value="tab-0-overview-data",
                    children=[
                        dcc.Tab(label="Overview", value="tab-0-overview-data"),
                        dcc.Tab(
                            label="Advanced Analytics", value="tab-1-advanced-analytics"
                        ),
                    ],
                )
            ]
        ),
        html.Div(id="tabs-content-example-graph"),
    ]
)


@app.callback(
    Output("tabs-content-example-graph", "children"),
    [
        Input("tabs-example-graph", "value"),
        Input("input-button-raw-data", "value"),
        Input("input-filter-data", "value"),
        Input("input-scatter-x", "value"),
        Input("input-scatter-y", "value"),
        Input("input-scatter-partition", "value"),
        Input("input-scatter-color", "value"),
        Input("input-scatter-size", "value"),
        Input("input-rank-scatter-desc_input", "value"),
        Input("input-rank-scatter-order_input", "value"),
    ],
)
def render_content(
    tab,
    input_button_raw_data,
    filter_input,
    x,
    y,
    partition,
    color,
    size,
    desc_input,
    order_input,
):
    if tab == "tab-1-advanced-analytics":
        return html.Div(
            [
                html.H4(children=f"ML and Advanced Analytics .... To Be Continued "),
            ]
        )

    elif tab == "tab-0-overview-data":
        if input_button_raw_data == "Movies Meta":
            df = get_raw_movies_meta()
            return html.Div(
                [
                    html.H4(children=f"Raw Data Preview: {input_button_raw_data}"),
                    generate_table(df),
                ]
            )
        elif input_button_raw_data == "Ranking":

            df = get_raw_ranks()
            return html.Div(
                [
                    html.H4(children=f"Raw Data Preview: {input_button_raw_data}"),
                    generate_table(df),
                ]
            )
        elif input_button_raw_data == "Combined":

            df = get_relevant_df()

            agg_df_select = get_agg_query(partition=partition)
            rank_df_select = get_rank_query(
                order_input=order_input, desc_input=desc_input
            )

            if filter_input and len(filter_input) > 0:
                df_vis = agg_df.query("movieID in @filter_input")
            else:
                df_vis = agg_df
            return html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H3(
                                        "{}".format(
                                            len(
                                                df[
                                                    ["production_company"]
                                                ].drop_duplicates()
                                            )
                                        ),
                                        id="total_companies",
                                        style={
                                            "background-color": "#F9F9F9",
                                            "margin": "2px",
                                            "padding": "2px",
                                            "textAlign": "center",
                                            "display": "inline-block",
                                        },
                                    ),
                                    html.H5(
                                        "Total: Companies",
                                        style={
                                            "background-color": "#F9F9F9",
                                            "margin": "2px",
                                            "padding": "2px",
                                            "textAlign": "center",
                                        },
                                    ),
                                    html.H3(
                                        "{}".format(
                                            len(
                                                df[
                                                    ["production_country"]
                                                ].drop_duplicates()
                                            )
                                        ),
                                        id="total_countries",
                                        style={
                                            "background-color": "#F9F9F9",
                                            "margin": "2px",
                                            "padding": "2px",
                                            "textAlign": "center",
                                        },
                                    ),
                                    html.H5(
                                        "Total: Countries",
                                        style={
                                            "background-color": "#F9F9F9",
                                            "margin": "2px",
                                            "padding": "2px",
                                            "textAlign": "center",
                                        },
                                    ),
                                    html.H3(
                                        "{}".format(
                                            len(df[["movieID"]].drop_duplicates())
                                        ),
                                        id="total_movies",
                                        style={
                                            "background-color": "#F9F9F9",
                                            "margin": "2px",
                                            "padding": "2px",
                                            "textAlign": "center",
                                        },
                                    ),
                                    html.H5(
                                        "Total: Movies",
                                        style={
                                            "background-color": "#F9F9F9",
                                            "margin": "2px",
                                            "padding": "2px",
                                            "textAlign": "center",
                                        },
                                    ),
                                    html.H3(
                                        "{}".format(
                                            len(df[["main_language"]].drop_duplicates())
                                        ),
                                        id="total_language",
                                        style={
                                            "background-color": "#F9F9F9",
                                            "margin": "2px",
                                            "padding": "2px",
                                            "textAlign": "center",
                                        },
                                    ),
                                    html.H5(
                                        "Total: Languages",
                                        style={
                                            "background-color": "#F9F9F9",
                                            "margin": "2px",
                                            "padding": "2px",
                                            "textAlign": "center",
                                        },
                                    ),
                                    html.H3(
                                        "{}".format(
                                            len(df[["main_genre"]].drop_duplicates())
                                        ),
                                        id="total_genre",
                                        style={
                                            "background-color": "#F9F9F9",
                                            "margin": "2px",
                                            "padding": "2px",
                                            "textAlign": "center",
                                        },
                                    ),
                                    html.H5(
                                        "Total: Genre",
                                        style={
                                            "background-color": "#F9F9F9",
                                            "margin": "2px",
                                            "padding": "2px",
                                            "textAlign": "center",
                                        },
                                    ),
                                ],
                                style={
                                    "background-color": "#F9F9F9",
                                    "margin": "15px",
                                    "padding": "15px",
                                    "border": "1px solid #F9F9F9",
                                    "border-radius": "10px",
                                    "display": "inline-block",
                                    "textAlign": "center",
                                },
                            ),
                            html.Div(
                                [
                                    dcc.Graph(
                                        figure=px.scatter(
                                            agg_df_select,
                                            x=agg_df_select[x],
                                            y=agg_df_select[y],
                                            color=agg_df_select[color],
                                            size=agg_df_select[size],
                                            hover_name=agg_df_select["movieID"],
                                            title="Explore Movies",
                                        )
                                        .update_xaxes(title=x)
                                        .update_yaxes(title=y)
                                    )
                                ],
                                style={
                                    "background-color": "#F9F9F9",
                                    "margin": "15px",
                                    "padding": "15px",
                                    "border": "1px solid #F9F9F9",
                                    "border-radius": "10px",
                                    "display": "inline-block",
                                    "textAlign": "center",
                                },
                            ),
                            html.Div(
                                [
                                    dcc.Graph(
                                        figure=px.scatter(
                                            rank_df_select,
                                            x=rank_df_select["partitioned_rank"],
                                            y=rank_df_select[order_input],
                                            hover_name=agg_df_select["movieID"],
                                            title="Explore Rank",
                                        )
                                        .update_xaxes(title="Company Rank")
                                        .update_yaxes(title=order_input)
                                    )
                                ],
                                style={
                                    "background-color": "#F9F9F9",
                                    "margin": "15px",
                                    "padding": "15px",
                                    "border": "1px solid #F9F9F9",
                                    "border-radius": "10px",
                                    "display": "flex",
                                    "textAlign": "center",
                                },
                            ),
                        ],
                        style={"display": "flex"},
                    ),
                    html.H5(children=f"Raw Data Preview: {input_button_raw_data}"),
                    generate_table(dataframe=df_vis),
                ]
            )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
