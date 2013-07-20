from flask import Flask, render_template, url_for, request, redirect

import os

app = Flask(__name__)

env = os.environ.get('YTP_ENV','prod')
app.config.from_object('youtubeparty.settings.DevConfig')
app.debug = True

import youtubeparty.views
import youtubeparty.models

if __name__ == '__main__':
  app.run()
