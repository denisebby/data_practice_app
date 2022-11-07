import dash
from dash import dcc, html, dash_table, ctx
from dash.dependencies import Output, Input, State
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate


import pandas as pd
import os

####### Utility Functions #####################

def get_date():
    return "October 29th, 2022, EST"

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

    data_df = pd.read_csv("development/data/Air_Traffic_Passenger_Statistics.csv")


    # data_df = pd.read_csv("gs://gcf-sources-134756275535-us-central1/youtube_stats_clean.csv")

    # return data_df
    return data_df

def get_question():
    return """
    Jeremiah is a data anlyst working with airline data. His stakeholder is interested\
    in seeing aggregate passener data grouped by the airline. Here is the data and code Jeremy currently has. But Jeremy\
    is stuck on how to finish the code?\n

    ```python
    import pandas as pd
    print("hi")
    ```
    
    Help out Jeremy. Can you fill in the missing code?
    """

def get_correct_answer():
    # return button that has correct answer
    return 3

# this is the most recent button
clicked_button_style = {"backgroundColor": "#f9dd81","box-shadow": "0rem 0rem 3rem #f9dd81", 
            "transform": "scale(1.025)", "font-family": "Roboto Mono, monospace", "font-size": "1.2em",
            "border": "0.1em solid", "border-radius":"1em", "border-color":"black", "text-align": "left", 
            "width": "100%", "margin-bottom": "2%"}

regular_button_style = {"backgroundColor": "#ffffff", "font-family": "Roboto Mono, monospace", 
    "font-size": "1.2em","border": "0.1em solid", "border-radius":"1em", "border-color":"black",
    "text-align": "left", "width": "100%", "margin-bottom": "2%"}

correct_button_style = {"backgroundColor": "#a7f4b7", "font-family": "Roboto Mono, monospace", 
    "font-size": "1.2em","border": "0.1em solid", "border-radius":"1em", "border-color":"black",
    "text-align": "left", "width": "100%", "margin-bottom": "2%"}

wrong_button_style = {"backgroundColor": "#f4b8a7", "font-family": "Roboto Mono, monospace", 
    "font-size": "1.2em","border": "0.1em solid", "border-radius":"1em", "border-color":"black",
    "text-align": "left", "width": "100%", "margin-bottom": "2%"}

other_feedback_button_style = {"backgroundColor": "#e2e5e2", "font-family": "Roboto Mono, monospace", 
    "font-size": "1.2em","border": "0.1em solid", "border-radius":"1em", "border-color":"black",
    "text-align": "left", "width": "100%", "margin-bottom": "2%"}

not_ready_submit_style = {"color": "grey", "backgroundColor": "#f0ead6", "border": "0.1em solid", "border-radius":"1em", 
        "border-color":"grey", "font-family": "Lato, -apple-system, sans-serif", 
        "font-size": "2em", "width": "5em", "margin": "0 auto", "margin-bottom": "2%", "justify-content": "center", "display": "flex"}

ready_submit_style = {"color": "black", "backgroundColor": "#f9dd81","box-shadow": "0rem 0rem 3rem #f9dd81",
        "border": "0.1em solid", "border-radius":"1em", 
        "border-color":"black", "font-family": "Lato, -apple-system, sans-serif", 
        "font-size": "2em", "width": "5em", "margin": "0 auto", "margin-bottom": "2%", "justify-content": "center", "display": "flex"}

hide_submit_style = {"display":"none"}

# youtube_stats_df = pd.read_csv("development_nb/youtube_stats_clean.csv")
# keyword_options = sorted(youtube_stats_df.Keyword.unique())

