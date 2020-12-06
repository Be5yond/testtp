from testtp import Session

def test_stash():
    url = 'http://httpbin.org/get'
    s = Session()
    s.get(url)
    s.stash('headers.Host', 'Host')
    assert s.cache['Host'] == 'httpbin.org'

def test_render():
    url = 'http://httpbin.org/{pa}'
    s = Session()
    s.cache = {'pa': 'post', 'para': '1000', 'dodo': '2000'}
    data = {'replace': '{{ dodo}}'}
    params = {'replace': '{{ para }}'}
    s.post(url, params=params, json=data)
    assert '/post' == s.response.request.path_url.split('?')[0]
    assert '1000' == s.response.request.path_url.split('=')[1]
    assert '{"replace": "2000"}' == s.response.request.body.decode('utf-8') 


test_render()
