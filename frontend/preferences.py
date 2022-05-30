import flask
from flask import render_template

def renderPreferenceSite(request : flask.Request) -> str:
    return render_template('preferences.html')
