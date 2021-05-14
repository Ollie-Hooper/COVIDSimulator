import base64
import os

import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate

from covid_sim.animation import Animation, plot_simulation, plot_ages
from covid_sim.simulator import Simulation
from web_app.functions import get_bottom_lvl_keys, unflatten_dict, parse_measures
from web_app.layout import get_layout


def get_app(defaults):
    """Creates and returns a dash web app which controls the simulation"""

    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])
    app.title = "COVID Simulator"
    app.layout = get_layout(app=app, defaults=defaults)  # Get layout from layout.py

    @app.callback(
        [Output('lbl-status', 'children'),  # Output to status label to know when plot/animation generation has finished
         # Image outputs
         Output('img-animation', 'src'),
         Output('img-plot', 'src'),
         Output('img-age', 'src')],
        # Button inputs
        [Input('btn-anim', 'n_clicks'),
         Input('btn-plot', 'n_clicks')],
        # Retain images when callback fired
        [State('img-animation', 'src'),
         State('img-plot', 'src'),
         State('img-age', 'src'),
         # File name inputs
         State('txt-anim-fname', 'value'),
         State('txt-plot-fname', 'value'),
         # Basic parameter inputs
         State('num-size', 'value'),
         State('num-duration', 'value'),
         State('num-cases', 'value'),
         State('num-length', 'value'),
         # Probability inputs
         *[State(f'num-{prob}-{age}', 'value') for prob, probs in
           defaults["probabilities"].items() for age in
           probs.keys()],
         # Vaccinator inputs
         *[State(f'num-vaccinator-{k}', 'value') for k in defaults["vaccinator"].keys()],
         # Measures inputs
         *[State(f'num-measures-{measure}-{k}', 'value') for measure, values in
           defaults["measures"].items() for k in
           values.keys()],
         ]
    )
    def run(btn_anim, btn_plot, anim_src, plot_src, age_src, anim_fname, plot_fname, *args):
        ctx = dash.callback_context

        # Don't continue if no button pressed
        if not ctx.triggered:
            raise PreventUpdate()
        else:
            # Determine which button was pressed
            btn = '-'.join(ctx.triggered[0]["prop_id"].split('.')[0].split('-')[1:])

        # Process callback inputs into dictionary
        input_names = get_bottom_lvl_keys(defaults, [], [])
        kwargs = unflatten_dict(dict(zip(input_names, args)))

        kwargs = parse_measures(kwargs)  # Format parameters dictionary into proper form

        # Set up the simulation
        simulation = Simulation(**kwargs)
        simulation.infect_randomly(kwargs["cases"])

        if not os.path.exists("web_app/assets"):
            os.mkdir("web_app/assets")  # Set up assets folder

        # Plot age distribution
        fig_age = plot_ages(simulation)
        fig_age.savefig("web_app/assets/age.png")

        if btn == 'anim':  # Run animation
            animation = Animation(simulation, duration=kwargs["duration"])

            if anim_fname is None:
                animation.save("web_app/assets/anim.gif")  # Save animation as gif
                # Encode animation and age distribution plot
                encoded_anim = base64.b64encode(open("web_app/assets/anim.gif", "rb").read())
                encoded_age = base64.b64encode(open("web_app/assets/age.png", "rb").read())
                # Return these into the image html elements
                return "Finished generating animation", f"data:image/png;base64,{encoded_anim.decode()}", plot_src, \
                       f"data:image/png;base64,{encoded_age.decode()}"
            else:
                animation.save(anim_fname)  # Save animation
                # Notify user it has finished saving
                return f"Finished saving animation in {anim_fname}", anim_src, plot_src, age_src

        elif btn == 'plot':  # Run plot
            fig_simulation = plot_simulation(simulation, 100)

            if plot_fname is None:
                fig_simulation.savefig("web_app/assets/plot.png")
                # Encode simulation plot and age distribution plot
                encoded_plot = base64.b64encode(open("web_app/assets/plot.png", "rb").read())
                encoded_age = base64.b64encode(open("web_app/assets/age.png", "rb").read())
                # Return these into the image html elements
                return "Finished generating plot", anim_src, f"data:image/png;base64,{encoded_plot.decode()}", \
                       f"data:image/png;base64,{encoded_age.decode()}"
            else:
                fig.savefig(plot_fname)  # Save simulation plot
                # Notify user it has finished saving
                return f"Finished saving plot in {plot_fname}", anim_src, plot_src, age_src

    @app.callback(
        Output("clp-probabilities", "is_open"),
        [Input("btn-probabilities", "n_clicks")],
        [State("clp-probabilities", "is_open")],
    )
    def toggle_probabilities_collapse(n, is_open):
        """Toggles the probabilities collapse"""
        if n:
            return not is_open
        return is_open

    @app.callback(
        Output("clp-vaccinator", "is_open"),
        [Input("btn-vaccinator", "n_clicks")],
        [State("clp-vaccinator", "is_open")],
    )
    def toggle_vaccinator_collapse(n, is_open):
        """Toggles the vaccinator collapse"""
        if n:
            return not is_open
        return is_open

    @app.callback(
        Output("clp-measures", "is_open"),
        [Input("btn-measures", "n_clicks")],
        [State("clp-measures", "is_open")],
    )
    def toggle_measures_collapse(n, is_open):
        """Toggles the measures collapse"""
        if n:
            return not is_open
        return is_open

    return app
