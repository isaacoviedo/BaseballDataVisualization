import json
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_jsglue import JSGlue
from player import Player
from team import Team
from pprint import pprint

app = Flask(__name__)
jsglue = JSGlue()
jsglue.init_app(app)

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

@app.route("/profile/team/<string:teamid>")
def profile_team(teamid):
    '''
        param:
            - teamid : the id of the team as noted in the mongodb
    '''
    # get all the information pertaninig to that team
    team = Team(teamid)
    rangeObj = team.gen_minmax(['yearID','Rank','W','L','2B','3B','HR','SB','ERA','HRA'])

    return render_template("team_profile.html", docList = team.docs, rangeD = rangeObj)

@app.route("/build_pplot", methods=['POST'])
def build_pplot():

    print("Im here")

    if request.method == 'GET':

        vals = request.json['data']
        print(vals)

    else:
        vals = request.args
        print(vals)
        print("Nothing")

    return ''


if __name__ == "__main__":
    app.run(debug=True)