from dash import Dash, dcc, html, Input, Output, callback, dash
import plotly.express as px
import pandas as pd


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('https://raw.githubusercontent.com/Reconik/Dashboard/Test-dashboard/text.csv')

app = Dash(__name__)


def tttt(a):
    return pd.to_datetime(a, format="%Y-%m-%d")


gg = df['Категория'].unique()
# df['Дата'] = tttt(df['Дата']).astype(int)/ 10**9


TEST = "FFFF"
app.layout = html.Div([


    html.Div([
    html.H1('График рассеяния'),
        dcc.Graph(id='graph-with-slider'),
        dcc.Slider(
            0,
            len(gg) - 1,
            step=None,
            value=0,
            marks={str(i): (str(gg[i])) for i in range(0, len(gg))},
            id='year-slider'
        )], style={'display': 'inline-lobck', 'width': '90%'}),

    html.H1('Круговой график по категории и отдельным товарам'),
    html.Div([
        html.P("Категория:"),
        dcc.Dropdown(id='names',
                     options=df["Категория"].unique(),
                     value='Электроника', clearable=False
                     ),
    ], style={'width': '15%', 'float': 'left', 'display': 'inline-block'}),

    html.Div([dcc.Graph(id="piegraph"), ],
             style={'width': '60%', 'display': 'inline-block', 'padding': '0 20'}),

    html.H1('Таблица и диаграмма для анализ данных о продажах товаров'),
        dcc.Graph(
            id='sales-analysis',
            figure={
                'data': [
                    {'x': df['Товар'], 'y': df['Товар'], 'type': 'bar', 'name': 'Товар'},
                    {'x': df['Товар'], 'y': df['Сумма'], 'type': 'bar', 'name': 'Сумма'},
                    {'x': df['Товар'], 'y': df['Количество'], 'type': 'bar', 'name': 'Количество'}
                ],
                'layout': {
                    'title': 'Анализ данных о продажах товаров',
                    'xaxis': {'title': 'Товар'},
                    'yaxis': {'title': 'Данные'},
                    'zaxis': {'title': 'Количество'}
                }
            }
        ),
        html.Table(
            id='sales-table',
            children=[html.Thead(html.Tr(children=[html.Th(col_name) for col_name in df.columns])),
                html.Tbody([html.Tr(children=[html.Td(str(value)) for value in row_values])
                         for row_values in df.values])]),


])


@callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'))
def update_figure(selected_year):
    filtered_df = df[df.Категория == df['Категория'][int(selected_year)]]

    fig = px.scatter(filtered_df, x="Сумма", y="Товар", color="Товар", size="Количество", hover_name="Товар",
                     log_x=True, size_max=55)
    fig.update_layout(transition_duration=500)
    return fig

@app.callback(
    Output("piegraph", "figure"),
    Input("names", "value"))
def generate_chart(names):
    jjj = df[df.Категория == names]
    fig = px.pie(jjj, values='Количество', names='Товар', hole=.3)
    return fig








if __name__ == '__main__':
    app.run(debug=True)
