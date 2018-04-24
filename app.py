from dotenv import load_dotenv
load_dotenv(verbose=True, dotenv_path="./.env")
from flask import Flask, render_template
from server.helper import *
from pprint import pprint
import cassiopeia as cass
import os

app = Flask(__name__, static_folder="./dist")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hello")
def hello():
    return "Hello World!"

@app.route("/<region>/<summoner_name>")
def in_game(region, summoner_name):
    region = region.upper() # maybe upcase? or downcase?
    summoner = get_summoner(region, summoner_name)
    summoner.id
    print("Name:", summoner.name)
    print("ID:", summoner.id)
    print("Account ID:", summoner.account.id)
    print("Level:", summoner.level)
    print("Revision date:", summoner.revision_date)
    print("Profile icon ID:", summoner.profile_icon.id)
    print("Profile icon name:", summoner.profile_icon.name)
    print("Profile icon URL:", summoner.profile_icon.url)
    print("Profile icon image:", summoner.profile_icon.image)
    pprint(vars(summoner))
    return region + ", " + summoner_name

if __name__ == '__main__':
    app.run()
