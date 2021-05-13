import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


def get_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Container([

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
                            dbc.Button("Run animation", color="primary", id="btn-run-anim")
                        ])
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Save plot", color="secondary", id="btn-save-plot")
                        ]),
                        dbc.Col([
                            dbc.Input(placeholder="File name/location", id="txt-plot-fname")
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
