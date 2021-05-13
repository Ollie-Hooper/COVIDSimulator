import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


def get_layout(defaults):
    return dbc.Container([
        dbc.Row([
            dbc.Col([
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
                    ]),
                    dbc.Button(
                        "Probabilities",
                        id="btn-probabilities",
                        color="secondary",
                    ),
                    dbc.Collapse([
                        dbc.Card([
                            html.H5("Probabilities", className="card-title"),
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
                    ])
                ])
            ]),
            dbc.Col([
                dbc.Container([

                ])
            ]),
            dbc.Col([
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
                            dbc.Button("Plot", color="secondary", id="btn-plot")
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
                ], fluid=True)
            ])
        ])
    ], fluid=True)
