# Run:  python app.py   (from the project root)
# Deps: pip install dash dash-bootstrap-components plotly pandas
#       numpy scikit-learn joblib
import dash
import dash_bootstrap_components as dbc
from app.layout import create_layout
from app.callbacks import register_callbacks

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY],
    suppress_callback_exceptions=True,
    title='Coffee Climate Pulse'
)

server = app.server

app.layout = create_layout()

register_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True)
    # app.run_server(debug=True)