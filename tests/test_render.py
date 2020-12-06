from testtp import Session
import time

def test_render_vars():
    s = Session()
    s.cache = {'token_holder': 'real_token'}
    body={'data': 'testdata', 'token': '{{ token_holder }}'}
    s.post('http://httpbin.org/post', json=body)
    s.stash(json_query='headers.Host', key='host')
    body={'context_vars': '{{ host }}'}
    s.post('http://httpbin.org/post', json=body)

def test_render_func():
    def get_timestamp():
        return int(time.time())
    s = Session()
    s.register_render(get_timestamp)
    body={'data': 'testdata', 'token': '{% get_timestamp() %}'}
    s.post('http://httpbin.org/post', json=body)

