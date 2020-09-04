from flask import render_template, request, session, redirect, url_for


def unauthorized():
    status = 'Unauthorized'
    status_code = '401'

    if request.method == 'POST':
        session['TOKEN'] = None
        return redirect(url_for('login'))

    return render_template('login_error.html', status=status, status_code=status_code)
