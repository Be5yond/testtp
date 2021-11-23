import types
from copy import copy
from itertools import zip_longest
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Data(dict):
    params: dict = field(default_factory=dict)
    data: dict = field(default_factory=dict)
    json: dict = field(default_factory=dict)
    headers: dict = field(default_factory=dict)
    cookies: dict = field(default_factory=dict)

    def __iter__(self):
        return iter([{'params': self.params}, self.data, self.json, self.headers, self.cookies])

    def __dict__(self):
        return {
            'params': self.params,
            'data': self.data,
            'json': self.json,
            'headers': self.headers,
            'cookies': self.cookies
        }


@dataclass
class Step:
    data: Data
    extract: str
    schema: Any


def step(func):
    def _warpper(ins, step):
        ret = func(ins, **step.data)
        ins.validate(json_query=step.extract, schema=step.schema)
        return ret
    return _warpper

class defaultdata:
    """默认数据装饰器，为方法添加默认参数.支持的参数为requests的参数headers，params，json, data等
    使用方法：
        @defaultdata(headers={"X-API-header": "default-API"},
                     json={"api-body": "some_api"})
        def some_api(self, **kwargs):
            ...
    """
    def __init__(self, *args, **kwargs):
        self.temp = kwargs

    def __call__(self, func):
        def _wrapper(*args, **kwargs):
            for k, v in self.temp.items():
                temp = copy(v)
                temp.update(kwargs.get(k, {}))
                kwargs[k] = temp
            return func(*args, **kwargs)
        return _wrapper


def merge(data, schema):
    """ 将data和schema merge成一个dict，展示对应字段的校验规则，及失败信息。

    Args:
        data (dict): 被校验数据
        schema (dict): 校验规则模板
    """
    if data is None:
        return f'>  Not Exist !  <'

    # 校验数据类型,或者函数校验时，展示schema名称，缩写展示target_value
    if isinstance(schema, (type, types.FunctionType, types.MethodType)):
        schema_name = schema.__name__
        if isinstance(data, list):
            data = '[...]'
        elif isinstance(data, dict):
            data = '{...}'
        elif isinstance(data, str):
            data = f'{data[:3]}...'
        return f'<  {data}  > == <  {schema_name}  >'
    # 校验target 为空数组或者空字典时
    elif schema in ([], {}):
        return f'<  {data}  > == <  {schema}  >'
    # 校验数据target 等于schema时
    elif isinstance(data, (int, float, str)):
        return f'<  {data}  > == <  {schema}  >'

    # 嵌套数据递归调用
    elif isinstance(data, dict):
        for k, v in schema.items():
            # key在schema中存在，data中不存在时，将data置为None 调用merge
            data[k] = merge(data.get(k), v)
    elif isinstance(data, list):
        for index, (item, scm) in enumerate(zip_longest(data, schema, fillvalue=schema[-1])):
            # 遍历列表数据，将每一个数据与对应的scm模板合并
            data[index] = merge(item, scm)
    return data
    
