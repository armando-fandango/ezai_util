import json
import yaml
import copy
import numpy as np

from . import log_util
from .deprecated import deprecated

logger = log_util.get_logger()

def json_or_yaml(filename):
    """
    This function would be obsolete when pyyaml supports yaml 1.2
    With yaml 1.2 pyyaml can also read json files
    :return:
    """
    import re
    from pathlib import Path

    commas = re.compile(r',(?=(?![\"]*[\s\w\?\.\"\!\-\_]*,))(?=(?![^\[]*\]))')
    """
    Find all commas which are standalone 
     - not between quotes - comments, answers
     - not between brackets - lists
    """
    file_path = Path(filename)
    signs = commas.findall(file_path.open('r').read())
    return "json" if len(signs) > 0 else "yaml"

def load_dict_from_json_file(filename):
    dict_obj = json.load(open(filename, 'r'))
    return dict_obj

def load_dict_from_yaml_file(filename):
    dict_obj = yaml.safe_load(open(filename, 'r'))
    return dict_obj

def load_dict_from_json_str(string):
    dict_obj = json.loads(string)
    return dict_obj

class NPJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NPJSONEncoder, self).default(obj)

def save_to_json_file(obj, filename, sort_keys=False, indent=4):
    if not isinstance(obj, dict):
        obj = obj.__dict__
    json.dump(obj, open(filename, 'w'), indent=indent, sort_keys=sort_keys, cls = NPJSONEncoder)

def save_to_yaml_file(obj, filename):
    if not isinstance(obj, dict):
        obj = obj.__dict__
    yaml.dump(obj, open(filename, 'w'))

class ObjDict(dict):
    """
        TODO: Create an init method that converts nested dicts in this object.
    """
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __str__(self):
        return self.json_dumps()

    def json_dumps(self, sort_keys=False, indent=2):
        return json.dumps(self, indent=indent, sort_keys=sort_keys, cls = NPJSONEncoder)

    def save_to_json_file(self, filename, sort_keys=False, indent=2):
        save_to_json_file(self, filename, sort_keys, indent)
        return self

    def save_to_yaml_file(self, filename):
        save_to_yaml_file(self, filename)
        return self

    @staticmethod
    def load_from_file(filename):
        filetype = json_or_yaml(filename)
        if filetype == "json":
            obj=ObjDict.load_from_json_file(filename)
        elif filetype == "yaml":
            obj=ObjDict.load_from_yaml_file(filename)
        return obj

    @staticmethod
    def load_from_json_file(filename):
        obj = ObjDict(load_dict_from_json_file(filename))
        return obj

    @staticmethod
    def load_from_yaml_file(filename):
        obj = ObjDict(load_dict_from_yaml_file(filename))
        return obj

    def deepcopy(self):
        return copy.deepcopy(self)

@deprecated("Use ObjDict")
class DictObj(object):
    '''
    Dictionaries that also work like objects

    Usage:
    1. Create by passing a dictionary or nothing.
    mydict = DictObj(d=a_dict)
    2. If created empty, you can populate using oe of the load methods:
    load_from_dict
    load_from_json_file
    load_from_json_str

    '''

    def __init__(self, d=None):
        if isinstance(d, dict):
            self.__dict__ = d
        # This code is commented out since the str could be a JSON string or file hence use new methods:
        # load_from_json_file or load_from_json_str
        #elif isinstance(d, str):  # d is filename # could be JSON String
        #    self.__dict__ = load_dict_from_json(d)
        else:
            logger.info('Making empty DictObj because parameters passed is not a dict')

    def __getitem__(self, key):
        return self.__dict__[key]

    # Return the value for key if key is in the dictionary, else default.
    # If default is not given, it defaults to None
    def get(self, key, default=None):
        return self.__dict__.get(key,default)

    # If key is in the dictionary, return its value.
    # If key is not in, insert key with a value of default and return default.
    def setdefault(self, key,default=None):
        return self.__dict__.setdefault(key,default)

    def pop(self, key, default=None):
        return self.__dict__.pop(key, default)

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __delitem__(self, key):
        del self.__dict__[key]

    def __contains__(self, key):
        return key in self.__dict__

    def __len__(self):
        return len(self.__dict__)

    def __repr__(self):
        return repr(self.__dict__)

    def __str__(self):
        return self.dumps_json()

    def update(self, obj):
        if isinstance(obj, dict):
            self.__dict__.update(obj)
        else:
            self.__dict__.update(obj.__dict__)
        return self

    def save_to_json_file(self, filename, sort_keys=False, indent=4):
        save_to_json_file(self, filename, sort_keys, indent)
        return self

    def save_to_yaml_file(self, filename):
        save_to_yaml_file(self, filename)
        return self

    def load_from_dict(self, d):
        self.__dict__ = d
        return self

    def load_from_file(self, filename):
        filetype = json_or_yaml(filename)
        if filetype == "json":
            self.load_from_json_file(filename)
        elif filetype == "yaml":
            self.load_from_yaml_file(filename)
        return self

    def load_from_json_file(self, filename):
        self.__dict__ = load_dict_from_json_file(filename)
        return self

    def load_from_yaml_file(self, filename):
        self.__dict__ = load_dict_from_yaml_file(filename)
        return self

    def load_from_json_str(self, string):
        self.__dict__ = load_dict_from_json_str(string)
        return self

    def dumps_json(self, sort_keys=False, indent=4):
        obj = self.__dict__
        return json.dumps(obj, indent=indent, sort_keys=sort_keys, cls = NPJSONEncoder)

    def deepcopy(self):
        return copy.deepcopy(self)

    def values(self):
        return list(self.__dict__.values())

    def keys(self):
        return list(self.__dict__.keys())

