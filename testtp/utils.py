import re
from copy import copy
from .logger import logger


def render(p: dict, cache: dict)->dict:
    """ 渲染数据替换变量和函数

    Args:
        p (dict): 待渲染的数据模板
        cache (dict): 数据变量

    Returns:
        dict: 替换后的文件
    """
    var_matcher = re.compile('^{{\s*([0-9A-Za-z_]+)\s*}}$')
    func_matcher = re.compile('^{%\s*([0-9a-zA-Z()"_.=-]+)\s*%}$')
    if isinstance(p, str) and re.match(var_matcher, p):
        try:
            para = p.strip('{ }')
            return cache.get(para, p)
        except KeyError as e:
            logger.error(e)
            logger.error(cache)
    if isinstance(p, str) and re.match(func_matcher, p):
        try:
            para = p.strip('[{%} ]')
            return eval(para)
        except Exception as e:
            logger.error(e)
    elif isinstance(p, dict):
        for k, v in p.items():

            p[k] = render(v, cache)
    elif isinstance(p, list):
        for i, v in enumerate(p):
            p[i] = render(v, cache)
    return p



class defaultdata:
    def __init__(self, **kwargs):
        self.temp = kwargs

    def __call__(self, func):
        def wrap(*args, **kwargs):
            for k, v in self.temp.items():
                temp = copy(v)
                temp.update(kwargs.get(k, {}))
                kwargs[k] = temp
            return func(*args, **kwargs)
        return wrap