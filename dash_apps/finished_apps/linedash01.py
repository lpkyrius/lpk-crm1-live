from django_plotly_dash import DjangoDash
from django.conf import settings
from dash.dependencies import Input, Output

import pandas as pd

import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go
import plotly.io as pio

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('linedash01', external_stylesheets=external_stylesheets)

# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
df = pd.read_csv(settings.MEDIA_ROOT + "/intro_bees.csv")

df = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['Pct of Colonies Impacted']].mean()
df.reset_index(inplace=True)
#print(df[:5])

bee_killers = ["Disease", "Other", "Pesticides", "Pests_excl_Varroa", "Unknown", "Varroa_mites"]

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H3("Teste linear", style={'text-align': 'center'}),

     dcc.Dropdown(id="slct_impact",
                 options=[{"label": x, "value":x} for x in bee_killers],
                 value="Pesticides",
                 multi=False,
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    #html.Br(), 

    html.Div(children = [
                dcc.Graph(id='my_bee_map_ln', 
                style={
                    'width':'100%',
                    'height':'100%',
                    'margin-left':'1px'},
                figure={}),
    ])
  
],
    # set the sizing of the parent div
    style = {'display': 'inline-block', 'height':'100%', 'width': '100%'})


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map_ln', component_property='figure')],
    [Input(component_id='slct_impact', component_property='value')]
)
def update_graph(option_slctd):
    #print(option_slctd)
    #print(type(option_slctd))

    container = "The bee-killer chosen by user was: {}".format(option_slctd)

    dff = df.copy()
    dff = dff[dff["Affected by"] == option_slctd]
    dff = dff[(dff["State"] == "Idaho") | (dff["State"] == "New York") | (dff["State"] == "New Mexico")]

    fig = px.line(
        data_frame=dff,
        x='Year',
        y='Pct of Colonies Impacted',
        color='State',
        template='plotly_white'
    )

    #fig.update_layout(height=800)

    return container, fig
