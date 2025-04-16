import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import base64

# Load preprocessed data
df = pd.read_csv("Project-Template/data/spacex_with_coords.csv")
clustered = pd.read_csv("Project-Template/data/spacex_clustered.csv")

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

# Helper method to load images
def load_image(path):
    encoded = base64.b64encode(open(path, 'rb').read()).decode()
    return f'data:image/png;base64,{encoded}'

#### Plotly Visualizations ####

# 1. Pie Chart
success_counts = df['Mission_Status'].value_counts()
fig_pie = px.pie(names=success_counts.index, values=success_counts.values, title="Mission Success vs Failure")

# 3. Geo Map - Launch Sites
fig_map = px.scatter_geo(df.dropna(subset=['Latitude', 'Longitude']),
                         lat='Latitude', lon='Longitude',
                         color='Mission_Status', hover_name='Organisation',
                         title="Launch Sites Around the World")

# 4. Load and Encode Plots from Files
img_location = load_image("Project-Template/data/location_data.png")
img_violin = load_image("Project-Template/data/price_vs_org.png")
img_box = load_image("Project-Template/data/success_vs_price.png")
img_heatmap = load_image("Project-Template/data/status.png")
img_stackedbar = load_image("Project-Template/data/success_rate.png")
img_anomaly = load_image("Project-Template/data/anomaly_plot.png")
img_kmeans = load_image("Project-Template/data/kmeans_clusters.png")

app.layout = dbc.Container([
    html.H1("Space Missions Dashboard", className="text-center text-primary mb-4"),

    dbc.Tabs([  # <- wrap all tabs inside this
        dbc.Tab(label="Overview", children=[
            dbc.Row([
                dbc.Col(dcc.Graph(figure=fig_pie), md=6),
                dbc.Col(dcc.Graph(figure=fig_map), md=6)
            ])
        ]),

        dbc.Tab(label="Organizational Insights", children=[
            dbc.Row([html.Img(src=img_violin, className="img-fluid")]),
            dbc.Row([html.Img(src=img_stackedbar, className="img-fluid")])
        ]),

        dbc.Tab(label="Environmental Analysis", children=[
            html.Img(src=img_anomaly, className="img-fluid")
        ]),

        dbc.Tab(label="Clustering Insights", children=[
            html.Img(src=img_kmeans, className="img-fluid")
        ]),

        dbc.Tab(label="Exploratory Visuals", children=[
            dbc.Row([html.Img(src=img_location, className="img-fluid")]),
            dbc.Row([html.Img(src=img_box, className="img-fluid")]),
            dbc.Row([html.Img(src=img_heatmap, className="img-fluid")])
        ]),

        dbc.Tab(label="Prediction & ML", children=[
            html.H4("Random Forest Classifier", className="text-center text-primary my-3"),
            html.Pre(open("Project-Template/data/classification_report.txt").read(), style={"textAlign": "center"})
        ])
    ])
], fluid=True)


# Run the app
if __name__ == "__main__":
    app.run(debug=True)


