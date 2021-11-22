# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

# Dash specific imports.
from typing import Type
import time
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
    title="DiaDash",
    assets_url_path="src/dash/assets",
    external_stylesheets=[dbc.themes.MORPH],
    suppress_callback_exceptions=True,
)

server = app.server
