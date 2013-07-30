class Config(object):
 YOUTUBE_URL = 'www.youtube.com'
 YOUTUBE_DATA_URL = 'https://gdata.youtube.com/feeds/api/videos/'
 YOUTUBE_DATA_PARAMS_URL = '?v=2&alt=json'



class ProdConfig(Config):
  SQLALCHEMY_DATABASE_URI = 'sqlite:///datebase.db'


class DevConfig(Config):
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = 'sqlite:///datebase.db'
  SQLALCHEMY_MIGRATE_REPO = 'db_repository'
  SQLALCHEMY_ECHO = True

