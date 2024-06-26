from flask import render_template,flash,redirect,url_for,request,g,current_app
from app import db
from app.auth import bp 
from flask_babel import _,get_locale
from app.auth.forms import LoginForm,RegisterForm,ResetPasswordRequestForm,ResetPasswordForm
from flask_login import current_user,login_user,logout_user,login_required
from app.models import User,Post
from app.auth.email import send_password_reset_email
from urllib.parse import urlparse as url_parse
from datetime import datetime
from guess_language import guess_language
from flask import jsonify
from app.translate import translate


@bp.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid credentials')
            return redirect(url_for('auth.login'))
        login_user(user=user,remember=form.remember_me.data)
        next_page=request.args.get('next')
        if not next_page or url_parse(next_page).netloc!='':
            next_page=url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html',title='Sign in',form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    print(current_user.is_authenticated)
    return redirect(url_for('auth.login'))

@bp.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form=RegisterForm()
    if form.validate_on_submit():
        user=User(username=form.username.data,email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations,you are now a registered user')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',title='Register',form=form)




        


    



    


@bp.route('/reset_password_request',methods=['GET','POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=ResetPasswordRequestForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for further instructions')
        return redirect(url_for('auth.login'))
    return render_template('reset_password_request.html',title='reset password',form=form)

@bp.route('/reset_password/<token>',methods=['GET','POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user=User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form=ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('reset_password.html',form=form)



    