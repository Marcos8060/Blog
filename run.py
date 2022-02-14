from app import app
from  flask_migrate import Migrate, MigrateCommand
from app import app,db
from flask_script import Manager,Server
from app.models import User,Comment,Blog

# Creating app instance
# app = create_app('development')


manager = Manager(app)
manager.add_command('server',Server)

@manager.shell
def make_shell_context():
    return dict(app = app,db = db, User=User, Comment = Comment, 
            Blog = Blog)

migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

manager.add_command('server',Server)
if __name__ == '__main__':
    manager.run()


if __name__ == '__main__':
    app.run(debug=True)