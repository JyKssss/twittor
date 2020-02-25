from flask import render_template, redirect, url_for, request, abort, current_app, flash
from twittor.forms import LoginForm,RegisterForm,EditProfileForm,TweetForm, PasswdResetRequestForm
from twittor.models import User ,load_user
from twittor.models import Tweet
from  flask_login import  login_user,current_user,logout_user, login_required
from twittor import  db
from twittor.email import send_email
@login_required
def index():
    form = TweetForm()
    if form.validate_on_submit():
        t = Tweet(body=form.tweet.data,author = current_user)
        db.session.add(t)
        db.session.commit()
        return redirect(url_for('index'))
    page_num = int(request.args.get('page') or 1)
    tweets= current_user.own_and_followed_tweets().paginate(page=page_num, per_page=current_app.config['TWEET_PER_PAGE'] ,error_out=False)
    next_url = url_for('index', page =tweets.next_num) if tweets.has_next else None
    prev_url = url_for('index', page =tweets.prev_num) if tweets.has_prev else None
    name ={'username':current_user.username}

    # posts = [
    #     {
    #         'author': {'username':'root'},
    #         'body':"Hi I am a root"
    #     },
    #     {
    #         'author': {'username':'test'},
    #         'body':"Hi I am a tset"
    #     },
    #     {
    #         'author': {'username':'test2'},
    #         'body':"Hi I am a test2"
    #     }
    # ]
    return render_template('index.html', tweets =tweets.items,form =form, next_url =next_url,prev_url =prev_url)

def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # msg = 'username ={}, password={},remember_me={}'.format(
        #     form.username.data,
        #     form.password.data,
        #     form.remember_me.data
        # )
        # print(msg)


        u= User.query.filter_by(username= form.username.data).first()
        if u is None:
            print('Username invalid')
            return  redirect(url_for('login'))
        if u.check_password(form.username.data):
            login_user(u,remember=form.remember_me.data)
            next_page = request.args.get('next')
            if next_page:
                return  redirect(next_page)
            return redirect(url_for('index'))

        else:
            print('Password invalid')
            return redirect(url_for('login'))

    return render_template('login.html',title='Sign in',form = form)

def logout():
    logout_user()
    return redirect(url_for('login'))

def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username= form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('register2.html', title= 'Registration',form =form)

@login_required
def user(username):
    u=User().query.filter_by(username=username).first()
    if u is None:
        abort(404)
    # posts = [
    #     {
    #         'author': {'username': 'u.username'},
    #         'body': "Hi I am {}".format(u.username)
    #     },
    #     {
    #         'author': {'username': 'u.username'},
    #         'body': "Hi I am {}".format(u.username)
    #     },
    # ]

    # tweets =Tweet.query.filter_by(author =u)
    page_num = int(request.args.get('page') or 1)
    tweets = u.tweets.order_by(Tweet.create_time.desc()).paginate(
        page=page_num, per_page=current_app.config['TWEET_PER_PAGE'] ,error_out=False)
    next_url = url_for('profile', page=tweets.next_num,username= username) if tweets.has_next else None
    prev_url = url_for('profile', page=tweets.prev_num,username= username) if tweets.has_prev else None
    if request.method =='POST':
        print(request.form.to_dict())
        if request.form['request_button'] =='Follow':
            current_user.follow(u)
            db.session.commit()
        else:
            current_user.unfollow(u)
            db.session.commit()

    return render_template('user.html',title='Profile',user=u,tweets =tweets.items,next_url =next_url,prev_url =prev_url)

def page_not_found(e):
    return render_template('404.html'),404

@login_required
def edit_profile():
    form = EditProfileForm();
    if request.method=='GET':
        form.about_me.data = current_user.about_me
    if form.validate_on_submit():
        current_user.about_me= form.about_me.data
        db.session.commit()
        return redirect(url_for('profile',username = current_user.username))
    return  render_template('edit_profile1.html',form =form)


def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = PasswdResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('You will receive a verify email in your mailbox ')
            token = user.get_jwt()
            url = 'http://127.0.0.1:5000/password_reset/{}'.format(token)
            send_email(
                subject='Reset your password',
                recipients=[user.email],
                text_body=url,
                html_body='<h1>{}</h1>'.format(url)
            )

        else:
            raise
        return redirect(url_for('login'))
    return render_template('password_reset_request.html',form =form)

def password_reset(token):
    if current_user.is_authenticated:
        return  redirect(url_for('index'))
    user =User.verify_jwt(token)
    form = PasswdResetRequestForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('password_reset.html', title = 'Password Reset',form =form)

@login_required
def explore():
    page_num = int(request.args.get('page') or 1)

    tweets = Tweet.query.order_by(Tweet.create_time.desc()).paginate(
        page=page_num, per_page=current_app.config['TWEET_PER_PAGE'], error_out=False)
    next_url = url_for('index', page=tweets.next_num) if tweets.has_next else None
    prev_url = url_for('index', page=tweets.prev_num) if tweets.has_prev else None
    return render_template(
        'explore.html',tweets =tweets.items ,next_url =next_url, prev_url = prev_url
    )