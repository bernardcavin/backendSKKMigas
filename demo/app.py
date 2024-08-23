from dash import Dash, html, dcc, callback, Output, Input, _dash_renderer
import dash_mantine_components as dmc

_dash_renderer._set_react_version("18.2.0")

app = Dash()

app.layout = [
    dmc.MantineProvider(
        dmc.Card(
            [
                dmc.SimpleGrid(
                    [
                        dmc.NumberInput(
                            label='Open Hole Size'
                        ),
                    ],
                    cols = 3
                )
            ]
        )
    )
]

if __name__ == '__main__':
    app.run(debug=True)