def app_layout():
    # youtube_stats_df = data_in()
    # keyword_options = sorted(youtube_stats_df.Keyword.unique())

    navbar = dbc.NavbarSimple(
        brand="E D A I L Y",
        # -apple-system, BlinkMacSystemFont, sans-serif
        brand_style = {"font-family": "Lato, -apple-system, sans-serif" , "font-size": "2rem", "padding": "0.1rem 0.1rem"},
        brand_href="#",
        color="black",
        dark=True,
        id="navbar",
        style={"height": "3rem"},
        expand = True
     
    )

    return html.Div(children=[
        navbar,

        # the body
        dbc.Container([

        dcc.Markdown(f'''\
        Practice EDA Daily. The date is **{get_date()}**.
        Here is today's question:
        ''', 
        style={"font-family": "Lato, -apple-system, sans-serif", "font-size": "2em", 
        "margin-top": "2%", "margin-bottom": "2%"},),

        dcc.Markdown('''Q: Pandas, Group By''', 
        style={"font-family": "Lato, -apple-system, sans-serif", "font-size": "4em"},),

        # The container is for the QUESTION body
        dbc.Container([
             dcc.Markdown(f'''\
                Jeremy is a data analyst working with airline data. Here is a sample:
                '''
            , style={"font-family": "Roboto Mono, monospace", "font-size": "1.2em",}),

            # table
            dbc.Container([
            dash_table.DataTable(data_df.head(10).to_dict('records'), [{"name": i, "id": i} for i in data_df.columns], 
            style_cell={'textAlign': 'left',
             "backgroundColor": "#f0ead6",
             "padding": "0.5em"},   
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
            },
            style_table={'overflowX': 'scroll', 'overflowY': 'scroll', "height": "20em"},
            style_header = {
                "backgroundColor": "#f9dd81",
                'fontWeight': 'bold',
                "border": "1px solid black",

            },
   
            ),
            ], style={"margin-top": "2%", "margin-bottom": "2%"}),



            dcc.Markdown(f'''\
        
            His stakeholder is interested\
            in seeing aggregate passener data grouped by the airline. Here is the data and code Jeremy currently has. But Jeremy\
            is stuck on how to finish the code?\n

            ```python
            import pandas as pd
            print("hi")
            ```
            
            Help out Jeremy. Can you fill in the missing code?
    
            ''', style={"font-family": "Roboto Mono, monospace", "font-size": "1.2em",}),





        ], id = "question_body", ),

       

        # data sample if needed


        

        # Answer

        dcc.Markdown('''A:''', 
            style={"font-family": "Lato, -apple-system, sans-serif", "font-size": "4em"},),

        dcc.Store(id="answer-most-recent-button", data=""),
        dcc.Store(id="ready-for-submit", data=False),
        dcc.Store(id="feedback-mode", data=False),
        dcc.Store(id="ab", data=""),
        # dcc.Store(id="feedback-selected-answer", data=0),

        # The container is for the ANSWER body
        # Could be single correct answer (RadioItems)
        # or multiple correct answers ()
        dbc.Container([

            # option 1

            dbc.Button([

            dcc.Markdown(f'''\
            hi hey hows it goin
            ```python
            import pandas as pd
            print("hi")
            ```
            ''', ),        
            ], 
            className = "answer-choice",
            id = "button-1",
            style={"backgroundColor": "#ffffff", "font-family": "Roboto Mono, monospace", "font-size": "1.2em",
                     "border": "0.1em solid", "border-radius":"1em", "border-color":"black", 
                     "text-align": "left", "width": "100%", "margin-bottom": "2%"},
            n_clicks = 0, color = "#f0ead6"
            ),
            
            # option 2

            dbc.Button([

            dcc.Markdown(f'''\
            ```python
            import pandas as pd
            print("hi")
            ```
            ''', ),        
            ], 
            className = "answer-choice",
            id = "button-2",
            style={"backgroundColor": "#ffffff", "font-family": "Roboto Mono, monospace", "font-size": "1.2em",
                     "border": "0.1em solid", "border-radius":"1em", "border-color":"black", 
                     "text-align": "left", "width": "100%", "margin-bottom": "2%"},
            n_clicks = 0, color = "#f0ead6"
            ),

            # option 3

            dbc.Button([

            dcc.Markdown(f'''\
            this is the right answer
            ```python
            import pandas as pd
            print("hi")
            ```
            ''', ),        
            ], 
            className = "answer-choice",
            id = "button-3",
            style={"backgroundColor": "#ffffff", "font-family": "Roboto Mono, monospace", "font-size": "1.2em",
                     "border": "0.1em solid", "border-radius":"1em", "border-color":"black", 
                     "text-align": "left", "width": "100%", "margin-bottom": "2%"},
            n_clicks = 0, color = "#f0ead6"
            ),

            # option 4

            dbc.Button([

            dcc.Markdown(f'''\
            whats up
            ```python
            import pandas as pd
            print("hi")
            ```
            ''', ),        
            ], 
            className = "answer-choice",
            id = "button-4",
            style={"backgroundColor": "#ffffff", "font-family": "Roboto Mono, monospace", "font-size": "1.2em",
                     "border": "0.1em solid", "border-radius":"1em", "border-color":"black", 
                     "text-align": "left", "width": "100%", "margin-bottom": "2%"},
            n_clicks = 0, color = "#f0ead6"
            ),

            
            # Submit button
            dbc.Button([
                "Submit"
            ],
            id = "submit-button",
            style = {"color": "grey", "backgroundColor": "#f0ead6", "border": "0.1em solid", "border-radius":"1em", 
            "border-color":"grey", "font-family": "Lato, -apple-system, sans-serif", 
            "font-size": "2em", "width": "5em", "margin": "0 auto", "margin-bottom": "2%", "justify-content": "center", "display": "flex"}
            ),



             # The container is for the FEEDBACK body

            dbc.Container(children="", id="feedback-body")



        ], id = "answer_body"),

       



        ],style= {}),

     
    ], )



