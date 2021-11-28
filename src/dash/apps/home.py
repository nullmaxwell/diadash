# Dash specific imports.
from typing import Type
from dash import dcc
from dash import html
from dash_bootstrap_components._components.Row import Row
import plotly.express as px
from dash import Input, Output, State
import dash_bootstrap_components as dbc

# Internal Application Imports
from app import app
from src.data.update import metrics
from src.pipelines.pipelines import WeeklyDataPipeline
from src.statistics.statistics import Stats

# Other imports
import pandas as pd

# Global Variable for Processed data
PROCESSED_DATA = None

try:
    PROCESSED_DATA = WeeklyDataPipeline.pipe()
except FileNotFoundError:
    PROCESSED_DATA = None


def serve_layout() -> list:
    """
    Returns layout containing the main application.
    """
    return [
        generalComponents.getNavBar(),
        dbc.Row(
            [
                dbc.Col(
                    id="main-container",
                    children=[
                        mainContainer.getButtonGroup(),
                        html.Br(style={"margin": "53px"}),
                        dbc.Row(id="card-row"),
                    ],
                    width=8,
                ),
                dbc.Col(
                    id="sidebar-container",
                    children=[
                        sidebarContainer.getSidebarHeader(),
                        html.Div(id="card-grid"),
                    ],
                    width=4,
                    style={"border-left": "black"},
                ),
            ]
        ),
    ]


class generalComponents:
    """
    Class housing all of the general components.
    """

    def getNavBar() -> any:
        """
        Defines and returns the NavBar of the dashboard.
        """
        navbar = dbc.Navbar(
            dbc.Container(
                [
                    html.A(
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Img(
                                        id="navbar-logo",
                                        src=app.get_asset_url(
                                            "images/space_dashboard_black_48dp.svg"
                                        ),
                                    ),
                                    width=2,
                                ),
                                dbc.Col(
                                    dbc.NavbarBrand(
                                        "DiaDash Application", className="ms-2"
                                    ),
                                    width=6,
                                ),
                            ],
                            align="center",
                            className="g-0",
                        ),
                    ),
                    dbc.DropdownMenu(
                        children=[
                            dbc.DropdownMenuItem("Additional Resources", header=True),
                            dbc.DropdownMenuItem("Medtronic CareLink", href="#"),
                            dbc.DropdownMenuItem("Source Code", href="#"),
                            dbc.DropdownMenuItem(
                                dcc.Link("Logout", href="/", refresh=True)
                            ),
                        ],
                        nav=True,
                        in_navbar=True,
                        label="Additional Resources",
                    ),
                ]
            )
        )
        return navbar

    def createCard(header: str, value: str) -> any:
        """
        Wrapper function that defines the content of a card
        based on a value and provided header.
        """
        content = [
            dbc.CardHeader(
                header,
                style={"width": "190px", "height": "75px"},
                className="align-items-center d-flex justify-content-center",
            ),
            dbc.CardBody(
                [
                    html.P(
                        value,
                        className="card-body align-items-center d-flex justify-content-center",
                        style={"height": "75px"},
                    )
                ],
            ),
        ]

        card = dbc.Col(
            dbc.Card(
                content,
                color="secondary",
                outline=True,
                className="card-body align-items-center d-flex justify-content-center",
                style={"height": "190px", "width": "190px"},
            )
        )

        return card


class mainContainer:
    """
    Class housing all of the items to be stored within the main container.
    """

    def getButtonGroup() -> any:
        """
        Defines and returns the row of buttons that control which graph is shown.
        """
        button_group = html.Div(
            [
                html.Br(),
                dbc.RadioItems(
                    id="view-radios",
                    className="btnGroup",
                    input_class_name="btn-check",
                    labelClassName="btn btn-outline-secondary",
                    labelCheckedClassName="active",
                    options=[
                        {"label": "Weekly View", "value": 1},
                        {"label": "Daily View", "value": 2},
                        {"label": "Unknown View", "value": 3},
                    ],
                    value=1,
                    labelStyle={"display": "inline-block"},
                    inline=True,
                ),
                html.Br(),
                html.Div(id="output"),
            ],
            className="radio-group",
        )
        return button_group

    @app.callback(Output("output", "children"), [Input("view-radios", "value")])
    def generatePlot(value) -> any:
        """
        Determines which plot to generate based on the Radio button selected.
        """
        if value == 1:
            return mainContainer.getWeeklyView()
        elif value == 2:
            return mainContainer.getDailyView()
        elif value == 3:
            return mainContainer.unknownView()
        pass

    def getTestPlot() -> any:
        """
        Defines and returns the div containing a basic plot for the time being.

        ## Parameters:
        `plot` any:
            The plot to insert into the main plot Div
        """
        df = pd.DataFrame(
            {
                "Fruit": [
                    "Apples",
                    "Oranges",
                    "Bananas",
                    "Apples",
                    "Oranges",
                    "Bananas",
                ],
                "Amount": [4, 1, 2, 2, 4, 5],
                "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"],
            }
        )

        fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
        return dcc.Graph(id="example-graph", figure=fig)

    def getWeeklyView() -> any:
        """
        Defines and returns the weekly view of the plot.
        """

        tab1_content = mainContainer.getTestPlot()
        tab2_content = None
        tab3_content = None

        tabs = dbc.Tabs(
            [
                dbc.Tab(tab1_content, label="Line Plot"),
                dbc.Tab(tab2_content, label="Violin Plot"),
                dbc.Tab(tab3_content, label="Heat Map"),
            ]
        )

        return tabs

    def getDailyView() -> any:
        """
        Defines and returns the daily view of the plot.
        """
        pass

    def unknownView() -> any:
        """
        A yet to be determined view. This is a placeholder function for the time being.
        """
        pass

    def getCardRow(stats_obj: Stats) -> any:
        """
        Defines and returns the row of cards
        """
        card_row = dbc.Row(
            [
                generalComponents.createCard("Time in Range", stats_obj.tir),
                generalComponents.createCard("Time high", stats_obj.timeHigh),
                generalComponents.createCard("Time low", stats_obj.timeLow),
                generalComponents.createCard("Average mg/dL", stats_obj.avgBG),
            ]
        )

        return card_row


