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
        [Input('btn-anim', 'n_clicks'),
         Input('btn-plot', 'n_clicks')],
        [State('txt-anim-fname', 'value'),
         State('txt-plot-fname', 'value')]
    )
    def run(btn_anim, btn_plot, anim_fname, plot_fname):
        ctx = dash.callback_context

        if not ctx.triggered:
            raise PreventUpdate()
        else:
            btn = '-'.join(ctx.triggered[0]['prop_id'].split('.')[0].split('-')[1:])

        # Set up the simulation
        simulation = Simulation(50, 50, 0.1, 0.1, 0.005)
        simulation.infect_randomly(2)

        if btn == 'anim':
            animation = Animation(simulation, 100)

            if anim_fname is None:
                animation.show()
                return "Finished showing animation"
            else:
                animation.save(anim_fname)
                return f"Finished saving animation in {anim_fname}"
        elif btn == 'plot':
            fig = plot_simulation(simulation, 100)

            if plot_fname is None:
                plt.show()
                return "Finished showing plot"
            else:
                fig.savefig(plot_fname)
                return f"Finished saving plot in {plot_fname}"

    return app