##########################################
external_stylesheets = [
    'https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,100;0,300;1,100&display=swap',
    'https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,100;0,300;1,100&family=Roboto+Mono&display=swap'
]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], meta_tags=[{'name': 'viewport','content': 'width=device-width, initial-scale=1.0'}])
app.title = "Data Mastery"
server = app.server

data_df = data_in()


app.layout = app_layout

####### Callbacks #######################
# Whenever an input property changes, the function that the callback decorator wraps will get called automatically. 

@app.callback(
    Output('answer-most-recent-button', 'data'),
    Output('ready-for-submit', 'data'),
    Output('submit-button', 'style'),
    Output('button-1', 'style'),
    Output('button-2', 'style'),
    Output('button-3', 'style'),
    Output('button-4', 'style'),
    Output('button-1', 'className'),
    Output('button-2', 'className'),
    Output('button-3', 'className'),
    Output('button-4', 'className'),
    Input("answer-most-recent-button", "data"),
    Input("ready-for-submit", "data"),
    Input('button-1', 'n_clicks'),
    Input('button-2', 'n_clicks'),
    Input('button-3', 'n_clicks'),
    Input('button-4', 'n_clicks'),
    Input("feedback-mode", "data"),
    Input("ab", "data"),)
def display(most_recent_btn_num, ready_for_submit, btn1, btn2, btn3, btn4,feedback_mode, selected_answer):
    """
    This is a pretty messy callback function:
    TODO: Document/ and explain it here
    TODO: consider cleaning up/ refactoring

    Output:
        ready-for-submit: boolean, True if we are ready to submit an answer
    """
    

    
    if not feedback_mode:
    # if not feedback_mode:
        button_id = ctx.triggered_id

        if button_id is None:
            raise PreventUpdate

        

        if button_id != None:
            # print(button_id)
            # print(type(button_id))
            # print(int(str(button_id).split("-")[-1]))

            chosen_num = int(str(button_id).split("-")[-1])

            # if button clicked matches second most recent button clicked
            # unselect button already selected
            if (ready_for_submit) and (most_recent_btn_num != None) and (most_recent_btn_num == chosen_num):
                return (chosen_num,) + (False, ) + (not_ready_submit_style,) + (regular_button_style,)*4 + ("answer-choice",)*4
            else:
                final_styles = tuple()
                for i in range(4):
                    if i == (chosen_num-1):
                        final_styles += (clicked_button_style,)
                    else:
                        final_styles += (regular_button_style,)

                return (chosen_num,) +  (True,) + (ready_submit_style,) + final_styles + ("answer-choice",)*4
        else:
        
            return (None,) + (False,) + (not_ready_submit_style,) + (regular_button_style,)*4 + ("answer-choice",)*4
    else:

        correct_answer = get_correct_answer()

        t = tuple()
        for i in range(1,5):
            if (i == selected_answer and i == correct_answer):
                t += (correct_button_style ,)
            elif i == correct_answer:
                t += (correct_button_style ,)
            elif i == selected_answer:
                t += (wrong_button_style ,)
            else:
                t += (other_feedback_button_style,)

        return (None,) + (False,) + (hide_submit_style,) + t + ("answer-choice-feedback-mode",)*4

    # else:
    #     # ready_for_submit is False because we already submitted and are in feedback mode
    #     return (most_recent_btn_num,) + (False,) + (not_ready_submit_style,) + (regular_button_style,) * 4


