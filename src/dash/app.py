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
    # assets_url_path="src/dash/assets/"
    external_stylesheets=[dbc.themes.MORPH],
)

app.title = "DiaDash"

# ---------------------------------------------------------------------------------------

ASSET_PATH = "src/dash/assets/images"

"""
This file contains all of the components used within the dashboard.
Each class is organized as follows:

class <MajorDivName>:
    def get<ChildComponent>
    @app.callback for <ChildComponent>

"""


class mainContainer:
    """
    Class housing all of the items to be stored within the main container.
    """

    def serve() -> any:
        """
        Defines and returns the container in which everything is housed.
        """
        return html.Div(
            id="main-container",
            children=[
                mainContainer.getBanner(),
                mainContainer.getButtonGroup(),
            ],
        )

    def getBanner() -> any:
        """
        Defines and returns the banner div and its child components.
        """
        return html.Div(
            id="banner",
            children=[
                html.Img(
                    id="logo",
                    src=app.get_asset_url(
                        ASSET_PATH + "space_dashboard_black_48dp.svg"
                    ),
                ),
                html.H2("DiaDash Application", id="banner-title"),
            ],
        )

    def getButtonGroup() -> any:
        """
        Defines and returns the row of buttons that control which graph is shown.
        """
        button_group = html.Div(
            [
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
                ),
                html.Div(id="output"),
            ],
            className="radio-group",
        )
        return button_group

    @app.callback(Output("output", "children"), [Input("view-radios", "value")])
    def generatePlot(value) -> any:
        """
        @app.callback is not defined because it is not in the app.py itself. -- attempted import to fix this.
        Determines which plot to generate based on the Radio button selected.
        """
        if value == 1:
            return mainContainer.getWeeklyPlot()
        elif value == 2:
            return mainContainer.getDailyPlot()
        elif value == 3:
            return mainContainer.unknownView()
        pass

    def getMainPlot() -> any:
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

    def getWeeklyPlot() -> any:
        """
        Defines and returns the weekly view of the plot.
        """
        pass

    def getDailyPlot() -> any:
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
        return html.Div(id="sidebar", children=[])


# ---------------------------------------------------------------------------------------


def serve_layout() -> list:
    """
    Returns layout containing components back to the app.
    """
    return []


# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

app.layout = html.Div(
    children=[
        mainContainer.getBanner(),
        mainContainer.getButtonGroup(),
        mainContainer.getMainPlot(),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
