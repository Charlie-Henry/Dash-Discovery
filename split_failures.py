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

df = pd.read_csv("split_failures.csv")

# df = df[df["Time"] == "PM"]

df["Selection"] = df["Month"] + " - " + df["Year"].astype(str)


app_color = {"graph_bg": "#082255", "graph_line": "#007ACE"}

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div(
    [
        html.H1("Austin Split Failures", style={"text-align": "center"}),
        dcc.Dropdown(
            id="slct_year",
            options=[
                {"label": "February 2020", "value": "Feb - 2020"},
                {"label": "March 2020", "value": "Mar - 2020"},
                {"label": "April 2020", "value": "Apr - 2020"},
                {"label": "May 2020", "value": "May - 2020"},
                {"label": "June 2020", "value": "Jun - 2020"},
                {"label": "July 2020", "value": "Jul - 2020"},
                {"label": "August 2020", "value": "Aug - 2020"},
                {"label": "September 2020", "value": "Sep - 2020"},
                {"label": "October 2020", "value": "Oct - 2020"},
                {"label": "November 2020", "value": "Nov - 2020"},
                {"label": "December 2020", "value": "Dec - 2020"},
                {"label": "January 2021", "value": "Jan - 2021"},
                {"label": "February 2021", "value": "Feb - 2021"},
                {"label": "March 2021", "value": "Mar - 2021"},
                {"label": "April 2021", "value": "April - 2021"},
                {"label": "May 2021", "value": "May - 2021"},
                {"label": "June 2021", "value": "Jun - 2021"},
                {"label": "July 2021", "value": "Jul - 2021"},
                {"label": "August 2021", "value": "Aug - 2021"},
                {"label": "September 2021", "value": "Sep - 2021"},
                {"label": "October 2021", "value": "Oct - 2021"},
                {"label": "November 2021", "value": "Nov - 2021"},
                {"label": "December 2021", "value": "Dec - 2021"},
                {"label": "January 2022", "value": "Jan - 2022"},
                {"label": "February 2022", "value": "Feb - 2022"},
                {"label": "March 2022", "value": "Mar - 2022"},
                {"label": "April 2022", "value": "Apr - 2022"},
            ],
            multi=False,
            value="Apr - 2022",
            style={"width": "40%"},
        ),
        dcc.Dropdown(
            id="slct_time",
            options=[{"label": "AM", "value": "AM"}, {"label": "PM", "value": "PM"},],
            multi=False,
            value="PM",
            style={"width": "40%"},
        ),
        html.Div(id="output_container", children=[]),
        html.Br(),
        html.Div(
            children=[
                dcc.Graph(
                    id="map",
                    style={
                        "display": "inline-block",
                        "width": "100vh",
                        "height": "90vh",
                    },
                ),
                dcc.Graph(
                    id="scatter",
                    style={"display": "inline-block", "width": "60vh"},
                    figure=dict(
                        layout=dict(
                            plot_bgcolor=app_color["graph_bg"],
                            paper_bgcolor=app_color["graph_bg"],
                        )
                    ),
                ),
            ]
        )
        # dcc.Graph(id="map", figure={}, style={"height": "90vh", "width": "60vh"}),
        # dcc.Graph(id="scatter", figure={}, style={"height": "90vh", "width": "20vh"}),
    ]
)


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [
        Output(component_id="output_container", component_property="children"),
        Output(component_id="map", component_property="figure"),
        Output(component_id="scatter", component_property="figure"),
    ],
    [
        Input(component_id="slct_year", component_property="value"),
        Input(component_id="slct_time", component_property="value"),
    ],
)
def update_graph(option_slctd, time_slctd):
    print(option_slctd)
    print(type(option_slctd))

    # container = "The year chosen by user was: {}".format(option_slctd)

    container = f"The time chosen by user is: {option_slctd} - {time_slctd}"

    dff = df.copy()
    dff = dff[dff["Selection"] == option_slctd]
    dff = dff[dff["Time"] == time_slctd]

    # fig = px.scatter_geo(
    #     dff,
    #     lat="lat",
    #     lon="lon",
    #     color="splitFailurePct",
    #     size="totalVehicleVolume",
    #     scope="usa",
    # )

    fig = px.scatter_mapbox(
        dff,
        lat="lat",
        lon="lon",
        hover_name="name",
        hover_data=["totalVehicleVolume", "splitFailurePct"],
        color="splitFailurePct",
        size="totalVehicleVolume",
        # color_discrete_sequence=["fuchsia"],
        zoom=10,
    )
    fig.update_layout(mapbox_style="open-street-map")

    fig_sctter = px.scatter(
        dff, x="totalVehicleVolume", y="splitFailurePct", hover_data=["name"]
    )
    # fig.update_layout(margin = dict(t=50, l=25, r=25, b=25)),
    # fig.update_traces(root_color="lightgrey")
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

    return container, fig, fig_sctter
    # return fig


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run_server(debug=True)
