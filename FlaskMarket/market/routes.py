from flask import render_template, redirect, url_for, flash, request
from market import app, db
from .models import Item, User
from .forms import RegisterForm, LoginForm, PurchaseForm, SellForm
from flask_login import login_user,login_required,logout_user,current_user

@app.route("/")
@app.route("/home/")
def index():
    return render_template('home.html')

@app.route("/market", methods=['GET','POST'])
@login_required
def market():
    purchase = PurchaseForm()
    sell = SellForm()
    if request.method == 'POST':
        purchased_item = Item.query.filter_by(name = request.form.get('purchase')).first()
        if purchased_item:
            if current_user.budget >= purchased_item.price:
                purchased_item.owner = current_user.id
                current_user.budget-=purchased_item.price
                db.session.commit()
                flash(f'Congratulation you purchased {purchased_item.name} for {purchased_item.price} $',category='success')
            else:
                flash(f'You dont have enough money for {purchased_item.name}',category='danger')

        sell_item = Item.query.filter_by(name = request.form.get("sell")).first()
        if sell_item:
            sell_item.owner = None
            current_user.budget+=sell_item.price
            flash(f'Congratulation you sold {sell_item.name} for {sell_item.price} $',category='success')
            db.session.commit()

        return redirect(url_for("market"))

    items = Item.query.filter_by(owner=None)
    owned_items = Item.query.filter_by(owner=current_user.id)
    return render_template("market.html", items = items, purchase = purchase, owned_items=owned_items, sell = sell)

@app.route("/register",methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Your Account created succesfully! Now You can login", category='success')
        return redirect(url_for('login'))
    return render_template("register.html",form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash(f"Succes! You are logged in as:{user.username}", category='success')
            return redirect(url_for('market'))

        flash(f"Username or Email is wrong", category='warning')
    return render_template('login.html',form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out", category='info')
    return redirect(url_for('login'))
