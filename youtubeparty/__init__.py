from flask import Flask#, render_template, url_for, request, redirect

import os

app = Flask(__name__)

conf = {
  'dev': 'youtubeparty.settings.DevConfig',
  'prod': 'youtubeparty.settings.ProdConfig'
}

app.config.from_object(conf[os.environ.get('YTP_ENV','dev')])

import youtubeparty.views

