# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

# Dash specific imports.
from typing import Type
import dash
from dash import dcc
from dash import html
import plotly.express as px
from dash import Input, Output, State
import dash_bootstrap_components as dbc

# Other Imports
import pandas as pd

# Local imports
from src.data import update
from src.visualization.visualize import *


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


class splashComponents:
    """
    Class housing all of the components available on the login landing page.
    """

    def serve() -> any:
        """
        Gets and returns all of the components for the splash login screen.
        """
        return splashComponents.getLogin()

    def getLogin() -> any:
        """
        Defines and returns the login components
        """
        login_form = dbc.Container(
            [
                dbc.Col(
                    [
                        html.Br(),
                        html.Img(
                            id="login-logo",
                            src=app.get_asset_url(
                                "images/space_dashboard_black_48dp.svg",
                            ),
                        ),
                        html.Br(),
                        # This is where we would start the dbc.Form method
                        dbc.Row(
                            [
                                dbc.FormFloating(
                                    [
                                        # Username input field
                                        dbc.Row(
                                            [
                                                dbc.Input(
                                                    id="login-field",
                                                    type="login",
                                                    placeholder="Username",
                                                ),
                                                dbc.Label(
                                                    "Medtronic CareLink Username"
                                                ),
                                            ]
                                        ),
                                        # Password input field
                                        dbc.Row(
                                            [
                                                dbc.Input(
                                                    id="password-field",
                                                    type="password",
                                                    placeholder="Password",
                                                ),
                                                dbc.Label(
                                                    "Medtronic CareLink Password"
                                                ),
                                            ]
                                        ),
                                        html.Br(),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        dbc.Button(
                                                            "Login",
                                                            id="login-button",
                                                            color="primary",
                                                            className="me-1",
                                                            type="button",
                                                            style={"width": "150px"},
                                                        )
                                                    ],
                                                    className="d-flex justify-content-center",
                                                )
                                            ]
                                        ),
                                    ]
                                )
                            ]
                        ),
                        html.Br(),
                        dbc.Row(
                            [html.P(id="temp-out")],
                            className="d-flex justify-content-center",
                        ),
                        dbc.Row([dbc.Spinner(html.Div(id="loading-spinner"))]),
                    ],
                    width=3,
                ),
            ],
            className="h-50 p-20 align-items-center justify-content-center display-flex",
            style={"display": "flex"},
        )

        return login_form

    # Callback to show the spinner when the login/download button is pressed.
    @app.callback(
        Output("loading-spinner", "children"), [Input("login-button", "n_clicks")]
    )
    # Callback to send the values from the user and pwd fields to the update interface.
    @app.callback(
        Output("temp-out", "children"),
        [
            Input("login-button", "n_clicks"),
            State("login-field", "value"),
            State("password-field", "value"),
        ],
    )
    def onLoginClick(n_clicks, user, token) -> any:
        """
        Just a testing method for understanding how the data flows with the dbc.Form
        """
        if n_clicks == None:
            return "You have not logged in yet"
        else:
            try:
                return user + token
                # TODO: Fill out the comments below
                # update.main(user, token)
                # show check mark confirming data downloaded
                # show main app page
                # return green check or something affirmative
            except ValueError:
                return html.P()  # Show login error message
            except:
                return html.P()  # Unknown error, try again later.

    def handleLoginFormInput(user, token) -> any:
        """
        Callback function for the login container.
        Takes input from the login form and passes it to the MLC interface.

        ## Parameters:
            `usr` str: Username specified by the input form.
            `pwd` str: Password specified by the input form.

        ## Returns:
            Spinner
        """

        """
        Logic Notes.
        1. Cast each input to a string if necessary (will be removed after testing)
        2. Send input to the update.py -- will have to import the main function from update.py
            - update.py/mcl_interface will have to be adapted to accept explicit arguments
            - will just use the already written set methods that exist within the interface.
        3. If a value error occurs then we know its a credentialing issue
        4. Otherwise it will be considered an unknown error.
        """

        # This will be removed after testing. Can never be too safe.
        try:
            assert type(user) == "String"
            assert type(token) == "String"
        except:
            usr = str(user)
            pwd = str(token)

        # Sending input to the data updating function
        try:
            update.main(user, token)
        except ValueError:
            print()  # TODO: Print that the username or password are inccorrect.
        pass


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
                        dbc.FormFloating(
                            [
                                dbc.Input(type="bg-lower-bound", placeholder=120),
                                dbc.Label("mg/dL lower bound"),
                            ]
                        )
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        dbc.FormFloating(
                            [
                                dbc.Input(type="bg-upper-bound", placeholder=120),
                                dbc.Label("mg/dL upper bound"),
                            ]
                        )
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
                sidebarContainer.createCard("Time in Range", "Value"),
                sidebarContainer.createCard("Average mg/dL", "Value"),
            ]
        )

        row2 = dbc.Row(
            [
                sidebarContainer.createCard("Highest Avg. Day", "Value"),
                sidebarContainer.createCard("Lowest Avg. Day", "Value"),
            ]
        )

        row3 = dbc.Row(
            [
                sidebarContainer.createCard("Carbs Consumed", "Value"),
                sidebarContainer.createCard("Insulin Dosed", "Value"),
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


def serve_main_page() -> list:
    """
    Returns layout containing the main application.
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


def serve_login_page() -> list:
    """
    Returns layout containing the login page.
    """
    return [splashComponents.serve()]


app.layout = dbc.Container(children=serve_login_page())

if __name__ == "__main__":
    app.run_server(debug=True)
