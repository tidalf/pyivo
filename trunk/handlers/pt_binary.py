from handler import Handler
import types

class PT_BINARY(Handler):
    
    def get_value(self, value):
        if type(value) in (types.TupleType, types.GeneratorType):            
            return [self.mapi.get_hex_from_bin(item) for item in value]
        return self.mapi.get_hex_from_bin(value)
        