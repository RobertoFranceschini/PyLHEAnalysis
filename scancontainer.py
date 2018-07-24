import json

class ScanContainer(object):
    def __init__(self):
        self.dict={}
    def get(self,d):
        return self.dict[json.dumps(d,sort_keys=True)]
    def set_value(self,d,v):
        self.dict[json.dumps(d,sort_keys=True)]=v
