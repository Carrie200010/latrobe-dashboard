
import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import datetime

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "La Trobe Emotion Dashboard"
app.config.suppress_callback_exceptions = True

LA_TROBE_RED = "#a6192e"

# Logo path (replace if logo is uploaded locally)
logo_path = "/assets/logo.png"

initial_chat = [{"role": "ai", "message": "🧠 Hello! I'm here to support you. How are you feeling today?"}]

app.layout = html.Div([
    dcc.Location(id="url"),
    dcc.Store(id="chat-store", data=initial_chat),
    html.Div([
        html.Img(src=logo_path, style={"width": "100%", "marginBottom": "1rem"}),
        html.H2("LA TROBE", className="text-white"),
        html.Hr(),
        dbc.Nav([
            dbc.NavLink("Overview", href="/", active="exact", className="text-white"),
            dbc.NavLink("Reports", href="/reports", active="exact", className="text-white"),
            dbc.NavLink("Surveys", href="/surveys", active="exact", className="text-white"),
            dbc.NavLink("AI Support", href="/ai", active="exact", className="text-white"),
        ], vertical=True, pills=True)
    ], className="sidebar", style={
        "position": "fixed", "top": 0, "left": 0, "bottom": 0,
        "width": "17rem", "padding": "2rem 1rem",
        "backgroundColor": LA_TROBE_RED,
    }),
    html.Div(id="page-content", style={"marginLeft": "18rem", "padding": "2rem 1rem"})
])

def chat_bubble(message, is_user=False):
    return html.Div(message, className="chat-bubble-right" if is_user else "chat-bubble-left")

overview_layout = html.Div([
    html.H2("Overview", style={"color": LA_TROBE_RED}),
    dbc.Row([
        dbc.Col(dbc.Card([dbc.CardHeader("Stress Level"), dbc.CardBody("📈 Stress: Moderate")])),
        dbc.Col(dbc.Card([dbc.CardHeader("Mood Status"), dbc.CardBody("😊 Mood: 60% Positive")]))
    ], className="mb-4"),
    dbc.Card([
        dbc.CardHeader("Daily Input"),
        dbc.CardBody([
            dcc.Textarea(id="input-text", placeholder="Describe how you feel today...", style={"width": "100%", "height": 100}),
            dbc.Button("Submit", id="submit-button", className="custom-btn mt-2"),
            html.Div(id="overview-feedback", className="mt-3")
        ])
    ])
])

reports_layout = html.Div([
    html.H2("Reports", style={"color": LA_TROBE_RED}),
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Monthly Report"),
            dbc.CardBody(dcc.Graph(figure={
                "data": [{"x": ["Jan", "Feb", "Mar", "Apr"], "y": [5, 6, 7, 8], "type": "line"}],
                "layout": {"title": "Stress Over Time"}
            }))
        ])),
        dbc.Col(dbc.Card([
            dbc.CardHeader("Mood Distribution"),
            dbc.CardBody(dcc.Graph(figure={
                "data": [{"labels": ["Positive", "Neutral", "Negative"], "values": [60, 25, 15], "type": "pie"}],
                "layout": {"title": "Mood Pie"}
            }))
        ]))
    ])
])

surveys_layout = html.Div([
    html.H2("Surveys", style={"color": LA_TROBE_RED}),
    dbc.Card([
        dbc.CardHeader("Self Check-in"),
        dbc.CardBody([
            html.P("Over the past week, how often have you felt anxious?"),
            dcc.Slider(0, 10, 1, value=5, id="survey-slider"),
            dbc.Button("Submit", id="survey-submit", className="custom-btn mt-2"),
            html.Div(id="survey-feedback", className="mt-3")
        ])
    ])
])

ai_layout = html.Div([
    html.H2("AI Support", style={"color": LA_TROBE_RED}),
    dbc.Card([
        dbc.CardBody([
            html.Div(id="chat-window", style={"maxHeight": "400px", "overflowY": "auto", "marginBottom": "1rem"}),
            dbc.InputGroup([
                dbc.Input(id="user-message", placeholder="How are you feeling today?"),
                dbc.Button("Send", id="send-button", className="custom-btn")
            ])
        ])
    ])
])

@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def route(path):
    if path == "/":
        return overview_layout
    elif path == "/reports":
        return reports_layout
    elif path == "/surveys":
        return surveys_layout
    elif path == "/ai":
        return ai_layout
    return html.Div("404 Page Not Found")

@app.callback(Output("overview-feedback", "children"), Input("submit-button", "n_clicks"), State("input-text", "value"))
def handle_overview(n, val):
    if n:
        if val and "stress" in val.lower():
            return "😟 Stress detected. Try some deep breaths."
        elif val and "happy" in val.lower():
            return "😊 Great to hear you're happy!"
        return "🧠 Entry recorded. Keep tracking!"
    return ""

@app.callback(Output("survey-feedback", "children"), Input("survey-submit", "n_clicks"), State("survey-slider", "value"))
def handle_survey(n, v):
    if n:
        if v >= 7:
            return "⚠️ High anxiety. Consider relaxation techniques."
        elif v >= 4:
            return "😐 Moderate anxiety. Stay aware."
        else:
            return "😊 You're doing well."
    return ""

@app.callback(Output("chat-store", "data"), Input("send-button", "n_clicks"),
              State("user-message", "value"), State("chat-store", "data"), prevent_initial_call=True)
def handle_chat(n, msg, history):
    if not msg:
        return history
    reply = "🤖 Thank you for sharing."
    if "stress" in msg.lower():
        reply = "😟 I'm sorry you're feeling stressed. Try a breathing exercise."
    elif "happy" in msg.lower():
        reply = "😊 That's wonderful to hear!"
    history.append({"role": "user", "message": msg})
    history.append({"role": "ai", "message": reply})
    return history

@app.callback(Output("chat-window", "children"), Input("chat-store", "data"))
def update_chat(chat_data):
    return [chat_bubble(m["message"], is_user=(m["role"] == "user")) for m in chat_data]

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080)）
    app.run(host="0.0.0.0", port=port, debug=True)

