import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


def get_layout(defaults):
    return dbc.Container([
        dbc.Container([
            html.H1("FCP - Simulating COVID-19"),
            html.H2("by Ollie Hooper, Abbie Backers, Josh Smith and Adam Morris"),
        ]),
        html.Br(),
        dbc.Container([
            dbc.InputGroup([
                dbc.InputGroupAddon("Size (Dimension)", addon_type="prepend"),
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
            dbc.InputGroup([
                dbc.InputGroupAddon("Average infection length", addon_type="prepend"),
                dbc.Input(value=defaults["length"], type="number", min=0, step=1, id="num-length"),
            ]),
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
                                            dbc.InputGroupAddon(f"Age < {age}", addon_type="prepend"),
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
            dbc.Button(
                "Measures",
                id="btn-measures",
                color="info",
            ),
            dbc.Collapse([
                dbc.Card([
                    dbc.Container([
                        html.H5(measure)
                    ]),
                    dbc.CardBody([
                        dbc.InputGroup([
                            dbc.Checklist(options=[
                                {"label": "Enable?", "value": 1}
                            ],
                                value=[1] if defaults["measures"][measure]["enabled"] else [],
                                id=f"num-measures-{measure}-enabled",
                                switch=True
                            ),
                        ]),
                        dbc.InputGroup([
                            dbc.InputGroupAddon("Start dates", addon_type="prepend"),
                            dbc.Input(value=str(defaults["measures"][measure]["starts"])[1:-1],
                                      id=f"num-measures-{measure}-starts"),
                        ]),
                        dbc.InputGroup([
                            dbc.InputGroupAddon("End dates", addon_type="prepend"),
                            dbc.Input(value=str(defaults["measures"][measure]["ends"])[1:-1],
                                      id=f"num-measures-{measure}-ends"),
                        ]),
                        dbc.InputGroup([
                            dbc.InputGroupAddon("Multiplier", addon_type="prepend"),
                            dbc.Input(value=defaults["measures"][measure]["multiplier"], type="number", min=0,
                                      step=0.01, id=f"num-measures-{measure}-multiplier"),
                        ])
                    ])
                ]) for measure, kwargs in defaults["measures"].items()
            ], is_open=False, id="clp-measures")
        ]),
        html.Br(),
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    dbc.Button("Run/Save animation", color="primary", id="btn-anim")
                ]),
                dbc.Col([
                    dbc.Input(placeholder="(Optional) File name to save animation - must end in .gif",
                              id="txt-anim-fname")
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Button("Plot", color="primary", id="btn-plot")
                ]),
                dbc.Col([
                    dbc.Input(placeholder="(Optional) File name to save plot - must end in .png", id="txt-plot-fname")
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label(id='lbl-status')
                ])
            ])
        ]),
        html.Br(),
        dbc.Container([
            html.Img(id="img-animation"),
            html.Img(id="img-age"),
            html.Img(id="img-plot"),
        ]),
        dbc.Container([
            dcc.Markdown(open('README.md', 'r').read())
        ])
    ])
