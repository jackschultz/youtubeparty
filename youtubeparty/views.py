from youtubeparty import app
from flask import Flask, render_template, url_for, request, redirect, jsonify, abort
from models import db, YTUrl, Room
import urlparse
import cgi
import json
import requests
import pdb

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    try:
      name = request.form['room-name']
    except KeyError:
      abort(400)
    room = Room(name=name)
    db.session.add(room)
    db.session.commit()
    return redirect(url_for('room', rid=room.id))
  return render_template('index.html')
  
@app.route('/room/<rid>', methods=['GET', 'POST'])
def room(rid):
  room = Room.query.get_or_404(rid)
  if request.method == 'POST':
    poss_url = request.form['youtube-url']
    parsed_url = urlparse.urlparse(poss_url)
    if parsed_url[1] == app.config['YOUTUBE_URL']:
      query_dict = cgi.parse_qs(parsed_url[4])
      try:
        video_key = query_dict['v'][0]
      except ValueError:
        errors = "Video not found"
        return jsonify(success=False, errors=errors)
        abort(500)
      data_url = app.config['YOUTUBE_DATA_URL'] + video_key + app.config['YOUTUBE_DATA_PARAMS_URL']
      resp = requests.get(data_url)
      if resp.status_code != 200:
        errors = "Video not found"
        return jsonify(success=False, errors=errors)
      video_info_dict = resp.json()
      title = video_info_dict['entry']['title']['$t']
      url = YTUrl(poss_url, title, video_key, rid)
      db.session.add(url)
      db.session.commit()
      return jsonify(success=True)
    errors = "Need Youtube url"
    return jsonify(success=False, errors=errors) 
  queue = room.urls
  return render_template('room.html', queue=queue, room=room)

@app.route('/update/<rid>')
def update(rid):
  room = Room.query.get(rid)
  if room is None:
    return abort(404)
  queue = room.urls
  queue_list = []
  for q in queue:
    queue_list.append({'title':q.title,'key':q.video_key})
  return jsonify(queue=queue_list)