class sidebarContainer:
    """
    Class housing all of the items to be created and generated within the sidebar container.
    """

    def getSidebarHeader() -> any:
        """
        Defines and returns a header with some basic text explanation.
        """
        title = html.H3("Stats at a Glance", style={"text-align": "center"})

        bg_bounds_form = dbc.Row(
            [
                dbc.Row(
                    [
                        dbc.Label(
                            "Target Blood Sugar Range (mg/dL)", html_for="bg-slider"
                        ),
                        dcc.RangeSlider(
                            id="bg-target-slider",
                            min=70,
                            max=200,
                            step=5,
                            value=[80, 150],
                            allowCross=False,
                            tooltip={"placement": "bottom", "always_visible": False},
                            marks={
                                70: {"label": "70 mg/dL"},
                                200: {"label": "200 mg/dL"},
                            },
                        ),
                    ],
                ),
                html.Br(style={"margin": "20px"}),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.FormFloating(
                                    [
                                        dbc.Input(
                                            id="daily-basal-amount",
                                            type="number",
                                            placeholder=120,
                                        ),
                                        dbc.Label("Basal Units per day"),
                                    ]
                                ),
                            ],
                            width=8,
                        ),
                        # TODO: This is where the toast notification column will go
                        dbc.Col(
                            [
                                dbc.Button(
                                    id="refresh-button",
                                    children=[
                                        html.Img(
                                            id="refresh-icon",
                                            src=app.get_asset_url(
                                                "images/update_black_48dp.svg",
                                            ),
                                            style={
                                                "height": "30px",
                                                "padding-bottom": "13px",
                                            },
                                        ),
                                    ],
                                    color="info",
                                    className="d-flex justify-content-center",
                                    type="button",
                                    style={"width": "45px", "height": "45px"},
                                    n_clicks=0,
                                ),
                            ],
                            width=3,
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        html.Br(),
                        # TODO: Add information toast explaining how to use this stuff.
                    ],
                    className="d-flex justify-content-center",
                ),
            ]
        )

        sidebar_header = html.Div(
            [html.Br(style={"margin": "10px"}), title, html.Br(), bg_bounds_form]
        )

        return sidebar_header

    # Output of this slider must be the div ID of the card row below graph and card grid
    @app.callback(
        Output("card-row", "children"),
        Output("card-grid", "children"),
        [
            Input("refresh-button", "n_clicks"),
            State("bg-target-slider", "value"),
            State("daily-basal-amount", "value"),
        ],
    )
    def onRefreshClick(n_clicks, s_arr, daily_basal_amount) -> any:
        """
        Updates all of stat cards based on the provided values.
        """
        global PROCESSED_DATA

        # Where the button has not yet been clicked
        if n_clicks == 0:
            # will need to pass daily_basal_amount to stats
            stats_obj = Stats(PROCESSED_DATA, s_arr[0], s_arr[1], 0)
            return mainContainer.getCardRow(stats_obj), sidebarContainer.getCardGrid(
                stats_obj
            )
        # Where the button is being clicked for the first time
        if n_clicks == 1:
            # attempt pipeline again
            stats_obj = WeeklyDataPipeline.pipe()
            temp = Stats(PROCESSED_DATA, s_arr[0], s_arr[1], daily_basal_amount)
            return mainContainer.getCardRow(stats_obj), sidebarContainer.getCardGrid(
                stats_obj
            )
        # Any time after that
        else:
            stats_obj = Stats(PROCESSED_DATA, s_arr[0], s_arr[1], daily_basal_amount)
            return mainContainer.getCardRow(stats_obj), sidebarContainer.getCardGrid(
                stats_obj
            )

    def getCardGrid(stats_obj: Stats) -> any:
        """
        Defines and returns a grid of cards to display stats on.
        """
        row1 = dbc.Row(
            [
                generalComponents.createCard("Time in Range", stats_obj.tir),
                generalComponents.createCard("Average mg/dL", stats_obj.avgBG),
            ]
        )

        row2 = dbc.Row(
            [
                generalComponents.createCard("Highest Avg. Day", stats_obj.highestDay),
                generalComponents.createCard("Lowest Avg. Day", stats_obj.lowestDay),
            ]
        )

        row3 = dbc.Row(
            [
                generalComponents.createCard("Carbs Consumed", stats_obj.carbsConsumed),
                generalComponents.createCard("Insulin Dosed", stats_obj.insulinTotal),
            ]
        )

        grid = [html.Br(), row1, html.Br(), row2, html.Br(), row3, html.Br()]
        return grid
