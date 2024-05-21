import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# Import and clean data
df = pd.read_csv(r'C:\Users\PC\Documents\Data-Science-Tasks\InteractiveDashboards\Bees\intro_bees.csv')

df = df.groupby(['State', 'ANSI','Affected by', 'Year','state_code'])[['Pct of Colonies Impacted']].mean()
df.reset_index(inplace=True)
print(df[:5])

#-------------------------------------------------------
#App Layout
app.layout = html.Div([
    html.H1('Web Application Dashboard', style={'text-align':'center'}),
    dcc.Dropdown(id='slct_year',
                 options=[
                     {'label': '2015', 'value':2015},
                     {'label': '2016', 'value':2016},
                     {'label': '2017', 'value':2017},
                     {'label': '2018', 'value':2018}],
                 multi=False,
                 value=2015,
                 style={'width':'48%'}
                ),
    html.Div(id='output_container'),
    html.Br(),
    
    dcc.Graph(id='bee_map')
])

#----------------------------------------------------------
# Connect the plotly with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='bee_map', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
)
def update_graph(option_selected):
    print(option_selected)
    #print(type(option_selected))
    
    container = 'The Year Chosen by User Was: {}'.format(option_selected)
    
    dff = df.copy()
    dff = dff[dff['Year']==option_selected]
    dff = dff[dff['Affected by'] == 'Varroa mites']
    
    #Plotly Express
    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations ='state_code',
        scope='usa',
        color='Pct of Colonies Impacted',
        hover_data=['State', 'Pct of Colonies Impacted'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Pct of Colonies Impacted':'% of Bee Colonies'},
        template='plotly_dark'
    )
    
    #Plotly Graph Objects (Go)
    fig = go.Figure(
        data =[go.Choropleth(
            locationmode='USA-states',
            locations=dff['state_code'],
            z=dff['Pct of Colonies Impacted'].astype(float),
            colorscale='Reds',
        )]
    )

    fig.update_layout(
        title_text='Bees Affected by Mites in the USA',
        title_xanchor ='center',
        title_font=dict(size=24),
        title_x=0.5,
        geo=dict(scope='usa'),
    )
    
    return container, fig
#-----------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
    
