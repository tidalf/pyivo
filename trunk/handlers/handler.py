import wrap_mapi.msgstore as msgstore
class Handler(object):
    
    def __init__(self, mapi, mapi_obj = None, prop_id = None):
        self.mapi = mapi
        self.mapi_obj = mapi_obj
        self.prop_id = prop_id
        self.msgstore = msgstore
        
    def get_value(self, value):
        pass
    