from flask import jsonify,request,url_for
from . import api
from ..models import Say



@api.route('/says/')
def get_says():
	page=request.args.get('page',1,type=int)
	pagination=Say.query.order_by(Say.create_time.desc()).paginate(page,per_page=10,error_out=False)
	says=pagination.items
	prev=None
	if pagination.has_prev:
		prev=url_for('api.get_says',id=id,page=page-1)
	next=None
	if pagination.has_next:
		next=url_for('api.get_says',id=id,page=page+1)
	return jsonify({
		'says':[say.to_json() for say in says],
		'prev':prev,
		'next':next,
		'count':pagination.total
	})


@api.route('/says/<int:id>')
def get_say(id):
	say=Say.query.get_or_404(id)
	return jsonify(say.to_json())




