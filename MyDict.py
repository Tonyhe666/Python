# !/usr/bin/python
# _*_ coding:utf-8 _*_

class Dict(dict):
    def __init__(self, **kwargs):
        super(Dict, self).__init__(**kwargs)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r'Dict object has not key %s' %key)
        except AttributeError:
            raise AttributeError(r'Dict object has not attrubuts %s' %key)

    def __setattr__(self, key, value):
        self[key] = value

