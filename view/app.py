from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql

# Uniquement pour les tests

app = Flask(__name__)

app.static_folder = 'static'
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/')
def index():
    return render_template('auth/layout.html')


@app.route('/auth/login')
def login():
    return render_template('auth/login.html')


@app.route('/auth/signup')
def signup():
    return render_template('auth/signup.html')


@app.route('/auth/forgot_password')
def forgot_password():
    return render_template('auth/forgot_password.html')


app.run()