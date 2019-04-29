# -*- coding:utf-8 -*-
from flask import render_template,redirect,request,url_for,flash
from flask_login import login_user,logout_user,login_required,current_user
from . import auth
from .. import db
from ..models import User
from .forms import LoginForm


@auth.route('/login',methods=['GET','POST'])
def login():
	form=LoginForm()
	if form.validate_on_submit():
		user=User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user)
			return redirect(url_for('main.home'))
		flash(u'账户或密码错误')
	return render_template('auth/login.html',form=form)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash(u'成功退出')
	return redirect(url_for('.login'))


