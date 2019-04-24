from flask import Flask, render_template, request, redirect, url_for, jsonify
from player import Player
from team import Team
from pprint import pprint

app = Flask(__name__)

# -------------- MAIN INDEX --------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search_bar", methods=["POST"])
def search_bar():
    
    # want to make sure we handle no input
    if request.form['pname']:
        player = Player(request.form['pname'])
        player.get_appearances()
        return redirect( url_for('about') )
    else:
        return redirect( url_for('index') )


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/dashboard")
def dashboard():
    return "Dashboard loaded here"

@app.route("/profile")
def profile_main():
    return render_template("profile.html")


@app.route("/profile/player")
def profile_player():
    return jsonify(request.form)

@app.route("/profile/team/<string:tname>")
def profile_team(tname):

    # get all the information pertaninig to that team
    team = Team(tname)

    return render_template("team_profile.html", docList = team.docs)


if __name__ == "__main__":
    app.run(debug=True)