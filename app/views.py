# -*- coding: utf-8 -*-

import os
from flask import render_template, flash, redirect, request, url_for, Response, abort
from app import app
from werkzeug import secure_filename
from wtforms import Form, TextField, widgets, validators, StringField, SubmitField, SelectMultipleField
from datetime import datetime as dt
from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sitedata.db'
db = SQLAlchemy(app)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

login_manager = LoginManager()
login_manager.init_app(app)


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), index=False, unique=True)
    webpage = db.Column(db.String(40), index=False, unique=True)
    statu = db.Column(db.String(10), index=True, unique=False)
    growth = db.Column(db.String(10), index=True, unique=False)
    revenue = db.Column(db.String(10), index=True, unique=False)
    industry = db.Column(db.String(40), index=True, unique=False)
    launched = db.Column(db.String(10), index=False, unique=False)
    employees = db.Column(db.String(10), index=False, unique=False)
    introduction = db.Column(db.String(1200), index=False, unique=True)
    creator = db.Column(db.String(10), index=False, unique=False)
    date = db.Column(db.String(20), index=False, unique=False)

    def __init__(self, name, webpage, statu, growth, revenue, industry, launched, employees, introduction, creator, date):
      self.name = name
      self.webpage = webpage
      self.statu = statu
      self.growth = growth
      self.revenue = revenue
      self.industry = industry
      self.launched = launched
      self.employees = employees
      self.introduction = introduction
      self.creator = creator
      self.date = date
     
    def __repr__(self):
      return '<Product %r>' % self.name

class Resource(db.Model):
    __tablename__ = 'resource'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(40), index=True, unique=False)
    note = db.Column(db.String(40), index=False, unique=False)
    link = db.Column(db.String(40), index=False, unique=True)
    rtype = db.Column(db.String(4), index=False, unique=False)
    creator = db.Column(db.String(10), index=False, unique=False)
    date = db.Column(db.String(20), index=False, unique=False)

    def __init__(self, product_name, note, link, rtype, creator, date):
      self.product_name = product_name
      self.note = note
      self.link = link
      self.rtype = rtype
      self.creator = creator
      self.date = date
    def __repr__(self):
      return '<Resource %r>' % self.link

class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(40), index=True, unique=False)
    review = db.Column(db.String(1200), index=False, unique=False)
    creator = db.Column(db.String(10), index=False, unique=False)
    date = db.Column(db.String(20), index=False, unique=False)

    def __init__(self, product_name, review, creator, date):
      id = db.Column(db.Integer, primary_key=True)
      self.product_name = product_name
      self.review = review
      self.creator = creator
      self.date = date

    def __repr__(self):
      return self.review

class Source(db.Model):
    __tablename__ = 'source'
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String(80), index=False, unique=False)
    link = db.Column(db.String(40), index=False, unique=True)
    creator = db.Column(db.String(10), index=False, unique=False)
    date = db.Column(db.String(20), index=False, unique=False)

    def __init__(self, note, link, creator, date):
      id = db.Column(db.Integer, primary_key=True)
      self.note = note
      self.link = link
      self.creator = creator
      self.date = date

    def __repr__(self):
      return '<Source %r>' % self.link

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), index=True, unique=False)
    role = db.Column(db.String(10), index=True, unique=False)
    email = db.Column(db.String(40), index=True, unique=True)
    company = db.Column(db.String(40), index=True, unique=False)
    password = db.Column(db.String(20), index=False, unique=False)
    date = db.Column(db.String(20), index=False, unique=False)

    def __init__(self, name, role, email, company, password, date):
      id = db.Column(db.Integer, primary_key=True)
      self.name = name
      self.role = role
      self.email = email
      self.company = company
      self.password = password
      self.date = date

    @property
    def is_authenticated(self):
      return True

    @property
    def is_active(self):
      return True

    @property
    def is_anonymous(self):
      return False

    def get_id(self):
      try:
        return unicode(self.id)  # python 2
      except NameError:
        return str(self.id)  # python 3

    def get(self):
      try:
        return unicode(self.id)  # python 2
      except NameError:
        return str(self.id)  # python 3

    def has_role(self, role):
      if self.role == role:
	return True
      else:
        return False

    def __repr__(self):
      return '<User %r>' % (self.email)

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class UserForm(Form):
    name     = TextField('name', [validators.Length(min=2, max=20)])
    role     = TextField('role', [validators.Length(min=3, max=10)])
    email     = TextField('email', [validators.Length(min=4, max=40)])
    company     = TextField('company', [validators.Length(min=2, max=30)])
    password     = TextField('password', [validators.Length(min=3, max=20)])

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
  s = Resource.query.filter_by(product_name = request.args['name']).all()
  r = Review.query.filter_by(product_name = request.args['name']).all()
  return render_template('show_product.html', product = Product.query.filter_by(name = request.args['name']).first(), resources = s, reviews = r)

@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
  return render_template('add_product.html')

