from hayden_functions import api


def login():
    # Lets user log in, or redirects to home page if already logged in.
    from flask import render_template, request, session
    session['TOKEN'] = None
    if request.method == 'POST':
        token = request.form['token']
        session['TOKEN'] = token
        return api.test_status(token)
    else:
        return render_template('login.html', without_header=True)
