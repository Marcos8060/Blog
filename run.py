from app import app
from  flask_migrate import Migrate, MigrateCommand
from app import app,db
from flask_script import Manager,Server

# Creating app instance
# app = create_app('development')


manager = Manager(app)
manager.add_command('server',Server)

migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

manager.add_command('server',Server)
if __name__ == '__main__':
    manager.run()


if __name__ == '__main__':
    app.run(debug=True)