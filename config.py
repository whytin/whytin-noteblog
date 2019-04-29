import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
	SSL_DISABLE = False
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_RECORD_QUERIES = True
	SIMPLEMDE_JS_IIFE=True
	SIMPLEMDE_USE_CDN=True	
	
	@staticmethod
	def init_app(app):
		pass


class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
	WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'data.sqlite')

class UnixConfig(ProductionConfig):
	@classmethod
	def init_app(cls, app):
		ProductionConfig.init_app(app)
		
		import logging
		from logging.handlers import SysLogHandler
		syslog_handler = SysLogHandler()
		syslog_handler.setLevel(logging.WARNING)
		app.logger.addHandler(syslog_handler)


class HerokuConfig(ProductionConfig):
	SSL_REDIRECT = True if os.environ.get('DYNO') else False

	@classmethod
	def init_app(cls, app):
		ProductionConfig.init_app(app)

		# handle reverse proxy server headers
		from werkzeug.contrib.fixers import ProxyFix
		app.wsgi_app = ProxyFix(app.wsgi_app)
		
		# log to stderr
		import logging
		from logging import StreamHandler
		file_handler = StreamHandler()
		file_handler.setLevel(logging.INFO)
		app.logger.addHandler(file_handler)



config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,
	'unix': UnixConfig,
	'heroku': HerokuConfig,
	'default': DevelopmentConfig
}

