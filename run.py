import os
from datetime import datetime
from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "string"
messages = []


def add_message(username, message):
    """strptime() gives the format, %H = hours in 24 hour clock etc."""
    now = datetime.now().strftime("%H:%M:%S")
    # now converts date-time object to string
    messages.append({"timestamp": now, "from": username, "message": message})


@app.route("/", methods=["GET", "POST"])
def index():
    """Main page with instructions"""
    if request.method == "POST":
        session["username"] = request.form["username"]
        # if form is posted create new variable in session called username
    if "username" in session:
        # if username exists then direct to username view
        return redirect(url_for("user", username=session["username"]))

    return render_template("index.html")


@app.route("/chat/<username>", methods=["GET", "POST"])
# username declared as variable
def user(username):
    """Add and display chat messages"""
    if(request.method) == "POST":
        username = session["username"]
        message = request.form["message"]
        add_message(username, message)
        return redirect(session["username"])
        """ Without the retrun redirect every time
        the page refreshes it resends the POST data amd will
        keep re-sending the same message, after redirect POST
        will be false and chat.html will render"""
    return render_template(
        "chat.html", username=username, chat_messages=messages)


app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)
