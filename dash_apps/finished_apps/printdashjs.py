from django_plotly_dash import DjangoDash
from django.conf import settings
from dash.dependencies import Input, Output, State

import pandas as pd

import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

import dash
import dash_core_components as dcc
import dash_html_components as html

import base64
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = DjangoDash('printdashjs', external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(children=[
    html.H3(children='Dados Demonstrativos | Teste'),

    html.Div(children='''
        Dados aleatórios - apenas para exibir o gráfico.
    '''),

    # html.Button('Graph -> PDF', id='button'),  #comentei o botão para não confundir e porque a função, infelizmente, naõ funcionou da forma como eu esperava

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),

    html.Div(id='graph_img')
])


app.clientside_callback(
    '''
    function (chart_children) {
        if (chart_children.type == "Img") {
            console.log(chart_children);
            var doc = new PDFDocument({layout:'landscape', margin: 25});
            var stream = doc.pipe(blobStream());

            doc.fontSize(28);
            doc.font('Helvetica-Bold');
            doc.text('Example'.toUpperCase(), 15, 40);
            doc.addPage().fontSize(28);
            doc.text('Showing that multiple pages work');
            doc.image(chart_children.props.src, {width: 780});
            doc.end();

            var saveData = (function () {
                var a = document.createElement("a");
                document.body.appendChild(a);
                a.style = "display: none";
                return function (blob, fileName) {
                    var url = window.URL.createObjectURL(blob);
                    a.href = url;
                    a.download = fileName;
                    a.click();
                    window.URL.revokeObjectURL(url);
                };
            }());

            stream.on('finish', function() {

              var blob = stream.toBlob('application/pdf');
              saveData(blob, 'Report.pdf');

                // iframe.src = stream.toBlobURL('application/pdf');
            });
        }
        return 0;
    }
    ''',
    Output('graph_img', 'n_clicks'),
    [
        Input('graph_img', 'children'),
    ]
)


@app.callback(
    Output('graph_img', 'children'),
    [
        Input('button', 'n_clicks')
    ],
    [
        State('example-graph', 'figure')
    ]
)
def figure_to_image(n_clicks, figure_dict):
    if n_clicks:
        # Higher scale = better resolution but also takes longer/larger size
        figure = go.Figure(figure_dict)
        img_uri = figure.to_image(format="png", scale=3)
        src = "data:image/png;base64," + base64.b64encode(img_uri).decode('utf8')
        return html.Img(src=src)

    return ''


# ------------------------------------------------------------------------------
#if __name__ == '__main__':
#    app.run_server(debug=True)
