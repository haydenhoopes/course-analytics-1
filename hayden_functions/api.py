from flask import session
import requests
BASE_PARAMS = {'per_page': '50'}
CANVAS_DOMAIN = "usu.instructure.com"


def courses(token, id='15', more_pages_URI=None, term=None, deleted=None):
    # parameters should be entered as type str
    rh = {"Authorization": "Bearer %s" % token}
    BASE_PARAMS = {'per_page': '50'}
    per_page = int(BASE_PARAMS['per_page'])
    # If term is used as a parameter, add it to parameters
    if term:
        BASE_PARAMS['enrollment_term_id'] = term

    # If the user only wants to see deleted pages, add to parameters
    if deleted:
        BASE_PARAMS['state[]'] = 'deleted'
    else:
        BASE_PARAMS['state[]'] = 'all'

    if more_pages_URI:
        URI = more_pages_URI
        data = requests.get(URI, headers=rh)
    else:
        endpoint = '/api/v1/accounts/%s/courses'
        BASE_PARAMS['include[]'] = ['teachers', 'total_students', 'term', 'syllabus_body']
        BASE_DOMAIN = "https://%s" % CANVAS_DOMAIN
        URI = BASE_DOMAIN + (endpoint % id)
        data = requests.get(URI, headers=rh, params=BASE_PARAMS)

    json_data = data.json()
    if 'prev' in data.links.keys():
        session['PREVIOUS_PAGE'] = data.links['prev']['url']
        first = False
    else:
        first = True

    # If we the number of courses we get is less than the number that we want, this
    # page is the last page.
    desiredItems = int(BASE_PARAMS['per_page'])
    if len(json_data) >= desiredItems:
        if 'next' in data.links:
            session['NEXT_PAGE'] = data.links['next']['url']
            last = False
        else:
            last = True
    else:
        last = True

    if more_pages_URI or first or last:
        return json_data, more_pages_URI, first, last, per_page
    else:
        if 'errors' in json_data:
            return json_data['errors'][0]['message'], more_pages_URI, first, last, per_page
        else:
            return json_data


def subaccounts(token, id='15', optional_base_params=None):
    # arguments should be entered as type str
    if optional_base_params:
        BASE_PARAMS = optional_base_params
    else:
        pass
    endpoint = '/api/v1/accounts/%s/sub_accounts'
    rh = {"Authorization": "Bearer %s" % token}
    BASE_DOMAIN = "https://%s" % CANVAS_DOMAIN
    URI = BASE_DOMAIN + (endpoint % id)
    data = requests.get(URI, headers=rh, params=BASE_PARAMS).json()
    if 'errors' in data:
        return data['errors'][0]['message']
    else:
        return data

def test_status(token, id='15'):
    from flask import redirect, url_for
    endpoint = '/api/v1/accounts/%s/scopes'
    rh = {"Authorization": "Bearer %s" % token}
    BASE_DOMAIN = "https://%s" % CANVAS_DOMAIN
    endpoint_complete = endpoint % id
    URI = BASE_DOMAIN + endpoint_complete
    data = requests.get(URI, headers=rh, params=BASE_PARAMS)
    # Test to get results of test
    if data.status_code == 400:
        return  redirect(url_for('bad_request'))
    elif data.status_code == 401:
        return redirect(url_for('unauthorized'))
    elif data.status_code == 404:
        return redirect(url_for('not_found'))
    elif data.status_code == 200:
        return redirect(url_for('courses'))
    else:
        return 'Unknown error occurred. <br> Please contact USU Center for Student Analytics at https://ais.usu.edu/analytics/'

def course_enrollments(token, id):
    endpoint = '/api/v1/courses/%s/enrollments'
    rh = {"Authorization": "Bearer %s" % token}
    BASE_DOMAIN = "https://%s" % CANVAS_DOMAIN
    endpoint_complete = endpoint % id
    URI = BASE_DOMAIN + endpoint_complete
    data = requests.get(URI, headers=rh, params=BASE_PARAMS).json()
    if 'errors' in data:
        return data['errors'][0]['message']
    else:
        return data

# def students_enrolled_in_course(token, id):
#     endpoint = '/api/v1/courses/%s/students'
#     rh = {"Authorization": "Bearer %s" % token}
#     BASE_DOMAIN = "https://%s" % CANVAS_DOMAIN
#     endpoint_complete = endpoint % id
#     URI = BASE_DOMAIN + endpoint_complete
#     data = requests.get(URI, headers=rh, params=BASE_PARAMS).json()
#     if 'errors' in data:
#         return data['errors'][0]['message']
#     else:
#         return data

def enrollment_terms(token):
    id = 15
    endpoint = '/api/v1/accounts/%s/terms'
    rh = {"Authorization": "Bearer %s" % token}
    BASE_DOMAIN = "https://%s" % CANVAS_DOMAIN
    endpoint_complete = endpoint % id
    URI = BASE_DOMAIN + endpoint_complete
    data = requests.get(URI, headers=rh, params=BASE_PARAMS).json()
    if 'errors' in data:
        return data['errors'][0]['message']
    else:
        return data


def get_assignments(token, id):
    BASE_PARAMS['per_page'] = '100' # Make loop through
    endpoint = '/api/v1/courses/%s/assignments'
    rh = {"Authorization": "Bearer %s" % token}
    BASE_DOMAIN = "https://%s" % CANVAS_DOMAIN
    endpoint_complete = endpoint % id
    URI = BASE_DOMAIN + endpoint_complete
    data = requests.get(URI, headers=rh, params=BASE_PARAMS).json()
    if 'errors' in data:
        return data['errors'][0]['message']
    else:
        return data
