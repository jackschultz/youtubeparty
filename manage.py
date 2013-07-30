from flask.ext.script import Manager, Shell, Server
from youtubeparty import app

manager = Manager(app)
manager.add_command('runserver',Server())
manager.add_command('shell', Shell())

@manager.command
def syncdb():
  from youtubeparty.models import db
  db.create_all()

if __name__ == '__main__':
  manager.run()
