from dash import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from src.visualization.visualize import *
from src.dash import app  # check comment in generatePlot function

"""
This file contains all of the components used within the dashboard.
Each function is organized as follows:

class <DivName>:
    def get<ChildComponent>
    @app.callback for <ChildComponent>

"""

ASSET_PATH = "src/dash/assets/images"


class mainContainer:
    """
    Class housing all of the items to be stored within the main container.
    """

    def serve(self) -> any:
        """
        Defines and returns the container in which everything is housed.
        """
        return html.Div(
            id="main-container",
            children=[
                self.getBanner(),
                self.getMainPlot(),
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
                    id="logo", src=app.get_asset_url("space_dashboard_black_24dp.svg")
                ),
                html.H2("DiaDash Application", id="banner-title"),
            ],
        )

    def getButtonRow() -> any:
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

    def getMainPlot(plot: any) -> any:
        """
        Defines and returns the div containing a basic plot for the time being.

        ## Parameters:
        `plot` any:
            The plot to insert into the main plot Div
        """
        return html.Div(id="graph-container", children=[mainContainer.getTabs()])

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
        pass


def serve_layout() -> list:
    """
    Returns layout containing components back to the app.
    """
    return []
