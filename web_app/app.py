import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from matplotlib import pyplot as plt

from covid_sim.animation import Animation, plot_simulation
from covid_sim.simulator import Simulation
from web_app.functions import get_bottom_lvl_keys, unflatten_dict, parse_measures
from web_app.layout import get_layout


def get_app(defaults):
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])
    app.title = "COVID Simulator"
    app.layout = get_layout(defaults=defaults)

    @app.callback(
        [Output('lbl-status', 'children'),
         Output('img-animation', 'src'),
         Output('img-plot', 'src')],
        [Input('btn-anim', 'n_clicks'),
         Input('btn-plot', 'n_clicks')],
        [State('img-animation', 'src'),
         State('img-plot', 'src'),
         State('txt-anim-fname', 'value'),
         State('txt-plot-fname', 'value'),
         State('num-size', 'value'),
         State('num-duration', 'value'),
         State('num-cases', 'value'),
         State('num-length', 'value'),
         *[State(f'num-{prob}-{age}', 'value') for prob, probs in
           defaults["probabilities"].items() for age in
           probs.keys()],
         *[State(f'num-vaccinator-{k}', 'value') for k in defaults["vaccinator"].keys()],
         *[State(f'num-measures-{measure}-{k}', 'value') for measure, values in
           defaults["measures"].items() for k in
           values.keys()],
         ]
    )
    def run(btn_anim, btn_plot, anim_src, plot_src, anim_fname, plot_fname, *args):
        ctx = dash.callback_context

        if not ctx.triggered:
            raise PreventUpdate()
        else:
            btn = '-'.join(ctx.triggered[0]["prop_id"].split('.')[0].split('-')[1:])

        input_names = get_bottom_lvl_keys(defaults, [], [])
        kwargs = unflatten_dict(dict(zip(input_names, args)))

        kwargs = parse_measures(kwargs)

        # Set up the simulation
        simulation = Simulation(**kwargs)
        simulation.infect_randomly(kwargs["cases"])

        if btn == 'anim':
            animation = Animation(simulation, duration=kwargs["duration"])

            if anim_fname is None:
                animation.save("web_app/assets/anim.gif")
                return "Finished generating animation", app.get_asset_url("anim.gif"), plot_src
            else:
                animation.save(anim_fname)
                return f"Finished saving animation in {anim_fname}", anim_src, plot_src
        elif btn == 'plot':
            fig = plot_simulation(simulation, 100)

            if plot_fname is None:
                fig.savefig("web_app/assets/plot.png")
                return "Finished generating plot", anim_src, app.get_asset_url("plot.png")
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

    @app.callback(
        Output("clp-vaccinator", "is_open"),
        [Input("btn-vaccinator", "n_clicks")],
        [State("clp-vaccinator", "is_open")],
    )
    def toggle_vaccinator_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        Output("clp-measures", "is_open"),
        [Input("btn-measures", "n_clicks")],
        [State("clp-measures", "is_open")],
    )
    def toggle_measures_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    return app
