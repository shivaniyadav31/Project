from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200))
    bids = db.relationship('Bid', backref='user', lazy=True)

class category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    
class Auction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref='auctions')
    bids = db.relationship('Bid', backref='auction', lazy=True)

class Bid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    auction_id = db.Column(db.Integer, db.ForeignKey('auction.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    amount = db.Column(db.Float)
    bid_time = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/base.html')
def base():
    return render_template('base.html')

@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == '1234':
            session['user'] = 'admin'
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/auctionform', methods=['GET', 'POST'])
def auctionform():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    categories = Category.query.all()

    if request.method == 'POST':
        ...

    return render_template('auctionform.html', categories=categories)


@app.route('/auctions.html')
def auctions():
    return render_template('auctions.html')

@app.route('/bids.html')
def bids():
    return render_template('bids.html')

@app.route('/categories.html')
def categories():
    return render_template('categories.html')

@app.route('/users')
def users():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    all_users = User.query.all()
    return render_template('users.html', users=all_users)



@app.route('/dashboard.html')
def dashboard():
    total_users = User.query.count()
    live_auctions = Auction.query.filter(Auction.end_date > datetime.utcnow()).count()
    return render_template('dashboard.html', total_users=total_users, live_auctions=live_auctions)


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000, debug=True)