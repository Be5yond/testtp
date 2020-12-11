import json
from copy import deepcopy
import testtp

merge = testtp.utils.merge

DATA = {
    'a': 1,
    'b': 'strgs',
    'c': [{'type': 'a'}, {'type': 'b'}],
    'd': {
        'd1': [1,2,3],
        'd2': 123,
        'd3': {'k': 'v'}
    },
    'e': True
}

def test_schema_equal():
    schema = {
        'a': 1,
        'b': 'strgs',
        'c': [{'type': 'a'}, {'type': 'b'}],
        'd': {
            'd1': [1,2,3],
            'd2': 123,
            'd3': {'k': 'v'}
        },
        'e': True
    }
    ret = merge(deepcopy(DATA), schema)
    print(json.dumps(ret, indent=4))

def test_schema_check_datatype():
    schema = {
        'a': int,
        'b': str,
        'c': list,
        'd': dict
    }
    ret = merge(deepcopy(DATA), schema)
    print(json.dumps(ret, indent=4))

def test_schema_check_part():
    schema = {
        'c': [dict],
        'd': {'d2': int}
    }
    ret = merge(deepcopy(DATA), schema)
    print(json.dumps(ret, indent=4))
    
def test_schema_custom_function():
    def le_100(i):
        return i < 100
    schema = {
        'a': le_100
    }
    ret = merge(deepcopy(DATA), schema)
    print(json.dumps(ret, indent=4))

def test_schema_custom_method():
    class Checker:
        @staticmethod
        def le_100(i):
            return i < 100
    schema = {
        'a': Checker.le_100
    }
    ret = merge(deepcopy(DATA), schema)
    print(json.dumps(ret, indent=4))

def test_schema_addtion_checkpoint():
    schema = {
        'a': ''
    }
    ret = merge(deepcopy(DATA), schema)
    print(json.dumps(ret, indent=4))
# test_schema_custom_method()

