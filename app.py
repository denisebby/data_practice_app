import dash
from dash import dcc, html
from dash.dependencies import Output, Input, State
import plotly.express as px
import dash_bootstrap_components as dbc

import pandas as pd
import os

####### Utility Functions #####################


def data_in():

    # if cloud == False:
    #     data = os.path.join('data/data.csv')

    # else:
    #     project = 'dash-example-265811'
    #     project_name = 'dash-example-265811.appspot.com'
    #     folder_name = 'data'
    #     file_name = 'data.csv'

    #     if local == True:
    #         GCP = GCPDownloaderLocal() # run locally
    #     else:
    #         GCP = GCPDownloaderCloud()  # run on cloud

    #     bytes_file = GCP.getData(project, project_name, folder_name, file_name)
    #     s = str(bytes_file, encoding='utf-8')
    #     data = StringIO(s)

    data_df = pd.read_csv("gs://gcf-sources-134756275535-us-central1/youtube_stats_clean.csv")

    return data_df

# youtube_stats_df = pd.read_csv("development_nb/youtube_stats_clean.csv")
# keyword_options = sorted(youtube_stats_df.Keyword.unique())

def app_layout():
    youtube_stats_df = data_in()
    keyword_options = sorted(youtube_stats_df.Keyword.unique())

    navbar = dbc.NavbarSimple(
        brand="YouTube Stats Explorer",
        brand_style = {"font-family": "Verdana, sans-serif", "font-size": "2em"},
        brand_href="#",
        color="red",
        dark=True,
        id = "navbar-example-update"
    )

    return html.Div(children=[
        navbar,

        dbc.Container([
        dcc.Markdown(''' 
        I used a dataset of top Youtube videos as of **September 2022**. 
        Use the dropdown and hover to explore videos by key word. The color of the points represent the number of likes \
            and the size of the points represent the number of comments\n 
        > 
        Source: https://www.kaggle.com/datasets/advaypatil/youtube-statistics?sort=votes
        ''', 
        style={"font-family": "Verdana, sans-serif"}),

        dbc.Container([], style = {"margin-top": "5%", "margin-bottom": "0%"}),

        dcc.Dropdown(
            id='dropdown', 
            options=keyword_options,
            value='mrbeast'
        ),

        dbc.Container([], style = {"margin-top": "7.5%", "margin-bottom": "0%"}),

        dcc.Graph(id="graph")
        ], style = {"margin-top": "5%", "margin-bottom": "5%"})
    ])



##########################################

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], meta_tags=[{'name': 'viewport','content': 'width=device-width, initial-scale=1.0'}])
app.title = "Data Mastery"
server = app.server

youtube_stats_df = data_in()


app.layout = app_layout

####### Callbacks #######################
@app.callback(
    Output("graph", "figure"), 
    Input("dropdown", "value"))
def change_colorscale(keyword):

    fig = px.scatter(youtube_stats_df.query(f"Keyword == '{keyword}'"), x = "publish_date", y = "Views", color = "Likes", size = "Comments",
            hover_data = ["Title"], template = "plotly_white", color_continuous_scale="portland")
    fig.update_traces(marker = dict(line=dict(width=2, color = "Black")))
    fig.update_xaxes(title = "Publish Date")
    fig.update_layout(title = f"<b>Youtube Stats: Keyword = '{keyword}'</b><br>Size = # comments, Color = # likes")
    return fig

##########################################

if __name__=='__main__':
    # app.run_server(debug=False, port=8005)
    app.run_server(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))