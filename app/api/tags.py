from flask import jsonify,request,url_for
from . import api
from ..models import Post,Tag



@api.route('/tags/')
def get_tags():
	page=request.args.get('page',1,type=int)
	pagination=Tag.query.order_by(Tag.create_time.desc()).paginate(page,per_page=10,error_out=False)
	tags=pagination.items
	prev=None
	if pagination.has_prev:
		prev=url_for('api.get_tags',page=page-1)
	next=None
	if pagination.has_next:
		next=url_for('api.get_tags',page=page+1)
	return jsonify({
		'says':[tag.to_json() for tag in tags],
		'prev':prev,
		'next':next,
		'count':pagination.total
	})


@api.route('/tags/<int:id>')
def get_tag(id):
	tag=Tag.query.get_or_404(id)
	return jsonify(tag.to_json())


@api.route('/posts/<int:id>/tags/')
def get_post_tags(id):
	post=Post.query.get_or_404(id)
	page=request.args.get('page', 1, type=int)
	pagination=post.tags.order_by(Tag.create_time.asc()).paginate(page, per_page=10,error_out=False)
	tags=pagination.items
	prev=None
	if pagination.has_prev:
		prev=url_for('api.get_post_tags', id=id, page=page-1)
	next=None
	if pagination.has_next:
		next=url_for('api.get_post_tags', id=id, page=page+1)
	return jsonify({
		'tags': [tag.to_json() for tag in tags],
		'prev': prev,
		'next': next,
		'count': pagination.total
	})



