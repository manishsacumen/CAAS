import requests

from .scorecard_exceptions import InvalidAPIKeyError, ResourceNotFoundError, InvalidJSONError, ServerError


def get_json_from_url(url, headers=None, params=None, proxy=None):
    """Creates json response from url

    :param url: str, url to call
    :param headers: dict, Optional custom headers
    :param params: dict, url parameters
    :param proxy: dict
    :return: object, json data from api mapped to equivalent python objects
    """
    headers = headers or {}
    params = params or {}

    try:
        if proxy:
            req = requests.get(url, headers=headers, params=params, proxies=proxy)
        else:
            req = requests.get(url, headers=headers, params=params)
    except Exception as e:
        raise Exception("Error in connecting to {}\nProxy: {}.\n{}".format(url, proxy, str(e)))

    try:
        rv = req.json()
    except ValueError:
        raise InvalidJSONError("URL: {}\nheaders: {}\nparams: {}\nstatus code: {}\nContent: {}".format(
            url,
            headers,
            params,
            req.status_code,
            req.content
        ))

    if req.status_code == 401:
        raise InvalidAPIKeyError("URL: {}\nheaders: {}\nparams: {}\nstatus code: {}\nContent: {}".format(
            url,
            headers,
            params,
            req.status_code,
            req.content
        ))

    if req.status_code == 404:
        raise ResourceNotFoundError("URL: {}\nheaders: {}\nparams: {}\nstatus code: {}\nContent: {}".format(
            url,
            headers,
            params,
            req.status_code,
            req.content
        ))

    if req.status_code == 502:
        raise ServerError("URL: {}\nheaders: {}\nparams: {}\nstatus code: {}\nContent: {}".format(
            url,
            headers,
            params,
            req.status_code,
            req.content
        ))

    if req.status_code != 200:
        raise requests.RequestException("URL: {} Received status {} with content {}.\n Headers {}, Params {}".format(
            url, req.status_code, req.content, headers, params))
    return rv


def connect_to_ss(url, token, params=None, proxy=None):
    """Connect to ss api and returns json data

    :param url: str
    :param token: str
    :param params: dict, url parameters
    :param proxy: dict
    :return: json
    """
    headers = {
        'authorization': 'Token {}'.format(token),
        'X-SSC-Application-Name': 'Splunk',
        'X-SSC-Application-Version': '1.5',
    }
    rv = get_json_from_url(url, headers, params, proxy)
    return rv


def get_value_from_dict_list(iterable, key, value):
    """Checks the key exists and matches with the value in a iterable of dicts,
    and returns it if present

    :param iterable:
    :param key: str, Key to check
    :param value: str, value to check
    :return: dict if present else None
    """
    for item in iterable:
        if key in item.keys() and item[key] == value:
            return item

    return None



def format_portfolio_ids(portfolio_ids):
    try:
        # Python 2.7
        is_string = isinstance(portfolio_ids, unicode)
    except NameError:
        # Python 3
        is_string = isinstance(portfolio_ids, str)

    if is_string and portfolio_ids.strip().strip(',').lower() == 'all':
        portfolio_ids = 'all'
    elif is_string:
        portfolio_ids = portfolio_ids.strip().strip(',')
        portfolio_ids = portfolio_ids.split(',') if portfolio_ids else None

    return portfolio_ids



