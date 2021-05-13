import dash
import dash_bootstrap_components as dbc

from web_app.layout import get_layout


def get_app():
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.title = "COVID Simulator"
    app.layout = get_layout()
    return app
