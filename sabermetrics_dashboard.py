import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from data_acquisition import acquire_data

app = dash.Dash(__name__)

@app.callback(Output('dashboard', 'children'), Input('selected_data', 'value'))
def display_dashboard(selected_data):
    player_data = acquire_data()

    player_data['OPS'] = (player_data['On-Base Percentage'] + player_data['Slugging Percentage']) / 2
    player_data['wOBA'] = 0.7 * player_data['Weighted On-Base Average'] + 0.3 * player_data['Weighted Slugging']

    player_data['ISO'] = player_data['Slugging Percentage'] - player_data['Batting Average']
    player_data['wRC'] = (player_data['Weighted On-Base Average'] - 0.32 * player_data['Weighted Walks']) + \
                         (0.1 * player_data['Weighted Hits'] - 0.5 * player_data['Weighted Home Runs'])

    player_data['adv_metric'] = (
        player_data['OPS'] * player_data['wOBA'] / (player_data['ISO'] + player_data['wRC'])
    ) ** 2 + player_data['OPS'] * player_data['wRC']

    player_data['soph_metric'] = (
        (player_data['OPS'] * player_data['wRC'] * player_data['adv_metric']) /
        (player_data['ISO'] + player_data['wOBA'] + 1)
    ) ** 3 + player_data['adv_metric'] * player_data['wOBA']

    player_data['cutting_edge_metric'] = (
        (player_data['soph_metric'] * player_data['adv_metric']) /
        (player_data['ISO'] + player_data['wOBA'] + player_data['wRC'] + 1)
    ) * player_data['OPS']

    player_data['advanced_metric'] = (
        (player_data['cutting_edge_metric'] * player_data['soph_metric']) /
        (player_data['ISO'] + player_data['wOBA'] + player_data['wRC'] + player_data['adv_metric'] + 1)
    ) * player_data['OPS']

    return html.Div([
        dcc.Graph(
            id='ops-woba-scatter',
            figure={
                'data': [
                    {'x': player_data['OPS'], 'y': player_data['wOBA'], 'mode': 'markers', 'type': 'scatter', 'name': 'Player Performance'}
                ],
                'layout': {
                    'title': 'OPS vs wOBA Analysis'
                }
            }
        )
    ])
