from youtubeparty import app
from flask import Flask, render_template, url_for, request, redirect, jsonify, abort
from models import db, YTUrl, Room
import urlparse
import cgi
import json
import requests
import pdb

YOUTUBE_URL = 'www.youtube.com'

#for splitting up the get request for info
YOUTUBE_DATA_URL = 'https://gdata.youtube.com/feeds/api/videos/'
YOUTUBE_DATA_PARAMS_URL = '?v=2&alt=json'

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    name = request.form['room-name']
    room = Room(name=name)
    db.session.add(room)
    db.session.commit()
    return redirect(url_for('room', rid=room.id))
  return render_template('index.html')
  
@app.route('/room/<rid>', methods=['GET', 'POST'])
def room(rid):
  room = Room.query.get(rid)
  if room is None:
    return abort(404)
  if request.method == 'POST':
    #pdb.set_trace()
    poss_url = request.form['youtube-url']
    parsed_url = urlparse.urlparse(poss_url)
    if parsed_url[1] == YOUTUBE_URL:
      query_dict = cgi.parse_qs(parsed_url[4])
      try:
        video_key = query_dict['v'][0]
      except ValueError:
        #odd, but we need error checking. just ditch
        abort(500)
      data_url = YOUTUBE_DATA_URL + video_key + YOUTUBE_DATA_PARAMS_URL
      resp = requests.get(data_url)
      video_info_dict = resp.json()
      title = video_info_dict['entry']['title']['$t']
      url = YTUrl(poss_url, title, video_key, rid)
      db.session.add(url)
      db.session.commit()
      return jsonify(success=True)
    return jsonify(success=False) #here we want to give errors...
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
    info = {}
    info['title'] = q.title
    info['key'] = q.video_key
    queue_list.append(info)
  return jsonify(queue=queue_list)

