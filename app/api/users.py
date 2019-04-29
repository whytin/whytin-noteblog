from flask import jsonify,request,url_for
from . import api
from ..models import User,Post,Say,Link,Comment


@api.route('/users/<int:id>')
def get_user(id):
	user=User.query.get_or_404(id)
	return jsonify(user.to_json())


@api.route('/users/<int:id>/posts/')
def get_user_posts(id):
	user=User.query.get_or_404(id)
	page=request.args.get('page',1,type=int)
	pagination=user.posts.order_by(Post.create_time.desc()).paginate(page,per_page=10,error_out=False)
	posts=pagination.items
	prev=None
	if pagination.has_prev:
		prev=url_for('api.get_user_posts',id=id,page=page-1)
	next=None
	if pagination.has_next:
		next=url_for('api.get_user_posts',id=id,page=page+1)
	return jsonify({
		'posts':[post.to_json() for post in posts],
		'prev':prev,
		'next':next,
		'count':pagination.total
	})


@api.route('/users/<int:id>/says/')
def get_user_says(id):
	user=User.query.get_or_404(id)
	page=request.args.get('page',1,type=int)
	pagination=user.says.order_by(Say.create_time.desc()).paginate(page,per_page=10,error_out=False)
	says=pagination.items
	prev=None
	if pagination.has_prev:
		prev=url_for('api.get_user_says',id=id,page=page-1)
	next=None
	if pagination.has_next:
		next=url_for('api.get_user_says',id=id,page=page+1)
	return jsonify({
		'says':[say.to_json() for say in says],
		'prev':prev,
		'next':next,
		'count':pagination.total
	})


@api.route('/users/<int:id>/links/')
def get_user_links(id):
	user=User.query.get_or_404(id)
	page=request.args.get('page',1,type=int)
	pagination=user.links.order_by(Link.create_time.desc()).paginate(page,per_page=10,error_out=False)
	links=pagination.items
	prev=None
	if pagination.has_prev:
		prev=url_for('api.get_user_links',id=id,page=page-1)
	next=None
	if pagination.has_next:
		next=url_for('api.get_user_links',id=id,page=page+1)
	return jsonify({
		'links':[link.to_json() for link in links],
		'prev':prev,
		'next':next,
		'count':pagination.total
	})


@api.route('/users/<int:id>/comments/')
def get_user_comments(id):
	user=User.query.get_or_404(id)
	page=request.args.get('page',1,type=int)
	pagination=user.comments.order_by(Comment.create_time.desc()).paginate(page,per_page=10,error_out=False)
	comments=pagination.items
	prev=None
	if pagination.has_prev:
		prev=url_for('api.get_user_comments',id=id,page=page-1)
	next=None
	if pagination.has_next:
		next=url_for('api.get_user_comments',id=id,page=page+1)
	return jsonify({
		'comments':[comment.to_json() for comment in comments],
		'prev':prev,
		'next':next,
		'count':pagination.total
	})


