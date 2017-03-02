from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sitedata.db'
db = SQLAlchemy(app)

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
      return '<Review %r>' % self.review

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), index=True, unique=False)
    role = db.Column(db.String(10), index=True, unique=False)
    email = db.Column(db.String(40), index=False, unique=True)
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

    def __repr__(self):
      return '<User %r>' % self.email

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


db.create_all()

#product = Products.query.filter_by(name = 'test1').first()
#print product.name
#product = Product('name', 'webpage', 'New', 'growth', 'revenue', 'industry', 'launched','employees','introduction', 'me', dt.now().strftime('%Y/%m/%d'))
#print product.date
#resource = Resource('product_name', 'note', 'link','rtype', 'creator', 'date')
#user = User('name','email','aptc','email','date')
#review = Review('product_name','review','creator','date')
