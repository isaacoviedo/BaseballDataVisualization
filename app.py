import json
import sys
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
from flask_jsglue import JSGlue
from player import Player
from team import Team
from pprint import pprint
from utils import *
from db import connect

app = Flask(__name__)
jsglue = JSGlue()
jsglue.init_app(app)

# -------------- MAIN INDEX --------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search_bar", methods=["POST"])
def search_bar():
    
    # Want to make sure we handle no input
    if request.form['pname']:

        name = request.form['pname']
        resList = get_search_results(name)
        resListSz = len(resList)

        if resListSz == 1:
            return redirect( url_for('profile_player', playerID = resList[0].profile.get('playerID') ) )
        elif resListSz > 1:
            return render_template( "search_results.html", searchResList = resList, searchedFor = name, teamObj = Team() )
        else:
            flash('No player found with name: {}'.format(name))
            return redirect( url_for('index') )
        
    else:
        flash('No input given. Please try again!')
        return redirect( url_for('index') )


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

@app.route("/profile/player/<string:playerID>")
def profile_player(playerID):

    player = Player(playerID)
    salaryList, yearsList = player.get_salaries()
    teamsList = player.get_teams()
    src = player.get_picture()

    return render_template("player_profile.html", player = player, salaryList = salaryList, yearsList = yearsList, teamsList = teamsList, hs_src=src)

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


@app.route("/search/results")
def search_results():
    return 'Hi'

if __name__ == "__main__":
    app.secret_key = 'super secret'

    if 'local' in sys.argv:
        app.run(debug=True)
    else:
        app.run(debug=False)