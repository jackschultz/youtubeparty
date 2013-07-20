from flaskext.script import Manager, Shell, Server
from youtubeparty import app

manager = Manager(app)
manager.add_commend('runserver',Server())
manager.add_command('shell', Shell())
manager.run()
