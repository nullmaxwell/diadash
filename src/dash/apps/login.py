# Dash specific imports.
import time
from dash import dcc
from dash import html
from dash import Input, Output, State
import dash_bootstrap_components as dbc

# Internal Application Imports
from app import app


def serve_layout() -> any:
    """
    Gets and returns all of the components for the splash login screen.
    """
    return [getLogin()]


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
                                            dbc.Label("Medtronic CareLink Username"),
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
                                            dbc.Label("Medtronic CareLink Password"),
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
                                                        n_clicks=0,
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
                        [dbc.Container(id="status-container")],
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


# # Callback to show the spinner when the login/download button is pressed.
@app.callback(
    Output("status-container", "children"), [Input("login-button", "n_clicks")]
)
# Callback to send the values from the user and pwd fields to the update interface.
@app.callback(
    Output("loading-spinner", "children"),
    [
        Input("login-button", "n_clicks"),
        State("login-field", "value"),
        State("password-field", "value"),
    ],
)
def onLoginClick(n_clicks, user, token) -> any:
    """
    Callback function for the login container.
    Takes input from the login form and passes it to the MLC interface.

    ## Parameters:
        `usr` str: Username specified by the input form.
        `pwd` str: Password specified by the input form.

    ## Returns:
        If completely successful have an alert directing user to main application.
        If any failure occurs the GUI will show the appropriate error.
    """
    if n_clicks == None:
        return
    else:
        try:
            # update.main(user, token)
            time.sleep(2)  # to sim something happening in background
            return dbc.Alert(
                dcc.Link(
                    "Data download successful!\n\nClick here to continue to the dashboard.",
                    href="/board",
                    refresh=True,
                ),
                color="success",
            )
        except ValueError:
            return dbc.Alert(
                "Invalid Username or Password. Please try again.",
                color="danger",
                duration=3,
            )
        except:
            return dbc.Alert(
                "Data download failure due to unknown error! Please try again later.",
                color="danger",
                duration=3,
            )
