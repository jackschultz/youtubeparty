import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///datebase.db'
SQLALCHEMY_MIGRATE_REPO = 'db_repository'

#if I do go for flask-WTF, then this
SECRET_KEY='dont-know-why-this-is-here'
CSRF_ENABLED = False



