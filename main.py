'''
This is the first program that I have ever built. As such, it may not be up to common
programming standards and may be somewhat difficult to understand. Please let me know
if there are any issues.
hayden.hoopes@usu.edu
11/14/2019
'''



# These import statements import a way for the html template to talk to the python
from flask import Flask, url_for, redirect, session, request
from flask_caching import Cache

# This app function is built in standard fashion, is built to run server
config = {
    "DEBUG": True,
    "CACHE_TYPE": "simple",
    "SECRET_KEY": "a4ca581b44b6f549a761f803fa0630c3"
}
app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)


# Below are all of the routes for pages and functions. Normally the functions
# are cached to maintain the data, and the pages are built separately.

@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    from pages import login
    return login.login()


@cache.cached(timeout=9999)
def dropdown_header():
    from pages import dropdown_header
    return dropdown_header.dropdown_header()


@app.route('/_assignments', endpoint='getAssignments')
def getAssignments():
    from pages import assignments
    id = request.args.get('id', 15, type=int)
    return assignments.assignments(id)


@app.route('/courses', methods=['GET', 'POST'])
def courses():
    if not session.get('TOKEN'):
        return redirect(url_for('login'))
    from pages import courses
    # The contents of the following function are cached
    w, x, y, z = dropdown_header()
    return courses.courses(x, y, z, w)


@app.route('/assignments', methods=['GET'])
def assignments():
    if not session.get('TOKEN'):
        return redirect(url_for('login'))
    from pages import assignments
    return assignments.assignments()


@app.route('/error/404', methods=['GET', 'POST'])
def not_found():
    from pages import page_not_found
    return page_not_found.not_found()


@app.route('/error/401', methods=['GET', 'POST'])
def unauthorized():
    from pages import unauthorized
    return unauthorized.unauthorized()


@app.route('/error/400', methods=['GET', 'POST'])
def bad_request():
    from pages import bad_request
    return bad_request.bad_request()


# This function runs the server.... Don't change this!!!
if __name__ == '__main__':
    app.run()
