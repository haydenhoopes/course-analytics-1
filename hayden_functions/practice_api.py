import requests
from pprint import pprint
def courses(token='1009~YfadrNgczvoB9ZWk2q9isEiCUwEzAXjiZfldkCmVJTmt6bICqc5jMXacV1rDYm1E', id='15'):
    rh = {"Authorization": "Bearer %s" % token}
    BASE_PARAMS = {'per_page': '50'}
    CANVAS_DOMAIN = "usu.instructure.com"
    BASE_DOMAIN = "https://%s" % CANVAS_DOMAIN
    endpoint = '/api/v1/accounts/%s/courses'
    URI = BASE_DOMAIN + (endpoint % id)
    data = requests.get(URI, headers=rh, params=BASE_PARAMS).json()
    return data

