import types


class defaultdata:
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
        for idx, v in enumerate(data):
            # 遍历列表数据，将schema应用到每一个
            data[idx] = merge(v, schema[0])
    return data
    
