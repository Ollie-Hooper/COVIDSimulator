import dash
import dash_html_components as html


def get_app():
    app = dash.Dash(__name__)
    app.title = "COVID Simulator"
    app.layout = html.Div()
    return app
