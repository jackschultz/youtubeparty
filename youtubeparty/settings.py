class Config(object):
  pass


class ProdConfig(Config):
  pass


class DevConfig(Config):
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = 'sqlite:///datebase.db'
  SQLALCHEMY_MIGRATE_REPO = 'db_repository'
  SQLALCHEMY_ECHO = True

