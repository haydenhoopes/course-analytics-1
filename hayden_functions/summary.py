import requests
BASE_PARAMS = {'per_page': '50'}
CANVAS_DOMAIN = "usu.instructure.com"
endpoint = '/api/v1/accounts/%s/courses'
BASE_PARAMS['include[]'] = ['syllabus_body']
BASE_DOMAIN = "https://%s" % CANVAS_DOMAIN
URI = BASE_DOMAIN + (endpoint % id)


def departmentSummary(token, id='15', term=None):
    # parameters should be entered as type str
    departmentData = get_all_data(token, id, term)
    stats = {}

    stats['stats'] = {}

# Make a bunch of variables to count the default view types
    has_syllabus_count = 0
    default_view_count__FEED = 0
    default_view_count__MODULES = 0
    default_view_count__WIKI = 0
    default_view_count__SYLLABUS = 0
    default_view_count__ASSIGNMENTS = 0
    total_courses = 0
    published_course_and_has_syllabus = 0


# Count each of the course types for each course
    for course in departmentData:
        if course['syllabus_body'] is not None:
            has_syllabus_count += 1
        if course['default_view'] == 'feed':
            default_view_count__FEED += 1
        elif course['default_view'] == 'modules':
            default_view_count__MODULES += 1
        elif course['default_view'] == 'syllabus':
            default_view_count__SYLLABUS += 1
        elif course['default_view'] == 'wiki':
            default_view_count__WIKI += 1
        elif course['default_view'] == 'assignments':
            default_view_count__ASSIGNMENTS += 1
        total_courses += 1

        if course['workflow_state'] == 'available' and course['syllabus_body']:
            published_course_and_has_syllabus += 1

# Add the count of each type to a dictionary as a value (the key is a string of type)
        stats['stats']['has_syllabus'] = str(has_syllabus_count)
        stats['stats']['feed'] = str(default_view_count__FEED)
        stats['stats']['modules'] = str(default_view_count__MODULES)
        stats['stats']['syllabus'] = str(default_view_count__SYLLABUS)
        stats['stats']['wiki'] = str(default_view_count__WIKI)
        stats['stats']['assignments'] = str(default_view_count__ASSIGNMENTS)
        stats['stats']['total'] = str(total_courses)
        stats['stats']['published_course_and_has_syllabus'] = str(published_course_and_has_syllabus)

    if total_courses == 0:
        stats['stats'] = None

    return stats



def get_all_data(token, id, term):
    URI = BASE_DOMAIN + (endpoint % id)
    rh = {"Authorization": "Bearer %s" % token}

    if term:
        BASE_PARAMS['enrollment_term_id'] = term
    else:
        BASE_PARAMS['enrollment_term_id'] = None

    desiredItems = int(BASE_PARAMS['per_page'])
    json_data = []
    more_pages = True
    while more_pages:
        data = requests.get(URI, headers=rh, params=BASE_PARAMS)
        json_data_page = data.json()
        if len(json_data_page) >= desiredItems:
            if 'next' in data.links:
                URI = data.links['next']['url']
            else:
                more_pages = False
        else:
            more_pages = False
        for i in json_data_page:
            json_data.append(i)
    return json_data
