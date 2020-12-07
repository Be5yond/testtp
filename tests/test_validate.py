from testtp import Session

def test_validate_response():
    url = 'http://httpbin.org/get'
    s = Session()
    s.get(url)
    s.stash('headers.Host', 'Host')
    scm = {
        "args": {},
        "headers": {
            "Accept": "{% str %}",
            "Accept-Encoding": "{% str %}",
            "Host": "httpbin.org",
            "User-Agent": "{% str %}",
            "X-Amzn-Trace-Id": "{% str %}"
        },
        "origin": "{% str %}",
        "url": "http://httpbin.org/get"
    }
    s.validate(scm)

def test_validate_response_custom_function():
    def is_url(s):
        return s.startswith('http')
    url = 'http://httpbin.org/get'
    s = Session()
    s.register_render(is_url)
    s.get(url)
    scm = {
        "args": {},
        "headers": {
            "Accept": "{% str %}",
            "Accept-Encoding": "{% str %}",
            "Host": "httpbin.org",
            "User-Agent": "{% str %}",
            "X-Amzn-Trace-Id": "{% str %}"
        },
        "origin": "{% str %}",
        "url": "{% is_url %}"
    }
    s.validate(scm)

def test_validate_response_fail():
    url = 'http://httpbin.org/get'
    s = Session()
    s.get(url)
    scm = {
        "ars": {},
        "origin": "{% str %}",
        "url": "http://httpbin.get"
    }
    s.validate(scm)

def test_validate_extract_data():
    data = {
        'data_list': [
            {'type': 'A', 'count': 80},
            {'type': 'B', 'count': 90},
            {'type': 'C', 'count': 70},
            {'type': 'D', 'count': 50},
            ]
        }
    url = 'http://httpbin.org/post'
    s = Session()
    s.post(url, json=data)
    scm = ['A', 'B', 'C', 'D']
    s.validate(schema=scm, json_query='json.data_list[].type')