@app.route('/add_up', methods = ['GET', 'POST'])
@login_required
def add_up():
  if request.method == 'POST':
    if not request.form['name'] or not request.form['webpage'] or not request.form['growth']:
      flash('Please enter all the fields', 'error')
    else:
      webpage = request.form['webpage']
      if webpage.find("http://") != 0 and webpage.find("https://") != 0:
        webpage = "http://" + webpage
      product = Product(request.form['name'], webpage, 'New', request.form['growth'], request.form['revenue'],request.form['industry'],request.form['launched'],request.form['employees'],request.form['introduction'], current_user.name, dt.now().strftime('%Y/%m/%d'))
      db.session.add(product)
      db.session.commit()
      return redirect(url_for('show_list'))
  return

@app.route('/show_list', methods=['GET', 'POST'])
@login_required
def show_list():
  return render_template('show_list.html', products = Product.query.all() )

@app.route('/show_product', methods=['GET', 'POST'])
@login_required
def show_product():
  s = Resource.query.filter_by(product_name = request.args['name']).all()
  r = Review.query.filter_by(product_name = request.args['name']).all()
  return render_template('show_product.html', product = Product.query.filter_by(name = request.args['name']).first(), resources = s, reviews = r)

@app.route('/add_link', methods=['GET', 'POST'])
@login_required
def add_link():
  webpage = request.form['link']
  if webpage.find("http://") != 0 and webpage.find("https://") != 0:
    webpage = "http://" + webpage

  resource = Resource(request.args['name'], request.form['note'], webpage, 'link', current_user.name, dt.now().strftime('%Y/%m/%d'))
  db.session.add(resource)
  db.session.commit()
  s = Resource.query.filter_by(product_name = request.args['name']).all()
  r = Review.query.filter_by(product_name = request.args['name']).all()
  return render_template('show_product.html', product = Product.query.filter_by(name = request.args['name']).first(), resources = s, reviews = r)

@app.route('/add_file', methods=['GET', 'POST'])
@login_required
def add_file():
  f = request.files['file']
  filename = secure_filename(f.filename)
  storename =  '/static/uploads/' + request.args['name'] + filename
  resource = Resource(request.args['name'], request.form['note'], storename, 'file', current_user.name, dt.now().strftime('%Y/%m/%d'))
  db.session.add(resource)
  db.session.commit()
  storename =  request.args['name'] + filename
  f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
  os.rename(app.config['UPLOAD_FOLDER'] + '/' + filename, app.config['UPLOAD_FOLDER'] + '/' + storename)
  s = Resource.query.filter_by(product_name = request.args['name']).all()
  r = Review.query.filter_by(product_name = request.args['name']).all()
  return render_template('show_product.html', product = Product.query.filter_by(name = request.args['name']).first(), resources = s, reviews = r)

@app.route('/add_review', methods=['GET', 'POST'])
@login_required
def add_review():
  review = Review(request.args['name'], request.form['review'], current_user.name, dt.now().strftime('%Y/%m/%d'))
  db.session.add(review)
  db.session.commit()
  s = Resource.query.filter_by(product_name = request.args['name']).all()
  r = Review.query.filter_by(product_name = request.args['name']).all()
  return render_template('show_product.html', product = Product.query.filter_by(name = request.args['name']).first(), resources = s, reviews = r)

@app.route("/user_management", methods=['GET', 'POST'])
@login_required
def user_management():
  form = UserForm(request.form)
  if request.method == 'POST':
    name=request.form['name']
    if form.validate():
      user = User(request.form['name'], request.form['role'], request.form['email'], request.form['company'],request.form['password'], dt.now().strftime('%Y/%m/%d'))
      db.session.add(user)
      db.session.commit()
      return redirect(url_for('user_management', users = User.query.all()))
    else:
      flash('All the form fields are required. ')
  return render_template('user_management.html', form=form, users = User.query.all())

@app.route("/remove_user", methods=['GET', 'POST'])
@login_required
def user_remove():
  form = UserForm(request.form)
  if request.method == 'POST':
    remove_names = request.form.getlist('user_list')
    for name in remove_names:
      remove_name = User.query.filter_by(email=name).first()
      db.session.delete(remove_name)
      db.session.commit()
  return render_template('user_management.html', form=form, users = User.query.all())

@app.route('/add_source', methods=['GET', 'POST'])
@login_required
def add_source():
  return render_template('add_source.html', sources = Source.query.all())

@app.route('/add_up_source', methods=['GET', 'POST'])
@login_required
def add_up_source():
  source = Source(request.form['note'], request.form['link'], current_user.name, dt.now().strftime('%Y/%m/%d'))
  db.session.add(source)
  db.session.commit()
  return render_template('add_source.html', sources = Source.query.all())

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']        
	user = User.query.filter_by(name = username).first()
        if user.password == password:
            login_user(user)
            return render_template('show_list.html', products = Product.query.all() )
        else:
            return abort(401)
    else:
        return Response('''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
        ''')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return Response('<p>Logged out</p>')

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
