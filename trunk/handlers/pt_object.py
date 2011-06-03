from handler import Handler
import types

class PT_OBJECT(Handler):
    
    def get_value(self, value):
        if type(value) in (types.TupleType, types.GeneratorType):            
            return [repr(self.mapi.get_hex_from_bin(item)) for item in value]
        return repr(self.mapi.get_hex_from_bin(value))
        