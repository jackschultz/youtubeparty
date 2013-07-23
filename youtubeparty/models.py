from flask_sqlalchemy import SQLAlchemy
from youtubeparty import app
import uuid

db = SQLAlchemy(app)

class Room(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50))
  urls = db.relationship('YTUrl', backref='room', lazy='dynamic')
 
  def __init__(self, name):
    check = not None
    while check is not None:
      poss_id = int(str(uuid.uuid4().int)[0:6])
      check = Room.query.get(poss_id)
    self.id = poss_id
    self.name = name
 
  def __repr__(self):
    return self.name
 
class YTUrl(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  url = db.Column(db.String(80))
  title = db.Column(db.String(40))
  video_key = db.Column(db.String(20))
  room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
 
  def __init__(self, url, title, video_key, room_id):
    self.url = url
    self.title = title
    self.video_key = video_key
    self.room_id = room_id
 
  def __repr__(self):
    return self.title

db.create_all()

