import dash

from web_app.layout import get_layout


def get_app():
    app = dash.Dash(__name__)
    app.title = "COVID Simulator"
    app.layout = get_layout()
    return app
