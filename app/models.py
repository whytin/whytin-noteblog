#-*- coding:utf-8 -*-
from . import db,login_manager
from flask import current_app,url_for
from flask_login import UserMixin,AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from markdown import markdown
import bleach
import time
from datetime import datetime



class User(UserMixin,db.Model):
	__tablename__='users'
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(128),unique=True)
	email=db.Column(db.String(64),unique=True,index=True)
	password_hash=db.Column(db.String(128))
	posts=db.relationship('Post',backref='author',lazy='dynamic')
	says=db.relationship('Say',backref='author',lazy='dynamic')
	links=db.relationship('Link',backref='author',lazy='dynamic')
	comments=db.relationship('Comment',backref='author',lazy='dynamic')

	def __repr__(self):
		return '<User %r>' %self.email
	
	@property
	def password(self):
		raise AttributeError('password is not a readable atribute')

	@password.setter
	def password(self,password):
		self.password_hash=generate_password_hash(password)

	def verify_password(self,password):
		return check_password_hash(self.password_hash,password)
	
	def to_json(self):
		json_user={
			'url':url_for('api.get_user',id=self.id),
			'name':self.name,
			'posts':url_for('api.get_user_posts',id=self.id),
			'posts_count':self.posts.count(),
			'says':url_for('api.get_user_says',id=self.id),
			'says_count':self.says.count(),
			'links':url_for('api.get_user_links',id=self.id),
			'links_count':self.links.count(),
			'comments':url_for('api.get_user_comments',id=self.id),
			'comments_count':self.comments.count()
		}
		return json_user		

	
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class AnonymousUser(AnonymousUserMixin):
	def can(self,permissions):
		return False
	def is_administrator(self):
		return False
login_manager.anonymous_user=AnonymousUser



class Say(db.Model):
	__tablename__='says'
	id=db.Column(db.Integer,primary_key=True)
	content=db.Column(db.Text)
	create_time=db.Column(db.DateTime,default=datetime.now(),index=True)
	like=db.Column(db.Integer,default=0)
	author_id=db.Column(db.Integer,db.ForeignKey('users.id'))

	def formatDate(self):
		str=self.create_time.strftime('%Y-%m-%d')
		return str

	def formatTime(self):
		str=self.create_time.strftime('%H:%M')
		return str

	def to_json(self):
		json_say={
			'url':url_for('api.get_say',id=self.id),
			'create_time':self.create_time,
			'content':self.content,
			'like':self.like
		}
		return json_say
	
	@staticmethod
	def from_json(json_say):
		content=json_say.get('content')
		if content is None or content=='':
			raise ValidationError('say does not have a content')
		return Say(content=content)


tag_post=db.Table('tag_post',
		db.Column('tag_id',db.Integer,db.ForeignKey('tags.id')),
		db.Column('post_id',db.Integer,db.ForeignKey('posts.id')))

class Post(db.Model):
	__tablename__='posts'
	id=db.Column(db.Integer,primary_key=True)
	title=db.Column(db.String(128))
	brief=db.Column(db.String(256))
	content=db.Column(db.Text)
	content_html=db.Column(db.Text)
	create_time=db.Column(db.DateTime,default=datetime.now(),index=True)
	update_time=db.Column(db.DateTime,default=datetime.now())
	category=db.Column(db.String(64),index=True)
	view=db.Column(db.Integer,default=0)	
	author_id=db.Column(db.Integer,db.ForeignKey('users.id'))
	tags=db.relationship('Tag',secondary=tag_post,
			backref=db.backref('posts',lazy='dynamic'))
	comments=db.relationship('Comment',backref='post',lazy='dynamic')	


	def __repr__(self):
		return '<Post %r>'%self.title	

	def formatCreateTime(self):
		str=self.create_time.strftime('%Y-%m-%d %H:%M')
		return str

	def formatUpdateTime(self):
		str=self.update_time.strftime('%Y-%m-%d %H:%M')
		return str
	
	def to_json(self):
		json_post={
			'url':url_for('api.get_post',id=self.id),
			'title':self.title,
            'category':self.category,
			'brief':self.brief,
			'content':self.content,
			'content_html':self.content_html,
			'create_time':self.create_time,
			'update_time':self.update_time,
			'view':self.view,
			'comments':[comment.to_json() for comment in self.comments],
			'comments_count':self.comments.count(),
			'tags':[url_for('api.get_post_tags',id=self.id) for tag in self.tags],
			'tags_count':len(self.tags)
		}
		return json_post

	@staticmethod
	def from_json(json_post):
		content=json_post.get('content')
		if content is None or content=='':
			raise ValidationError('post does not have a content')
		return Post(content=content)


class Link(db.Model):
	__tablename__='links'
	id=db.Column(db.Integer,primary_key=True)
	link=db.Column(db.Text)
	name=db.Column(db.String)
	create_time=db.Column(db.DateTime,default=datetime.now())
	author_id=db.Column(db.Integer,db.ForeignKey('users.id'))

	def __repr__(self):
		return '<Link %r>'%link

	def to_json(self):
		json_link={
			'url':url_for('api.get_link',id=self.id),
			'link':self.link,
			'name':self.name,
			'create_time':self.create_time,
		}
		return json_link

	@staticmethod
	def from_json(json_link):
		link=json_link.get('link')
		if link is None or link=='':
			raise ValidtationError('link does not exit')
		return Link(link=link)


class Tag(db.Model):
	__tablename__='tags'
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String,unique=True,index=True)
	create_time=db.Column(db.DateTime,default=datetime.now())

	def to_json(self):
		json_tag={
			'url':url_for('api.get_tag',id=self.id),
			'name':self.name,
			'tag_posts':url_for('api.get_tag_posts',id=self.id),
			'tag_posts_count':self.posts.count()
		}	
		return json_tag
	

class Comment(db.Model):
	__tablename__='comments'
	id=db.Column(db.Integer,primary_key=True)
	content=db.Column(db.Text)
	content_html=db.Column(db.Text)
	create_time=db.Column(db.DateTime,default=datetime.now(),index=True)
	author_id=db.Column(db.Integer,db.ForeignKey('users.id'))
	post_id=db.Column(db.Integer,db.ForeignKey('posts.id'))


	def formatCreateTime(self):
		str=self.create_time.strftime('%Y-%m-%d %H:%M')
		return str

	def to_json(self):
		json_comment={
			'url':url_for('api.get_comment',id=self.id),
			'post_url':url_for('api.get_post',id=self.post_id),
			'author':url_for('api.get_user',id=self.author_id),
			'create_time':self.create_time,
			'content':self.content,
			'content_html':self.content_html
		}
		return json_comment

	@staticmethod
	def from_json(json_comment):
		content=json_post.get('content')
		if content is None or content=='':
			raise ValidationError('comment does not have a content')
		return Comment(content=content)

