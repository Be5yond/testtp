from functools import wraps
import json as jsonlib
from json.decoder import JSONDecodeError
import jmespath
import pytest
import requests
from schema import Schema, SchemaError

from .logger import logger
from .utils import merge
from . import render


class Session(requests.Session):
    def __init__(self, **kwargs):
        self.response = None
        self.cache = {}
        super().__init__(**kwargs)

    def _restore_resp(self, r, *args, **kwargs):
        self.response = r
        try:
            logger.log('SEND', '<= request url => \n{}'.format(r.request.url))
            logger.log('RECV', '<= response data => \n{}'.format(jsonlib.dumps(r.json(), indent=4, ensure_ascii=False)))
        except JSONDecodeError as e:
            logger.log('RECV', '<= response data => \n{}'.format(r.content))
    
    def _prepare(method):
        @wraps(method)
        def _wrapper(ins, url, **kwargs):
            url = url.format(**ins.cache)
            kwargs = {k: render.render(v, ins.cache) for k, v in kwargs.items()}
            # logger.log('SEND', '<= request url => \n{}'.format(url))
            logger.log('SEND', '<= request params => \n{}'.format(jsonlib.dumps(kwargs.get('params', {}), indent=4, ensure_ascii=False)))
            body = kwargs.get('json') or kwargs.get('data', {})
            logger.log('SEND', '<= request body => \n{}'.format(jsonlib.dumps(body, indent=4, ensure_ascii=False)))
            return method(ins, url, **kwargs)
        return _wrapper

    @_prepare
    def get(self, url, **kwargs):
        return super().get(url, **kwargs, hooks={'response': self._restore_resp})
    
    @_prepare
    def post(self, url, **kwargs):
        return super().post(url, **kwargs, hooks={'response': self._restore_resp})

    @_prepare
    def put(self, url, **kwargs):
        return super().put(url, **kwargs, hooks={'response': self._restore_resp})

    @_prepare
    def delete(self, url, **kwargs):
        return super().delete(url, **kwargs, hooks={'response': self._restore_resp})

    def stash(self, json_query: str, key: str):
        """ 通过json_query取出数据并，缓存数据到cache

        Args:
            json_query (str): jsonpath for target object
            key (str): data key in self.cache 
        """
        self.cache[key] = jmespath.search(json_query, self.response.json())

    def validate(self, schema: dict, json_query: str=None):
        """ 校验返回体的部分字段

        Args:
            scm (dict): 数据校验模板
            json_query (str): 待校验数据的json_query,
        """
        if json_query:
            data = jmespath.search(json_query, self.response.json())
            logger.debug('<= json query => \n{}'.format(json_query))
            logger.debug('<= extract body => \n{}'.format(schema))
        else:
            data = self.response.json()
        schema = render.render(schema, self.cache)
        scm = Schema(schema, ignore_extra_keys=True)

        try:
            scm.validate(data)
        except SchemaError as e:
            logger.error('<= err msg => \n{}'.format(e))
            pytest.fail(msg=str(e), pytrace=False)
        finally:
            scm_log = merge(data, schema)
            scm_log = jsonlib.dumps(scm_log, indent=4, ensure_ascii=False)
            logger.debug('<= schema template => \n{}'.format(scm_log))


    def register_render(self, *args):
        """ 将函数注册到Session，供渲染时使用
        """
        for f in args:
            render.__setattr__(f.__name__, f)


