import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate

from covid_sim.animation import Animation
from covid_sim.simulator import Simulation
from web_app.layout import get_layout


def get_app():
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.title = "COVID Simulator"
    app.layout = get_layout()

    @app.callback(
        Output('lbl-status', 'children'),
        [Input('btn-run-anim', 'n_clicks')]
    )
    def run_animation(n_clicks):
        if not n_clicks:
            raise PreventUpdate()

        # Set up the simulation
        simulation = Simulation(50, 50, 0.1, 0.1, 0.005)
        simulation.infect_randomly(2)

        animation = Animation(simulation, 100)
        animation.show()

        return "Finished animation"

    return app
