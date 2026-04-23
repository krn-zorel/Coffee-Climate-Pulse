import dash
from app.layout import create_layout
from app.callbacks import register_callbacks

# Initialize Dash App
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Coffee Climate Pulse"

# Set the layout
app.layout = create_layout()

# Register callbacks
register_callbacks(app)

if __name__ == '__main__':
    # Run from the root directory using: python -m app.app
    app.run(debug=True)