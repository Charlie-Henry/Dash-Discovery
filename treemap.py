import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import (
    Dash,
    dcc,
    html,
    Input,
    Output,
)  # pip install dash (version 2.0.0 or higher)


app = Dash(__name__)

df = pd.read_excel("ATD FY20_21 Det Exp v Budget.xlsx")

df = df[df["Budget 2021"] > 0]
df = df[df["Budget 2020"] > 0]

df = df[df["Unit Name"] != "Transfers"]

# df = df[
#    df["Unit Name"].isin(
#        ["Smart Mobility", "Transportation Systems Development", "Arterial Management"]
#    )
# ]

df = df[["Unit Name", "Object Code Category", "Obj Code", "Budget 2020", "Budget 2021"]]

df = df.rename(columns={"Budget 2020": 2020, "Budget 2021": 2021})

df = df.melt(
    id_vars=["Unit Name", "Object Code Category", "Obj Code"],
    var_name="Year",
    value_name="Value",
)

df["Year"] = df["Year"].astype(int)


# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div(
    [
        html.H1("Web Application Dashboards with Dash", style={"text-align": "center"}),
        dcc.Dropdown(
            id="slct_year",
            options=[
                {"label": "2020", "value": 2020},
                {"label": "2021", "value": 2021},
            ],
            multi=False,
            value=2020,
            style={"width": "40%"},
        ),
        html.Div(id="output_container", children=[]),
        html.Br(),
        dcc.Graph(id="treemap", figure={}, style={"height": "75vh"}),
    ]
)


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [
        Output(component_id="output_container", component_property="children"),
        Output(component_id="treemap", component_property="figure"),
    ],
    [Input(component_id="slct_year", component_property="value")],
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The year chosen by user was: {}".format(option_slctd)

    dff = df.copy()
    dff = dff[dff["Year"] == option_slctd]

    fig = px.treemap(
        dff,
        path=[
            px.Constant("Austin Transportation Department Budget"),
            "Unit Name",
            "Object Code Category",
            "Obj Code",
        ],
        values="Value",
        maxdepth=2,
    )
    # fig.update_layout(margin = dict(t=50, l=25, r=25, b=25)),
    fig.update_traces(root_color="lightgrey")
    # fig.show()

    # Plotly Express
    # fig = px.choropleth(
    #     data_frame=dff,
    #     locationmode="USA-states",
    #     locations="state_code",
    #     scope="usa",
    #     color="Pct of Colonies Impacted",
    #     hover_data=["State", "Pct of Colonies Impacted"],
    #     color_continuous_scale=px.colors.sequential.YlOrRd,
    #     labels={"Pct of Colonies Impacted": "% of Bee Colonies"},
    #     template="plotly_dark",
    # )

    # Plotly Graph Objects (GO)
    # fig = go.Figure(
    #     data=[go.Choropleth(
    #         locationmode='USA-states',
    #         locations=dff['state_code'],
    #         z=dff["Pct of Colonies Impacted"].astype(float),
    #         colorscale='Reds',
    #     )]
    # )
    #
    # fig.update_layout(
    #     title_text="Bees Affected by Mites in the USA",
    #     title_xanchor="center",
    #     title_font=dict(size=24),
    #     title_x=0.5,
    #     geo=dict(scope='usa'),
    # )

    return container, fig
    # return fig


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run_server(debug=True)
