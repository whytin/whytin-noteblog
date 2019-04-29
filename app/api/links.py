from flask import jsonify,request,url_for
from . import api
from ..models import Link



@api.route('/links/')
def get_links():
	page=request.args.get('page',1,type=int)
	pagination=Link.query.order_by(Link.create_time.desc()).paginate(page,per_page=10,error_out=False)
	links=pagination.items
	prev=None
	if pagination.has_prev:
		prev=url_for('api.get_links',page=page-1)
	next=None
	if pagination.has_next:
		next=url_for('api.get_links',page=page+1)
	return jsonify({
		'links':[link.to_json() for link in links],
		'prev':prev,
		'next':next,
		'count':pagination.total
	})


@api.route('/links/<int:id>')
def get_link(id):
	link=Link.query.get_or_404(id)
	return jsonify(link.to_json())





