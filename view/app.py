from flask import Flask, render_template, request, redirect, url_for, flash

# Uniquement pour les tests

app = Flask(__name__)

app.static_folder = 'static'
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def index():
    return render_template('auth/layout.html')

app.run()