import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from matplotlib import pyplot as plt

from covid_sim.animation import Animation, plot_simulation
from covid_sim.simulator import Simulation
from web_app.layout import get_layout


def get_app():
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.title = "COVID Simulator"
    app.layout = get_layout()

    @app.callback(
        Output('lbl-status', 'children'),
        [Input('btn-run-anim', 'n_clicks'),
         Input('btn-plot', 'n_clicks'),
         Input('txt-plot-fname', 'value'),
         ]
    )
    def run(btn_run_anim, btn_plot, plot_fname):
        ctx = dash.callback_context

        if not ctx.triggered:
            raise PreventUpdate()
        else:
            btn = '-'.join(ctx.triggered[0]['prop_id'].split('.')[0].split('-')[1:])

        # Set up the simulation
        simulation = Simulation(50, 50, 0.1, 0.1, 0.005)
        simulation.infect_randomly(2)

        if btn == 'run-anim':
            animation = Animation(simulation, 100)
            animation.show()
        elif btn == 'plot':
            fig = plot_simulation(simulation, 100)

            if plot_fname is None:
                plt.show()
            else:
                fig.savefig(plot_fname)

        return "Finished animation"

    return app
