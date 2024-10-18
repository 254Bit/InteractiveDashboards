# Import Python Libraries
import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

#Load The Dataset
df = pd.read_csv('Population of all US Cities 2024.csv')
df.info()


# Create The Dash app
app = dash.Dash()

# Set up The App Layout
app.layout = html.Div([
    html.H1('US CITY POPULATION'),
    dcc.Dropdown(id='geo-dropdown',
                 options=[{'label':i, 'value': i}
                          for i in df['US State'].unique()],
                 value='New York'),
    dcc.Graph(id='Population 2024')
])

#Set Up The Callback function
@app.callback(
    Output(component_id='Population 2024', component_property='figure'),
    Input(component_id='geo-dropdown', component_property='value')
)
def update_graph(selected_state):
    filtered_state = df[df['US State'] == selected_state]
    line_fig = px.line(filtered_state,
                       x = 'Population 2024', y = 'US City',
                       title=f'US STATE Population in {selected_state}')
    return line_fig

#Run Local Server
if __name__ == '__main__':
    app.run_server(debug=True)