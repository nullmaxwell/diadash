# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

# Dash specific imports.
import dash
from dash import dcc
from dash import html
import plotly.express as px
from dash import Input, Output
import dash_bootstrap_components as dbc

# Other Imports
import pandas as pd


app = dash.Dash(
    __name__,
    assets_url_path="src/dash/assets",
    external_stylesheets=[dbc.themes.MORPH],
)

app.title = "DiaDash"

# ---------------------------------------------------------------------------------------

"""
Below contains all of the components used within the dashboard.
Each class is organized as follows:

class <MajorDivName>:
    def get<ChildComponent>
    @app.callback for <ChildComponent>

"""


class generalComponents:
    """
    Class housing all of the general components.
    """

    def serve() -> any:
        """
        Gets all of the general components and returns them as a list.
        """
        return generalComponents.getNavBar()

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
                        ],
                        nav=True,
                        in_navbar=True,
                        label="Additional Resources",
                    ),
                ]
            )
        )
        return navbar


class mainContainer:
    """
    Class housing all of the items to be stored within the main container.
    """

    def serve() -> any:
        """
        Defines and returns the container in which everything is housed.
        """
        return dbc.Col(
            id="main-container",
            children=[mainContainer.getButtonGroup()],
            width=8,
        )

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


class sidebarContainer:
    """
    Class housing all of the items to be created and generated within the sidebar container.
    I want the graph WITHIN the div to change based on the radio button. -- not produce a new div each time.
    """

    def serve() -> any:
        """
        Defines and returns the left container that contains the main graph and basic options.
        """
        return dbc.Col(
            id="sidebar-container",
            children=[
                sidebarContainer.getSidebarHeader(),
                sidebarContainer.getCardGrid(),
            ],
            width=4,
            style={"border-left": "black"},
        )

    def getSidebarHeader() -> any:
        """
        Defines and returns a header with some basic text explanation.
        """
        title = html.H3("Stats at a Glance", style={"text-align": "center"})

        bg_bounds_form = dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Input(type="bg-lower-bound", placeholder=90),
                        dbc.Label("mg/dL lower bound"),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        dbc.Input(type="bg-upper-bound", placeholder=120),
                        dbc.Label("mg/dL upper bound"),
                    ],
                    width=6,
                ),
            ]
        )

        sidebar_header = html.Div([html.Br(), title, html.Br(), bg_bounds_form])

        return sidebar_header

    def createCard(header: str, value: str) -> any:
        """
        Wrapper function that defines the content of a card
        based on a value and provided header.
        """
        content = [
            dbc.CardHeader(header),
            dbc.CardBody(
                [
                    html.P(
                        value,
                        className="card-body align-items-center d-flex justify-content-center",
                    )
                ]
            ),
        ]

        card = dbc.Col(
            dbc.Card(
                content,
                color="secondary",
                outline=True,
                className="card-body align-items-center d-flex justify-content-center",
            )
        )

        return card

    def getCardGrid() -> any:
        """
        Defines and returns a grid of cards to display stats on.
        """
        row1 = dbc.Row(
            [
                sidebarContainer.createCard("Metric", "Value"),
                sidebarContainer.createCard("Metric", "Value"),
            ]
        )

        row2 = dbc.Row(
            [
                sidebarContainer.createCard("Metric", "Value"),
                sidebarContainer.createCard("Metric", "Value"),
            ]
        )

        row3 = dbc.Row(
            [
                sidebarContainer.createCard("Metric", "Value"),
                sidebarContainer.createCard("Metric", "Value"),
            ]
        )

        # row4 = dbc.Row(
        #     [
        #         sidebarContainer.createCard("Metric", "Value"),
        #         sidebarContainer.createCard("Metric", "Value"),
        #     ]
        # )

        grid = html.Div([html.Br(), row1, html.Br(), row2, html.Br(), row3, html.Br()])
        return grid


# ---------------------------------------------------------------------------------------


def serve_layout() -> list:
    """
    Returns layout containing components back to the app.
    """
    return [
        generalComponents.getNavBar(),
        dbc.Row(
            [
                mainContainer.serve(),
                sidebarContainer.serve(),
            ]
        ),
    ]


app.layout = dbc.Container(children=serve_layout())

if __name__ == "__main__":
    app.run_server(debug=True)
