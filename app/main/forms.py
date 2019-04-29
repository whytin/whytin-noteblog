#-*- coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,BooleanField,SelectField,SubmitField,PasswordField
from wtforms.validators import Required,Length,Email,Regexp
from wtforms import ValidationError
from .. models import User,Say,Post,Link,Tag



class SayForm(FlaskForm):
	content=TextAreaField(u'嗨，在想什么呢？',validators=[Required()])
	submit=SubmitField(u'提交')

class PostForm(FlaskForm):
	title=StringField(u'标题',validators=[Required(),Length(0,64)])
	category=SelectField(u'分类',validators=[Required()],choices=[('technique','technique'),('life','life')])
	tag=StringField(u'标签',validators=[Required()])
	brief=TextAreaField(u'摘要',validators=[Required()])
	content=TextAreaField(u'文章内容',validators=[Required()])
	submit=SubmitField(u'提交')


class LinkForm(FlaskForm):
	link=TextAreaField(u'链接',validators=[Required(),Length(0,256)])
	name=StringField(u'名字',validators=[Required(),Length(0,256)])
	submit=SubmitField(u'提交')


class CommentForm(FlaskForm):
	email=StringField(u'Email',validators=[Required(),Length(0,256),Email()])
	name=StringField(u'昵称',validators=[Required(),Length(0,256)])
	comment=TextAreaField(u'写点什么吧..',validators=[Required()])
	submit=SubmitField(u'评论')


