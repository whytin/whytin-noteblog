from flask import jsonify,request,g,url_for
from flask_login import login_required
from . import api
from ..models import Post,Tag
from .errors import forbidden

@api.route('/posts/')
def get_posts():
	page=request.args.get('page', 1, type=int)
	pagination=Post.query.order_by(Post.create_time.desc()).paginate(page, per_page=10,error_out=False)
	posts=pagination.items
	prev=None
	if pagination.has_prev:
		prev=url_for('api.get_posts', page=page-1)
	next=None
	if pagination.has_next:
		next=url_for('api.get_posts', page=page+1)
	return jsonify({
		'posts': [post.to_json() for post in posts],
		'prev': prev,
		'next': next,
		'count': pagination.total
	})


@api.route('/posts/<int:id>')
def get_post(id):
	post=Post.query.get_or_404(id)
	return jsonify(post.to_json())


@api.route('/posts/',methods=['POST'])
@login_required
def new_post():
	post=Post.from_json(request.json)
	post.author=g.current_user
	db.session.add(post)
	db.session.commit()
	return jsonify(post.to_json()),201,{'Location':url_for('api.get_post',id=post.id)}

@api.route('/posts/<int:id>',methods=['PUT'])
@login_required
def edit_post(id):
	post=Post.query.get_or_404(id)
	if g.current_user !=post.author:
		return forbidden('Insufficient permissons')
	post.content=request.json.get('content',post.content)
	db.session.add(post)
	db.session.commit()
	return jsonify(post.to_json())


@api.route('/category/<category>/posts/')
def get_category_posts(category):
	page=request.args.get('page', 1, type=int)
	pagination=Post.query.filter_by(category=category).order_by(Post.create_time.desc()).paginate(page, per_page=10,error_out=False)
	posts=pagination.items
	prev=None
	if pagination.has_prev:
		prev=url_for('api.get_category_posts', id=id, page=page-1)
	next=None
	if pagination.has_next:
		next=url_for('api.get_category_posts', id=id, page=page+1)
	return jsonify({
		'posts': [post.to_json() for post in posts],
		'prev': prev,
		'next': next,
		'count': pagination.total
	})



@api.route('/tags/<int:id>/posts/')
def get_tag_posts(id):
	tag=Tag.query.get_or_404(id)
	page=request.args.get('page', 1, type=int)
	pagination=tag.posts.order_by(Post.create_time.desc()).paginate(page, per_page=10,error_out=False)
	posts=pagination.items
	prev=None
	if pagination.has_prev:
		prev=url_for('api.get_tag_posts', id=id, page=page-1)
	next=None
	if pagination.has_next:
		next=url_for('api.get_tag_posts', id=id, page=page+1)
	return jsonify({
		'tag':url_for('api.get_tag',id=id),
		'posts': [post.to_json() for post in posts],
		'prev': prev,
		'next': next,
		'count': pagination.total
	})




