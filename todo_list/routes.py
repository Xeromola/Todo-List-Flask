from os import removedirs
import re

from flask_login.utils import login_required
from todo_list import app, db
import todo_list
from todo_list.forms import Registration_Form, LoginForm, Item_Form, Edit_Item_Form
from todo_list.models import User, Todo_Item
from flask import render_template, redirect, flash, url_for
from flask_login import current_user, login_user, logout_user

@app.route('/', methods=['GET', 'POST'])
@login_required
def home_page():
    items = current_user.items.all()
    form = Item_Form()
    edit_form = Edit_Item_Form()
    if form.validate_on_submit():
        item = Todo_Item(todo_item=form.item_title.data, user=current_user)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('home_page'))
    return render_template('home.html', items=items, form=form, edit_form=edit_form)

@app.route('/edit/<item_id>', methods=['POST'])
def edit_item(item_id):
    edit_form = Edit_Item_Form()
    i = current_user.items.filter_by(item_id=item_id).first()
    i.todo_item = edit_form.new_item_title.data
    db.session.add(i)
    db.session.commit()
    return redirect(url_for('home_page'))

@app.route('/delete/<item_id>')
def delete_item(item_id):
    current_user.items.filter_by(item_id=item_id).delete()
    db.session.commit()
    return redirect(url_for('home_page'))

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password')
            return redirect(url_for('login_page'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('home_page'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    return redirect(url_for('login_page'))

@app.route('/register', methods=['GET', 'POST'])
def registration_page():
    form = Registration_Form()
    if form.validate_on_submit():
        user = User(username=form.username.data, email_address=form.email_address.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home_page'))
    return render_template('register.html', form=form)