import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


def get_layout(defaults):
    return dbc.Container([
        dbc.Container([
            html.H1("COVID Simulator"),
            html.H2("by Ollie Hooper, Abbie Backers, Josh Smith and Adam Morris"),
        ]),
        html.Br(),
        dbc.Container([
            dbc.InputGroup([
                dbc.InputGroupAddon("Size", addon_type="prepend"),
                dbc.Input(value=defaults["size"], type="number", min=0, step=1, id="num-size"),
            ]),
            dbc.InputGroup([
                dbc.InputGroupAddon("Duration", addon_type="prepend"),
                dbc.Input(value=defaults["duration"], type="number", min=0, step=1, id="num-duration"),
            ]),
            dbc.InputGroup([
                dbc.InputGroupAddon("Initial cases", addon_type="prepend"),
                dbc.Input(value=defaults["cases"], type="number", min=0, step=1, id="num-cases"),
            ])
        ]),
        html.Br(),
        dbc.Container([
            dbc.Button(
                "Probabilities",
                id="btn-probabilities",
                color="info",
            ),
            dbc.Collapse([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                dbc.Label(prob),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.InputGroup([
                                            dbc.InputGroupAddon(f"< {age}", addon_type="prepend"),
                                            dbc.Input(value=p, type="number", min=0, step=0.01,
                                                      id=f"num-{prob}-{age}"),
                                        ])
                                    ]) for age, p in probs.items()
                                ])
                            ]) for prob, probs in defaults["probabilities"].items()
                        ])
                    ])
                ])
            ], is_open=True, id="clp-probabilities")
        ]),
        html.Br(),
        dbc.Container([
            dbc.Button(
                "Vaccinator",
                id="btn-vaccinator",
                color="info",
            ),
            dbc.Collapse([
                dbc.Card([
                    dbc.CardBody([
                        dbc.InputGroup([
                            dbc.InputGroupAddon("Start day", addon_type="prepend"),
                            dbc.Input(value=defaults["vaccinator"]["start"], type="number", min=0, step=1,
                                      id="num-vaccinator-start"),
                        ]),
                        dbc.InputGroup([
                            dbc.InputGroupAddon("Vaccination capacity increase rate (per day)",
                                                addon_type="prepend"),
                            dbc.Input(value=defaults["vaccinator"]["rate"], type="number", min=0, step=0.01,
                                      id="num-vaccinator-rate"),
                        ]),
                        dbc.InputGroup([
                            dbc.InputGroupAddon("Max vaccination capacity (per day)", addon_type="prepend"),
                            dbc.Input(value=defaults["vaccinator"]["max"], type="number", min=0, step=1,
                                      id="num-vaccinator-max"),
                        ]),
                    ])
                ])
            ], is_open=True, id="clp-vaccinator")
        ]),
        html.Br(),
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    dbc.Button("Run/Save animation", color="primary", id="btn-anim")
                ]),
                dbc.Col([
                    dbc.Input(placeholder="(Optional) File name to save animation", id="txt-anim-fname")
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Button("Plot", color="primary", id="btn-plot")
                ]),
                dbc.Col([
                    dbc.Input(placeholder="(Optional) File name to save plot", id="txt-plot-fname")
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label(id='lbl-status')
                ])
            ])
        ])
    ])
