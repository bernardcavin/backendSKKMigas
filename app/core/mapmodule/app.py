from flask import Flask
import dash
from dash import dcc, html
import dash_mantine_components as dmc
import app.core.mapmodule.apdps_map as apdps_map

dash._dash_renderer._set_react_version("18.2.0")

stylesheets = [
    "https://unpkg.com/@mantine/dates@7/styles.css",
    "https://unpkg.com/@mantine/code-highlight@7/styles.css",
    "https://unpkg.com/@mantine/charts@7/styles.css",
    "https://unpkg.com/@mantine/carousel@7/styles.css",
    "https://unpkg.com/@mantine/notifications@7/styles.css",
    "https://unpkg.com/@mantine/nprogress@7/styles.css",
]

server = Flask(__name__)
app = dash.Dash(
    __name__, 
    server=server, 
    suppress_callback_exceptions=True, 
    external_stylesheets=stylesheets, 
    update_title=None,
    requests_pathname_prefix='/map/'
)

# app.scripts.config.serve_locally = True
# app.css.config.serve_locally = True

app.title = 'APDPS Map'

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

app.layout = dmc.MantineProvider(
    [
        html.Div(id='modal'),
        dmc.NotificationProvider(),
        html.Div(
            id='notif'
        ),
        dcc.Location(id='url', refresh=False),
        dcc.Location(id='redirect', refresh=True),
        html.Div(
            apdps_map.layout,
            id='page-container',
        ),
    ],
)

if __name__ == "__main__":
    app.run()
    
