from handler import Handler
import types

class PT_SYSTIME(Handler):
    
    def get_value(self, value):
        if type(value) in (types.TupleType, types.GeneratorType):
            return ['%d:%d:%d %d.%d.%d' %(item.hour, item.minute, item.second, item.day, item.month, item.year) for item in value]
        return '%d:%d:%d %d.%d.%d' %(value.hour, value.minute, value.second, value.day, value.month, value.year)
        