# Standard library imports...
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

# Third-party imports...
import requests

# Local imports...
from constants import BASE_URL

def get_response(call, parameters, headers, method):
    request_url = urljoin(BASE_URL, call)

    if(method == 'get'):
        response = requests.get(request_url, params=parameters, headers=headers)
    elif(method == 'post'):
        response = requests.post(request_url, params=parameters, headers=headers)
    elif(method == 'put'):
        response = requests.put(request_url, params=parameters, headers=headers)
    elif(method == 'delete'):
        response = requests.delete(request_url, params=parameters, headers=headers)

    if (response.status_code == 200):
        return response
    else:
        return None