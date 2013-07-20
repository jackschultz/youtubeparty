from youtubeparty import app
from flask import Flask, render_template, url_for, request, redirect
from models import db, YTUrl

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    url = YTUrl(request.form['youtube-url'])
    db.session.add(url)
    db.session.commit()
  queue = db.session.query(YTUrl)
  return render_template('index.html', queue=queue)


