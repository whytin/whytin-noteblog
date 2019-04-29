#!/usr/bin/env python
import os
import click
from app import create_app, db
from app.models import User,Say,Post,Link,Tag,Comment
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand,init,migrate,upgrade

app=create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate=Migrate(app,db)
manager=Manager(app)


@app.shell_context_processor
def make_shell_context():
	return dict(app=app, db=db, User=User,Say=Say,Post=Post,Link=Link,Tag=Tag,Comment=Comment)


@manager.command
#@click.option('--length', default=25,help='Number of functions to include in the profiler report.')
#@click.option('--profile-dir', default=None,help='Directory where profiler data files are saved.')
def profile(length, profile_dir):
	"""Start the application under the code profiler."""
	from werkzeug.contrib.profiler import ProfilerMiddleware
	app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],profile_dir=profile_dir)
	app.run()


@manager.command
def init_data():
	"""Run deployment tasks."""
	db.create_all()
	admin_name=os.environ.get('FLASK_ADMIN_NAME')
	admin_email=os.environ.get('FLASK_ADMIN_EMAIL')
	admin_password=os.environ.get('FLASK_ADMIN_PASSWORD')
	user_admin=User(name=admin_name,email=admin_email,password=admin_password)
	db.session.add(user_admin)
	db.session.commit()

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)

if __name__=='__main__':
	manager.run()


