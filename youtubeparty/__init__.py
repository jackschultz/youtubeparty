from flask import Flask#, render_template, url_for, request, redirect

import os

app = Flask(__name__)

env = os.environ.get('YTP_ENV','prod')
app.config.from_object('youtubeparty.settings.DevConfig')

import youtubeparty.views

