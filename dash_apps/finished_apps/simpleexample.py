from django_plotly_dash import DjangoDash
from django.conf import settings
from dash.dependencies import Input, Output

import dash_core_components as dcc
import dash_html_components as html
#import plotly.graph_objs as go
import plotly.graph_objects as go
import plotly.io as pio


#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#app = DjangoDash('SimpleExample', external_stylesheets=external_stylesheets)
app = DjangoDash('SimpleExample')


app.layout = html.Div([
    html.H4('Respostas comportamentais'),
    dcc.Graph(id='slider-graph', animate=True, style={"backgroundColor": "#1a2d46", 'color': '#ffffff'}),
    dcc.Slider(
        id='slider-updatemode',
        marks={i: '{}'.format(i) for i in range(20)},
        max=20,
        value=2,
        step=1,
        updatemode='drag',
    ),
])

app.css.append_css({
    "external_url":"https://codepen.io/chriddyp/pen/bWLwgP.css"
})





@app.callback(
               Output('slider-graph', 'figure'),
              [Input('slider-updatemode', 'value')])
def display_value(value):


    x = []
    for i in range(value):
        x.append(i)

    y = []
    for i in range(value):
        y.append(i*i)

    graph = go.Scatter(
        x=x,
        y=y,
        name='Manipulate Graph'
    )
    layout = go.Layout(
        paper_bgcolor='#fff',
        plot_bgcolor='whitesmoke', #'lightblue', #'rgb(10,10,10)',
        xaxis=dict(range=[min(x), max(x)]),
        yaxis=dict(range=[min(y), max(y)]),
        font=dict(color='RebeccaPurple'),
        #font=dict(color='white'),

    )

     # após gerar já salva a imagem dele
     # testado e gerando arquivo C:\Python\crm1-plotly\crm1\static/images/fig1.png
    fig = go.Figure()
    #print('diretório e nome')
    #print(settings.MEDIA_ROOT + "/fig1.png")
    
    # para gerar a imagem, basta remover o comentário da linha abaixo:
    #fig.write_image(settings.MEDIA_ROOT + "/fig1.svg")

    #fig.write_image("images/fig1.svg")
    #fig.write_image("images/fig1.pdf")
    #img_bytes = fig.to_image(format="svg")

    #img_bytes = fig.to_image(format="svg", width=600, height=350, scale=2)
    #Image(img_bytes)

    #return {'data': [img_bytes], 'layout': layout}

    return {'data': [graph], 'layout': layout}
