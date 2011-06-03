import os
import re

class Exclusions():
    def __init__(self, context):
        self.context = context
        
    def check_excluded(self, item):
        pattern = self.context.exclusions.regexp
        if pattern:
            if re.match(pattern, item):
                return True
        file = self.context.exclusions.file
        if file:
            if os.path.exists(file):
                for line in open(file):
		    items = item.lower().split('cn=')			
		    if len(items) < 3:
			return False
                    if line.strip().lower() == items[2]:
                        return True
            return False
                
                