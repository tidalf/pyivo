from constants import ExclusionsConfig
import types
import yaml
import os

class ContextError(Exception):
    pass

class Context(ExclusionsConfig):
    
    def __init__(self):
        if os.path.exists(ExclusionsConfig.CONFIG_FILE_NAME):
            self.config_data = yaml.load(open(ExclusionsConfig.CONFIG_FILE_NAME))
        else:
            raise ContextError('no conifg file found')
    
    def __getattr__(self, item):  
        value = self.config_data[item]
        if type(value) == types.DictType:
            return type(item, (), value)
        else:
            return value
    
    