@app.callback(
    Output("submit-button", "className"),
    Input("ready-for-submit", "data"),
)
def make_submit_button_hoverable(ready_for_submit):
    # print(ready_for_submit)
    if ready_for_submit:
        return "hover_class"
    else:
        return

@app.callback(
    Output("feedback-body", "children"),
    Output("feedback-mode", "data"),
    # feedback selected answer, 
    # for some reason naming it 'ab' works but other names don't
    Output("ab", "data"),
    Input("answer-most-recent-button", "data"),
    Input("ready-for-submit", "data"),
    Input("submit-button", "n_clicks"),
    Input("feedback-mode", "data"),
    # feedback-selected-answer
    Input("ab", "data"),
)
def submit_answer_and_get_feedback(most_recent_btn_num, ready_for_submit, 
    n_clicks, feedback_mode, feedback_selected_answer):
    button_id = ctx.triggered_id

    if button_id is None:
        raise PreventUpdate

    print(most_recent_btn_num, button_id)
    # the first time we press submit
    if not feedback_mode and ready_for_submit and n_clicks is not None and n_clicks > 0 and button_id == "submit-button":
        selected_answer = most_recent_btn_num

        if selected_answer == get_correct_answer():
            performance_message = "You're right!"
        else:
            performance_message = "Close but no cigar!"

        feedback_body = dbc.Container([
        dcc.Markdown('''Feedback:''', 
        style={"font-family": "Lato, -apple-system, sans-serif", "font-size": "4em"},),

        dcc.Markdown(performance_message, style={"font-family": "Roboto Mono, monospace", "font-size": "1.2em",}),

        dcc.Markdown(f'''\
        
            Jeremy has to do this line of code. This is how that pandas function works. 
            More can be found in the pandas documentation. He has to use the group by function.
            He can use agg for more functionality.
    
            ''', style={"font-family": "Roboto Mono, monospace", "font-size": "1.2em",}
        ),



        ])

        return feedback_body, True, selected_answer
    elif not feedback_mode:
        return "", False, 0
    else:

        if feedback_selected_answer == get_correct_answer():
            performance_message = "You're right!"
        else:
            performance_message = "Close but no cigar!"

        feedback_body = dbc.Container([
        dcc.Markdown('''Feedback:''', 
        style={"font-family": "Lato, -apple-system, sans-serif", "font-size": "4em"},),

        dcc.Markdown(performance_message, style={"font-family": "Roboto Mono, monospace", "font-size": "1.2em",}),

        dcc.Markdown(f'''\
        
            Jeremy has to do this line of code. This is how that pandas function works. 
            More can be found in the pandas documentation. He has to use the group by function.
            He can use agg for more functionality1
    
            ''', style={"font-family": "Roboto Mono, monospace", "font-size": "1.2em",}
        ),



        ])

        return feedback_body, True, feedback_selected_answer



##########################################

if __name__=='__main__':
    # app.run_server(debug=False, port=8005)
    # host = "0.0.0.0"
    app.run_server(debug=True, host = "127.0.0.1", port=int(os.environ.get("PORT", 8080)))