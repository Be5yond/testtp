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

def test_render_func_with_args():
    def deco_func(a, b):
        def func(x):
            return a < x < b
        return func
    s = Session()
    s.register_render(deco_func)
    body={'data': 'testdata', 'token': 3}
    s.post('http://httpbin.org/post', json=body)
    scm = {'json': {'token': "{% deco_func(1, 5) %}"}}
    s.validate(schema=scm)