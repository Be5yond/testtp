# Testtp
http client for testers 

## Supported Features
- - -
- 系统级及接口级的默认参数。
- 参数动态渲染-（变量或者函数）
- Validate  --- 基于 Schema 模板的数据校验

## 默认参数
- - -
### Session级默认参数，所有请求会默认带该参数，如果若请求时赋值新值则覆盖。
``` 
>>> from testtp import Session
>>> s = Session()
>>> s.headers
{'User-Agent': 'python-requests/2.25.0', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
>>> s.headers['X-request-type'] = 'autotest'
>>> s.params = {'default_params': 'value'}
>>> s.get('http://httpbin.org/get', params={'custom': 'query'}, headers={'X-token': 'loda'}) 
2020-12-05 19:26:02.953 | SEND     | testtp.Req:_wrapper:33 - <= request params => 
{
    "custom": "query"
}
2020-12-05 19:26:02.955 | SEND     | testtp.Req:_wrapper:35 - <= request body => 
{}
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
<Response [200]>
```
### DefaultData --- API级别默认参数
```

```