from flask_sqlalchemy import SQLAlchemy
import app

db = SQLAlchemy(app)

class YTUrl(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  url = db.Column(db.String(80))

  def __init__(self, url):
    self.url = url

  def __repr__(self):
    return self.url
