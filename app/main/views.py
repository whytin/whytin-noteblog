#-*- coding:utf-8 -*-
from flask import render_template,redirect,url_for,abort,flash,request
from flask_login import login_required,current_user
from .forms import SayForm, PostForm,LinkForm,CommentForm
from . import main
from .. import db
from .. import simplemde
from ..models import User,Say,Post,Link,Tag,Comment
from datetime import datetime
import markdown



@main.route('/',methods=['GET','POST'])
def home():
	page=request.args.get('page',1,type=int)
	pagination=Post.query.order_by(Post.create_time.desc()).paginate(page,per_page=10,error_out=False)
	posts=pagination.items
	return render_template('home.html',posts=posts,pagination=pagination)


@main.route('/new_post',methods=['GET','POST'])
@login_required
def new_post():
	form=PostForm()
	if request.method=="POST" and form.validate_on_submit():
		content=form.content.data
		content_html=markdown.markdown(content)
		post=Post(title=form.title.data,author=current_user,category=form.category.data,brief=form.brief.data,content=content,content_html=content_html,create_time=datetime.now(),update_time=datetime.now())
		tag_list=form.tag.data.split(',')
		for tag_name in tag_list:
			t=db.session.query(Tag).filter(Tag.name==tag_name).first()
			if not t:
				t=Tag(name=tag_name)
			post.tags.append(t)
		db.session.add(post)
		db.session.commit()
		return redirect(url_for('.post',id=post.id,title=post.title))
		flash(u'成功创建文章！')
	return render_template('new_post.html',form=form)


@main.route('/post/<int:id>/<title>',methods=['GET','POST'])
def post(id,title):
	post=Post.query.get_or_404(id)
	form=CommentForm()
	if request.method=='POST' and form.validate_on_submit():
		user=User.query.filter_by(email=form.email.data).first()
		if not user:
			user=User(name=form.name.data,email=form.email.data,password='888888')
			db.session.add(user)
		content=form.comment.data
		content_html=markdown.markdown(content)
		comment=Comment(content=content,content_html=content_html,author=user,post=post,create_time=datetime.now())
		db.session.add(comment)
		db.session.commit()
		flash(u'评论发表成功')
		return redirect(url_for('.post',id=post.id,title=title,page=-1))
	page=request.args.get('page',1,type=int)
	if page==-1:
		page=(post.comments.count()-1)/10+1
	pagination=post.comments.order_by(Comment.create_time.asc()).paginate(page,per_page=10,error_out=False)
	comments=pagination.items	
	post.view+=1
	return render_template('post.html',post=post,title=title,form=form,comments=comments,pagination=pagination)


@main.route('/edit_post/<int:id>/<title>',methods=['GET','POST'])
@login_required
def edit_post(id,title):
	post=Post.query.get_or_404(id)
	form=PostForm()
	if request.method=='POST' and form.validate_on_submit():
		post.title=form.title.data
		post.category=form.category.data
		post.brief=form.brief.data
		post.content=form.content.data
		post.content_html=markdown.markdown(post.content)
		post.update_time=datetime.now()
		tag_list_n=form.tag.data.split(',')
		tag_list_now=[]
		for tag_name in tag_list_n:
			t=db.session.query(Tag).filter(Tag.name==tag_name).first()
			if not t:
				t=Tag(name=tag_name)
			tag_list_now.append(t)
		post.tags=tag_list_now
		db.session.commit()
		return redirect(url_for('.post',id=post.id,title=post.title))
		flash(u'成功更新文章！')
	form.title.data=post.title
	form.category.data=post.category
	form.brief.data=post.brief
	form.content.data=post.content
	tag_dict=post.tags
	tag_list=""
	for t in tag_dict:
		tag_list=tag_list+t.name+","
	form.tag.data=tag_list[:-1]
	return render_template('edit_post.html',form=form,post=post)


#@main.route('/delete_post/<int:id>/<title>',methods=['GET','POST'])
#@login_required
#def delete_post(id,title):
	#post=Post.query.get_or_404(id)
    #form=PostForm()
    #if request.method=='POST' and form.validate_on_submit():
		#db.session.delete(post)
		#db.session.commit()
		#flash(u'成功删除文章!')
		#return redirect('.home')


@main.route('/say',methods=['GET','POST'])
def say():
	page=request.args.get('page',1,type=int)
	pagination=Say.query.order_by(Say.create_time.desc()).paginate(page,per_page=10,error_out=False)
	says=pagination.items
	return render_template('say.html',says=says,pagination=pagination)

@main.route('/new_say',methods=['GET','POST'])
@login_required
def new_say():
	form=SayForm()
	if request.method=="POST" and form.validate_on_submit():
		say=Say(content=form.content.data,create_time=datetime.now(),author=current_user)
		db.session.add(say)
		db.session.commit()
		flash(u'成功发表说说!')
		return redirect(url_for('.say'))
	return render_template('new_say.html',form=form)


@main.route('/link',methods=['GET','POST'])
def link():
    links=Link.query.order_by(Link.create_time.asc())
    return render_template('link.html',links=links)

@main.route('/new_link',methods=['GET','POST'])
@login_required
def new_link():
	form=LinkForm()
	if request.method=="POST" and form.validate_on_submit():
		link=Link(name=form.name.data,link=form.link.data,create_time=datetime.now(),author=current_user)
		db.session.add(link)
		db.session.commit()
		flash(u'成功添加友链!')
		return redirect(url_for('.link'))
	return render_template('new_link.html',form=form)


@main.route('/technique')
def technique():
	page=request.args.get('page',1,type=int)
	pagination=Post.query.filter_by(category='technique').order_by(Post.create_time.desc()).paginate(page,per_page=10,error_out=False)
	posts=pagination.items
	return render_template('technique.html',posts=posts,pagination=pagination)


@main.route('/life')
def life():
	page=request.args.get('page',1,type=int)
	pagination=Post.query.filter_by(category='life').order_by(Post.create_time.desc()).paginate(page,per_page=10,error_out=False)
	posts=pagination.items
	return render_template('life.html',posts=posts,pagination=pagination)


@main.route('/tag',methods=['GET','POST'])
def tag():	
	tag_list=Tag.query.all()
	for tag in tag_list:
		if tag.posts.count()==0:
			db.session.delete(tag)
			db.session.commit()
			tag_list.remove(tag)
	if tag_list:
		return render_template('tag.html',tag_list=tag_list)
	else:
		abort(404)
		return render_template('404.html')

@main.route('/tag_detail/<int:id>/<name>',methods=['GET','POST'])
def tag_detail(id,name):
	tag=Tag.query.get_or_404(id)
	page=request.args.get('page',1,type=int)
	pagination=tag.posts.order_by(Post.create_time.desc()).paginate(page,per_page=10,error_out=False)
	posts=pagination.items
	return render_template('tag_detail.html',tag=tag,name=name,posts=posts,pagination=pagination)	


@main.route('/about')
def about():
	return render_template('about.html')




