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


# sart app
#app = dash.Dash(__name__)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('raddash01', external_stylesheets=external_stylesheets)

# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
df = pd.read_csv(settings.MEDIA_ROOT + "/intro_bees.csv")

df = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['Pct of Colonies Impacted']].mean()
df.reset_index(inplace=True)
# imprime o resultado do groupby
# print(df[:5])

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    #html.H1("Web Application Dashboards utilizando Dash", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_year_mp",
                 options=[
                     {"label": "2015", "value": 2015},
                     {"label": "2016", "value": 2016},
                     {"label": "2017", "value": 2017},
                     {"label": "2018", "value": 2018}],
                 multi=False,
                 value=2015,
                 style=[{'width': "40%"},{'height': "100%"}]
                 ),
    # empty space
    html.Div(id='output_container', children=[]),
    html.Br(),

    #empty graph
    #dcc.Graph(id='my_bee_map', figure={})
    dcc.Graph(id='my_bee_rad_bar', figure={})

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_rad_bar', component_property='figure')],
    [Input(component_id='slct_year_mp', component_property='value')]
)
def update_graph(option_slctd):
    # update_graph has one argument for each input above
    #print(option_slctd)
    #print(type(option_slctd))

    container = "" #"Ano selecionado no filtro: {}".format(option_slctd)

    # faz uma cópia do dataframe para não alterar o original
    dff = df.copy()
    # filtro conforme o ano selecionado, 2015 por default por conta da propriedade value=2015 acima
    dff = dff[dff["Year"] == option_slctd]
    # 2o filtro é para abelhas afetadas apenas por VArroa_mites
    dff = dff[dff["Affected by"] == "Varroa_mites"]



    # Plotly Graph Objects (GO)
    categories = ['Visão','Liderança','Proatividade',
                'Pontualidade', 'Comunicação']

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=[3.5, 5, 3, 3, 3.5],
        theta=categories,
        fill='toself',
        name='Coachee',
        legendgroup='Coachee'
    ))
    fig.add_trace(go.Scatterpolar(
        r=[4, 4.5, 2.5, 3, 3.5],
        theta=categories,
        fill='toself',
        name='Participantes',
        legendgroup='Participantes'
    ))

    fig.update_layout(
    polar=dict(
        radialaxis=dict(
        visible=True,
        range=[0, 5]
        )),
    showlegend=True
    )

     # após gerar já salva a imagem dele
     # testado e gerando arquivo C:\Python\crm1-plotly\crm1\static/images/fig1.png
    #fig = px.Figure()
    #print('diretório e nome')
    #print(settings.MEDIA_ROOT + "/fig1.png")

    # para gerar a imagem, basta remover o comentário da linha abaixo:
    #fig.write_image(settings.MEDIA_ROOT + "/map01.svg")

    # o return possui dois argumentos porque acima temos dois outputs
    return container, fig


# ------------------------------------------------------------------------------
#if __name__ == '__main__':
#    app.run_server(debug=True)
