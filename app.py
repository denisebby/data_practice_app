import dash
from dash import dcc, html, dash_table, ctx
from dash.dependencies import Output, Input, State
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

import datetime as dt
from datetime import datetime
from pytz import timezone

import pandas as pd
import joblib
import os

####### Utility Functions #####################

########### Styles ############
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

# text/markdown styles

text_heading_style = {"font-family": "Lato, -apple-system, sans-serif", "font-size": "4em"}

text_body_style = {"font-family": "Roboto Mono, monospace", "font-size": "1.2em",}

###############################

def get_date():
    tz = timezone('EST')
    d = datetime.now(tz)
    year = d.year
    month = d.strftime("%B")
    day = d.day

    if day in [1,21, 31]:
        suffix == "st"
    elif day in [2,22]:
        suffix = "nd"
    elif day == [3, 23]:
        suffix = "rd"
    else:
        suffix = "th"

    return f"{month} {day}{suffix}, {year}, EST"

def next_datetime(current: dt.datetime, hour: int, **kwargs) -> dt.datetime:
    repl = current.replace(hour=hour, **kwargs)
    while repl <= current:
        repl = repl + dt.timedelta(days=1)
    return repl

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

    bank_df = joblib.load("development/data/bank_df.joblib")

    today = get_date()
    # can do custom logic here to define what out of the bank to use
    bank_df = bank_df.query(f"readable_date == '{today}'")
    # data_df = pd.read_csv("gs://gcf-sources-134756275535-us-central1/youtube_stats_clean.csv")

    # return data_df
    return bank_df, data_df


def get_question_title():
    question_title = bank_df.loc[0,"question_title"]
    return question_title

def get_question_body():
    question_body = bank_df.loc[0,"question"]

    return question_body

def get_correct_answer():
    # return button that has correct answer
    return bank_df.loc[0,"correct_answer"]

def get_answer_choice(choice_num):
    col = f"answer_choice_{str(choice_num)}"
    return bank_df.loc[0, col]


def get_feedback_body(performance_message):
    """
    Args:
        performance_message: message depending on if the user got 
            question correct
    """

    tz = timezone('EST')
    d = datetime.now(tz)

    # we update at 7:00 AM every day
    update_date = next_datetime(d, hour = 7, minute = 0, second = 0)

    duration_in_s = (update_date - d).total_seconds()
    hours = duration_in_s/ 3600

    hours_int = int(hours)
    minutes_int = int((hours - hours_int)*60)

    feedback_main_body = bank_df.loc[0,"feedback"]

    feedback_body = dbc.Container([
        dcc.Markdown('''Feedback:''', 
        style=text_heading_style,),

        dcc.Markdown(performance_message, style=text_body_style),

        feedback_main_body,

        dcc.Markdown(f'''\
        The next question is in {hours_int} hours and {minutes_int} minutes!
        ''', 
        style={"font-family": "Lato, -apple-system, sans-serif", "font-size": "1.2em", 
        "margin-top": "2%", "margin-bottom": "2%"},),

    ])

    return feedback_body


def app_layout():
   
    navbar = dbc.NavbarSimple(
        brand="E D A I L Y",
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

        # QUESTION HEADING
        dcc.Markdown(f'''Q: {get_question_title()}''', 
        style=text_heading_style,),

        # QUESTION BODY
        get_question_body(),

        # ANSWER HEADING
        dcc.Markdown('''A:''', 
            style={"font-family": "Lato, -apple-system, sans-serif", "font-size": "4em"},),

        # IMPORTANT DATA STORED
        dcc.Store(id="answer-most-recent-button", data=""),
        dcc.Store(id="ready-for-submit", data=False),
        dcc.Store(id="feedback-mode", data=False),
        dcc.Store(id="ab", data=""),

        # ANSWER BODY
        dbc.Container([

            # option 1

            dbc.Button([
                get_answer_choice(choice_num = 1)       
            ], 
            className = "answer-choice",
            id = "button-1",
            style=regular_button_style,
            n_clicks = 0, color = "#f0ead6"
            ),
            
            # option 2

            dbc.Button([
                get_answer_choice(choice_num = 2)
                   
            ], 
            className = "answer-choice",
            id = "button-2",
            style=regular_button_style,
            n_clicks = 0, color = "#f0ead6"
            ),

            # option 3

            dbc.Button([
                get_answer_choice(choice_num = 3)

                  
            ], 
            className = "answer-choice",
            id = "button-3",
            style=regular_button_style,
            n_clicks = 0, color = "#f0ead6"
            ),

            # option 4

            dbc.Button([

                get_answer_choice(choice_num = 4)

            ], 
            className = "answer-choice",
            id = "button-4",
            style=regular_button_style,
            n_clicks = 0, color = "#f0ead6"
            ),

            
            # Submit button
            dbc.Button([
                "Submit"
            ],
            id = "submit-button",
            # 
            style = not_ready_submit_style
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

bank_df, data_df = data_in()


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
        # this button can be any button clicked, 
        # not just the answer choices
        button_id = ctx.triggered_id

        if button_id is None:
            raise PreventUpdate

        

        if button_id != None:
            # print(button_id)
            # print(type(button_id))
            # print(int(str(button_id).split("-")[-1]))

            x = str(button_id).split("-")[-1]
            if x in ["1", "2", "3", "4"]:
                chosen_num = int(str(button_id).split("-")[-1])
            else:
                chosen_num = None

            # unselect button already selected
            if (chosen_num is None) or ((ready_for_submit) and (most_recent_btn_num != None) and (most_recent_btn_num == chosen_num)):
                return (chosen_num,) + (False, ) + (not_ready_submit_style,) + (regular_button_style,)*4 + ("answer-choice",)*4
            else:
                final_styles = tuple()
                for i in range(4):
                    if i == (chosen_num-1):
                        final_styles += (clicked_button_style,)
                    else:
                        final_styles += (regular_button_style,)
                
                # we are ready to submit!
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

        feedback_body = get_feedback_body(performance_message)
        
        
        return feedback_body, True, selected_answer
    elif not feedback_mode:
        return "", False, 0
    else:

        if feedback_selected_answer == get_correct_answer():
            performance_message = "You're right!"
        else:
            performance_message = "Close but no cigar!"

        feedback_body = get_feedback_body(performance_message)

        return feedback_body, True, feedback_selected_answer



##########################################

if __name__=='__main__':
    # app.run_server(debug=False, port=8005)
    # host = "0.0.0.0"
    app.run_server(debug=True, host = "127.0.0.1", port=int(os.environ.get("PORT", 8081)))