class Config:
    CONFIG_FILE_NAME = 'config.yaml'
    HANDLERS_DIR = 'handlers'
    
class ExclusionsConfig(Config):
    EXCLUSIONS_BLOCK = 'exclusions'
    EXCLUSIONS_FILE_BLOCK = 'file'
    EXCLUSIONS_REGEXP_BLOCK = 'file'        
    
class ReportConstants:
    UNIQUE_REPORT_NAME = 'unique.csv'
    REPORT_ENCODING = 'utf8'
    
class MAPIConstants:
    pass

class ADConstants:
    pass

class MAPIConstants:
    MAPI_E_NOT_ENOUGH_MEMORY = -2147024882
