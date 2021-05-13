import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from matplotlib import pyplot as plt

from covid_sim.animation import Animation, plot_simulation
from covid_sim.simulator import Simulation
from web_app.layout import get_layout


def get_app(defaults):
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.title = "COVID Simulator"
    app.layout = get_layout(defaults=defaults)

    @app.callback(
        Output('lbl-status', 'children'),
        [Input('btn-anim', 'n_clicks'),
         Input('btn-plot', 'n_clicks')],
        [State('txt-anim-fname', 'value'),
         State('txt-plot-fname', 'value'),
         State('num-size', 'value'),
         State('num-duration', 'value'),
         State('num-cases', 'value')]
    )
    def run(btn_anim, btn_plot, anim_fname, plot_fname, *args):
        ctx = dash.callback_context

        if not ctx.triggered:
            raise PreventUpdate()
        else:
            btn = '-'.join(ctx.triggered[0]['prop_id'].split('.')[0].split('-')[1:])

        input_names = defaults.keys()
        kwargs = dict(zip(input_names, args))

        # Set up the simulation
        simulation = Simulation(kwargs["size"], kwargs["size"], 0.1, 0.1, 0.005)
        simulation.infect_randomly(kwargs["cases"])

        if btn == 'anim':
            animation = Animation(simulation, duration=kwargs["duration"])

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

    @app.callback(
        Output("clp-probabilities", "is_open"),
        [Input("btn-probabilities", "n_clicks")],
        [State("clp-probabilities", "is_open")],
    )
    def toggle_probabilities_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    return app
