# Testtp
http client for testers 

## Supported Features
- - -
- [defaultdata 系统级及接口级的默认参数](#默认参数) 
  - [Session级默认参数](#Session级默认参数)
  - [API级默认参数](#API级别默认参数)
- [render 参数动态渲染（变量或者函数）](#数据动态渲染)
  - [数据变量](#变量缓存---cache)
  - [函数变量](#使用函数实时计算参数---register_render)
- [validate 基于模板的数据校验](#数据校验)
  - [response校验](#校验返回body---validate)
  - [预处理后校验](#数据抽取---json_query)

## Built with
- - -
- [requests](https://github.com/psf/requests)
- [jmespath](https://github.com/jmespath/jmespath.py)
- [schema](https://github.com/keleshev/schema)
- [loguru](https://github.com/Delgan/loguru)

## 默认参数
- - -
### Session级默认参数
Session继承自requests.Session.利用requests.Session实现默认数据。
``` 
from testtp import Session
s = Session()
s.headers['X-request-type'] = 'autotest'
s.params = {'default_params': 'value'}
s.get('http://httpbin.org/get', params={'custom': 'query'}, headers={'X-token': 'loda'}) 

>>> OUTPUT
2020-12-05 19:26:03.677 | SEND     | testtp.Req:_restore_resp:22 - <= request url => 
http://httpbin.org/get?default_params=value&custom=query
2020-12-05 19:26:03.682 | RECV     | testtp.Req:_restore_resp:23 - <= response data => 
{
    "args": {
        "custom": "query",   # 本次请求中的params
        "default_params": "value"    # Session中所有请求的默认params
    },
    "headers": {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Host": "httpbin.org",
        "User-Agent": "python-requests/2.25.0",
        "X-Amzn-Trace-Id": "Root=1-5fcb6e4c-1d48a5716e5a0a1b2328d089",
        "X-Request-Type": "autotest",  # Session中所有请求默认header
        "X-Token": "loda"     # 本次请求中的header
    },
    "origin": "159.138.88.145",
    "url": "http://httpbin.org/get?default_params=value&custom=query"
}
```
### API级别默认参数
使用defaultdata装饰器实现添加接口默认参数
```
class Client(Session):
    def __init__(self, host):
        self.host = host
        super().__init__()

    # 定义api接口，添加默认header和body数据
    @defaultdata(
        headers={"X-API-header": "default-API"},
        json={"default-body-data": "some_api"}
    )
    def some_api(self, **kwargs):
        self.post(self.host+'/post', **kwargs)


c = Client('http://httpbin.org')
c.some_api(json={'real': 'hadogen'})

>>> OUTPUT
2020-12-06 21:44:47.948 | SEND     | testtp.Req:_wrapper:35 - <= request body => 
{
    "default-body-data": "some_api",  # API默认参数
    "real": "hadogen"                 # 本次请求参数
}
2020-12-06 21:44:48.432 | SEND     | testtp.Req:_restore_resp:22 - <= request url => 
http://httpbin.org/post
2020-12-06 21:44:48.438 | RECV     | testtp.Req:_restore_resp:23 - <= response data => 
{
    "args": {},
    "data": "{\"default-body-data\": \"some_api\", \"real\": \"hadogen\"}",
    "files": {},
    "form": {},
    "headers": {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Content-Length": "52",
        "Content-Type": "application/json",
        "Host": "httpbin.org",
        "User-Agent": "python-requests/2.25.0",
        "X-Amzn-Trace-Id": "Root=1-5fcce04f-26e703c65519aff126e74acf",
        "X-Api-Header": "default-API"    #API-默认参数
    },
    "json": {
        "default-body-data": "some_api",  
        "real": "hadogen"                 # 本次请求参数
    },
    "origin": "61.149.134.32",
    "url": "http://httpbin.org/post"
}
```
## 数据动态渲染
- - -
### 变量缓存---cache
“{{ x }}"字符串括起来的数据x被认为是变量，运行时将替换成cache中的对应数据。   

```
s = Session()
s.cache = {'token_holder': 'real_token'}  # 设置缓存数据
body={'data': 'testdata', 'token': '{{ token_holder }}'}
s.post('http://httpbin.org/post', json=body)
>>> OUTPUT
2020-12-06 22:07:40.964 | SEND     | testtp.Req:_wrapper:35 - <= request body => 
{
    "data": "testdata",
    "token": "real_token"  # token被替换成cache中的数据
}
```
### 上下文数据缓存---stash
Session将最近一次请求的response存储。使用stash函数可以从response数据抽取关键的数据，存储到cache，供后面请求使用,
[json_query](https://jmespath.org/)提取规则为jmespath规则
```
s = Session()
s.cache = {'token_holder': 'real_token'}
body={'data': 'testdata', 'token': '{{ token_holder }}'}
s.post('http://httpbin.org/post', json=body)
s.stash(json_query='headers.Host', key='host') # 将返回的content中 'header.Host'字段存到缓存cache中，key为'host'
body={'context_vars': '{{ host }}'}
s.post('http://httpbin.org/post', json=body)
>>> OUTPUT
2020-12-06 22:07:41.644 | SEND xx   | testtp.Req:_wrapper:35 - <= request body => 
{
    "context_vars": "httpbin.org"
xx
```
### 使用函数实时计算参数---register_render
“{% f(x) %}"字符串括起来的数据f(x)被认为是函数，运行时将执行函数来生成数据。   
支持python内置函数例如random.randint()， 也可以用register_render将自定义函数注册给渲染器使用。 
```
def get_timestamp(shift: int):
        return int(time.time()) + shift
s = Session()
s.register_render(get_timestamp) 
body={'data': 'testdata', 'timestamp': '{% get_timestamp(100) %}'}
s.post('http://httpbin.org/post', json=body)

>>> OUTPUT
2020-12-06 22:36:32.784 | SEND     | testtp.Req:_wrapper:35 - <= request body => 
{
    "data": "testdata",
    "timestamp": 1607265492  # 实际参数为get_timestamp函数返回的当前时间戳
}
```
## 数据校验
- - -
### 校验返回body---validate
validate方法对response进行格式校验， scm与请求数据一样会经过render处理，支持变量和函数规则同"{{ x }}", "{% f %}".    
> **注意[schema](https://github.com/keleshev/schema)中的函数只传函数名，执行时会将response对应位置的值作为参数调用f，函数f的返回，应是一个bool值。*
```
def is_url(s):
    return s.startswith('http')
s = Session()
s.get('http://httpbin.org/get')
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

>>> OUTPUT
2020-12-07 14:40:05.689 | SEND     | testtp.Req:_restore_resp:22 - <= request url => 
http://httpbin.org/get
2020-12-07 14:40:05.691 | RECV     | testtp.Req:_restore_resp:23 - <= response data => 
{
    "args": {},
    "headers": {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Host": "httpbin.org",
        "User-Agent": "python-requests/2.25.0",
        "X-Amzn-Trace-Id": "Root=1-5fcdce45-6e7808ba224497484deb1bf1"
    },
    "origin": "223.223.188.146",
    "url": "http://httpbin.org/get"
}
2020-12-07 14:40:05.695 | DEBUG    | testtp.Req:validate:81 - <= schema template => 
{'args': {}, 'headers': {'Accept': <class 'str'>, 'Accept-Encoding': <class 'str'>, 'Host': 'httpbin.org', 'User-Agent': <class 'str'>, 'X-Amzn-Trace-Id': <class 'str'>}, 'origin': <class 
'str'>, 'url': <function test_validate_response_custom_function.<locals>.is_url at 0x000001B478983280>}
```
### 数据抽取---json_query
有些场景下需要对返回数据进行一些预处理（如：抽取关键字段，求和，求最大值等），之后才进行校验，这时需要传入数据处理规则[json_query](https://jmespath.org/),提取规则为jmespath规则
```
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

>>> OUTPUT
2020-12-07 14:38:31.241 | RECV     | testtp.Req:_restore_resp:23 - <= response data => 
{
    "args": {},
    "data": "{\"data_list\": [{\"type\": \"A\", \"count\": 80}, {\"type\": \"B\", \"count\": 80}, {\"type\": \"C\", \"count\": 80}, {\"type\": \"D\", \"count\": 80}]}",
    "files": {},
    "form": {},
    "headers": {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Content-Length": "127",
        "Content-Type": "application/json",
        "Host": "httpbin.org",
        "User-Agent": "python-requests/2.25.0",
        "X-Amzn-Trace-Id": "Root=1-5fcdcde7-332bb4ee193f31915faee06b"
    },
    "json": {
        "data_list": [
            {"count": 80,"type": "A"},
            {"count": 90,"type": "B"},
            {"count": 70,"type": "C"},
            {"count": 50,"type": "D"},
        ]
    },
    "origin": "223.223.188.146",
    "url": "http://httpbin.org/post"
}
2020-12-07 14:38:31.246 | DEBUG    | testtp.Req:validate:73 - <= json query => 
json.data_list[].type
2020-12-07 14:38:31.247 | DEBUG    | testtp.Req:validate:74 - <= extract body => 
['A', 'B', 'C', 'D']
2020-12-07 14:38:31.248 | DEBUG    | testtp.Req:validate:81 - <= schema template => 
['A', 'B', 'C', 'D']
```