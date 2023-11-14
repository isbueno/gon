from app import app

from flask import Flask, render_template, request, redirect, url_for, session, flash

from .models.User import User
from .models.Carpool import Carpool
from .models.Student import Student
from app.models.Search import Search

from .user.user_routes import current_user

from .forms import SearchNameForm

# Blueprints
from app.user.user_routes import user_blueprint
app.register_blueprint(user_blueprint)

from app.error.error import error_blueprint
app.register_blueprint(error_blueprint)


# HOME PAGE ROUTE
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


# ABOUT PAGE ROUTE
@app.route('/about')
def about():
    return render_template('about.html')

# ABOUT PAGE ROUTE
@app.route('/contact')
def contact():
    return render_template('contact.html')


# SEARCH PAGE ROUTE
@app.route('/search', methods=['GET', 'POST'])
def search():
    user = current_user
    searchNameForm = SearchNameForm()
    search = Search()

    if searchNameForm.validate_on_submit():

        searched = searchNameForm.searchname.data

        if user.tipo == "student":
            users = search.searchName(searched, Carpool)
        if user.tipo == "carpool":
            users = search.searchName(searched, Student)

        return render_template('results.html', searched=searched, users=users)

    return render_template('search.html', searchNameForm=searchNameForm)


@app.route('/results')
def results():
    return render_template('results.html')