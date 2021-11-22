# Dash specific imports.
from dash import dcc
from dash import Input, Output
import dash_bootstrap_components as dbc

# Internal Application Imports
from app import app
from apps import home, login


# Basic layout definition
app.layout = dbc.Container(
    id="page-content", children=[dcc.Location(id="url", refresh=False)]
)


# Callback to change which page to display
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname) -> any:
    """
    Placeholder description
    """
    if pathname == "/":
        return login.serve_layout()
    if pathname == "/board":
        return home.serve_layout()


if __name__ == "__main__":
    app.run_server(debug=True)
