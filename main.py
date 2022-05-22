from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import math

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    html.H1('Select shape'),
    dcc.Dropdown(['Square', 'Triangle', 'Circle'], value='Triangle',id='dropdown1'),
    html.Div(id='dd-output-container'),

    html.H1('Select size'),
    dcc.Slider(4, 10, 2,
               value=6,
               id='my-slider'
    ),
    html.Div(id='slider-output-container'),
    # dcc.Dropdown(['Small', 'Medium', 'Large'], id='dropdown2'),
    # html.Div(id='dd-output-container1'),

    # html.H1('Select position'),
    # dcc.Dropdown(['Center', 'Top right', 'Bottom left'], id='dropdown3'),
    # html.Div(id='dd-output-container2'),

    html.H1('Preview / Start'),
    dcc.Dropdown(['Preview', 'Start'],value='Preview', id='dropdown4'),
    dcc.Graph(id='graph1'),
    html.Div(id='preview1'),


])


@app.callback(
    Output('dd-output-container', 'children'),
    Input('dropdown1', 'value')
)
def update_output(value):
    return f'You have selected {value}'


@app.callback(
    Output('slider-output-container', 'children'),
    Input('my-slider', 'value'))
def update_output(value):
    return 'You have selected "{}"'.format(value)
# @app.callback(
#     Output('dd-output-container1', 'children'),
#     Input('dropdown2', 'value')
# )
# def update_output(value):
#     return f'You have selected {value}'

# @app.callback(
#     Output('dd-output-container2', 'children'),
#     Input('dropdown3', 'value')
# )
# def update_output(value):
#     return f'You have selected {value}'

@app.callback(
    [Output('graph1', 'figure'),Output('preview1','children')],
    [Input('dropdown4', 'value'),Input('dropdown1','value'),Input('my-slider','value')]
)
def update_output(run,shape,size):
    if run == 'Preview':
        if shape == 'Triangle':
            b = size * 10
            h = math.sqrt(b ** 2 - ((b/2) ** 2))
            fig = go.Figure(go.Scatter(x=[(10 - h / 2), (10 + h /2), (10 - h / 2), (10 - h /2 )], y=[(10 + b / 2), 10, (10 - b / 2), (10 + b / 2)], fill="toself"))
            fig.update_layout(
                autosize=False,
                width=500,
                height=500,)
            return fig, f'you have selected {shape} with size = {size}'

        if shape == 'Square':
            fig = go.Figure(go.Scatter(x=[10-5*size,10+5*size,10+5*size,10-5*size,10-5*size], y=[10+5*size,10+5*size,10-5*size,10-5*size,10+5*size], fill="toself"))
            fig.update_layout(
                autosize=False,
                width=500,
                height=500, )
            return fig ,f'you have selected {shape} with size = {size}'

        if shape == 'Circle':
            x=[]
            y=[]
            for i in range(360):
                xr = 10 + size + math.cos(i )
                yr = 10 + size + math.sin(i )
                x.append(xr)
                y.append(yr)
            fig = go.Figure(go.Scatter(x=x,y=y,fill="toself"))
            fig.update_layout(
                autosize=False,
                width=500,
                height=500, )

            return fig, f'you have selected {shape} with size = {size}'


    elif run == 'Start':
        print(f'Start drawing {shape} with size = {size}')




if __name__ == '__main__':
    app.run_server(debug=True)