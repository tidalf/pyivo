from handler import Handler
import types

class PT_STRING8(Handler):
    
    def get_value(self, value):
        if type(value) in (types.TupleType, types.GeneratorType):
            return [repr(item) for item in value]
        return repr(value)
        
        