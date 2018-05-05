from dotenv import load_dotenv
load_dotenv(verbose=True, dotenv_path="./.env")
from flask import Flask, render_template, g, request
from server.helper import *
from pprint import pprint
import cassiopeia as cass
import os

import datetime
import time

import colors
from rfc3339 import rfc3339

app = Flask(__name__, static_folder="./dist")
app.debug = True

@app.before_request
def start_timer():
    g.start = time.time()


@app.after_request
def log_request(response):
    if request.path == '/favicon.ico':
        return response
    elif request.path.startswith('/static'):
        return response

    now = time.time()
    duration = round(now - g.start, 2)
    dt = datetime.datetime.fromtimestamp(now)
    timestamp = rfc3339(dt, utc=True)

    args = dict(request.args)

    log_params = [
        ('method', request.method, 'yellow'),
        ('path', request.path, 'yellow'),
        ('status', response.status_code, 'cyan'),
        ('duration', duration, 'green'),
        ('time', timestamp, 'magenta'),
        ('params', args, 'yellow')
    ]

    request_id = request.headers.get('X-Request-ID')
    if request_id:
        log_params.append(('request_id', request_id, 'yellow'))

    parts = []
    for name, value, color in log_params:
        part = colors.color("{}={}".format(name, value), fg=color)
        parts.append(part)
    line = " ".join(parts)

    app.logger.info(line)

    return response

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
    app.run(debug=True)
