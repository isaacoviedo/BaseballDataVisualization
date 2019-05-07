import json
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_jsglue import JSGlue
from player import Player
from team import Team
from pprint import pprint
from utils import *

app = Flask(__name__)
jsglue = JSGlue()
jsglue.init_app(app)

# When trying to get all the teams in the database
# {teamID: {$regex: "^((?!KCA|NYA|HOU|SLN|NYN|NYP|NY1|SFN|CHA|TOR|PHI|SEA|CHN|MIA|FLO|ARI|MIN|BOS|TEX|PIT|CHP|ATL|ML1|BSN|LAN|BRO|CLE|TBA|LAA|ANA|CAL|MIL|ML4|MLA|ML3|MLU|PHI|SDN|DET|BAL|BLN|BL3|BL2|BLA|KC1|OAK|PH4|PHP|PHA|PHN|PH1|BS2|BSP|CNU|BSU|CIN|CN1|WS8|WS4|WSU|WS6|WS7|WAS|MON|COL|FW1|CL1|NY2|BS1|RC1|TRO).)*$"}}
# -------------- MAIN INDEX --------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search_bar", methods=["POST"])
def search_bar():
    
    # want to make sure we handle no input
    # if request.form['pname']:
    #     player = Player(request.form['pname'])
    #     player.get_appearances()
    #     return redirect( url_for('about') )
    # else:
    #     return redirect( url_for('index') )
    
    return render_template("under_construction.html")


@app.route("/about")
def about():
    return render_template("under_construction.html")

@app.route("/dashboard")
def dashboard():
    return "Dashboard loaded here"

@app.route("/profile")
def profile_main():

    SUBLISTNUM = 6
    tList = get_active_teams()
    tList = [ tList[ x : x+SUBLISTNUM ] for x in range(0 ,len(tList), SUBLISTNUM) ]
    return render_template("profile.html", teamsList = tList)


@app.route("/profile/player")
def profile_player():
    return jsonify(request.form)

@app.route("/profile/team/<string:franchid>")
def profile_team(franchid):
    '''
        param:
            - teamid : the id of the team as noted in the mongodb
    '''
    # get all the information pertaining to that team
    team = Team(franchid)
    rangeObj = team.gen_minmax()
    nmList = team.get_all_names()

    return render_template("team_profile.html", docList = team.docs, rangeD = rangeObj, namesList = nmList)

if __name__ == "__main__":
    app.run(debug=True)