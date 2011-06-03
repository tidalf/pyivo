import os
import types

class Loader:
    """
    implements custom and magic load of handlers
    """

    def __init__(self,plugins_dir,except_list, plugin_api_class_name = 'Handler'):
        self.plugins_dir = plugins_dir
        self.__modules = None
        self._except_list = except_list
        self.plugin_api = plugin_api_class_name
        self.__modules = None
        self.__classes = []	
        self.__prepared_for_build = False
        self.__handlers_list = []

    def __load_modules(self):
        if not self.__prepared_for_build:
            self.__modules = [__import__('%s.%s' %(self.plugins_dir,module.replace('.py','')), globals(), locals(), module.replace('.py',''))
                              for module in os.listdir(self.plugins_dir) 
                              if module.endswith('.py') and module not in self._except_list]
        else:
            self.__modules = [__import__('%s.%s' %(self.plugins_dir, item), globals(), locals(), item) for item in self.__handlers_list]

    def __import_classes(self):
        if self.__modules is not None:	
            classes = []
            for module in self.__modules:
                for class_inst in module.__dict__.values(): 
                    if module.__name__ in str(class_inst) and type(class_inst) != types.StringType :
                        if class_inst.__name__ == self.plugin_api:
                            plugin_inst = class_inst
                        else:				
                            classes.append(class_inst)
            self.__classes = [cls.__name__ for cls in classes if issubclass(cls, plugin_inst)]	
            modules_names = [item.__name__ for item in self.__modules]            
            if plugin_inst.__module__ in modules_names: 
                index = modules_names.index(plugin_inst.__module__)
                self.__modules.pop(index)

    def load_handlers(self):
        self.__is_prepared_for_build()
        self.__load_modules()
        self.__import_classes()		
        return [self.__classes, self.__modules]

    def __is_prepared_for_build(self):
        import handlers
        try:
            self.__handlers_list = getattr(handlers, '__all__')
        except AttributeError:
            pass
        else:
            self.__prepared_for_build = True			