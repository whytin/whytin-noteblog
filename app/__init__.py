#-*- coding:utf-8 -*-
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_simplemde import SimpleMDE
from config import config
from flask_admin import Admin,AdminIndexView


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
simplemde = SimpleMDE()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	bootstrap.init_app(app)
	mail.init_app(app)
	moment.init_app(app)
	db.init_app(app)
	login_manager.init_app(app)
	simplemde.init_app(app)
	
	from .admin import admin
	admin.init_app(app)	

	from .admin import NewPostView,NewSayView,NewLinkView,UserView,PostView,SayView,LinkView
	admin.add_view(NewPostView(name=u'写文章',endpoint='new_post'))
	admin.add_view(NewSayView(name=u'写说说',endpoint='new_say'))
	admin.add_view(NewLinkView(name=u'添加友链',endpoint='new_link'))
	admin.add_view(UserView(db.session,name=u'用户管理',endpoint='users'))
	admin.add_view(PostView(db.session,name=u'文章管理',endpoint='posts'))
	admin.add_view(SayView(db.session,name=u'说说管理',endpoint='says'))
	admin.add_view(LinkView(db.session,name=u'友链管理',endpoint='links'))

	if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
		from flask_sslify import SSLify
		sslify = SSLify(app)

	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint, url_prefix='/auth')

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	from .api import api as api_blueprint
	app.register_blueprint(api_blueprint,url_prefix='/api')

	return app


