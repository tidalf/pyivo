import chardet
import pywin
from constants import ReportConstants

def get_encoding(string):    
    encoding = chardet.detect(string)['encoding']
    if encoding is None:
        encoding = ReportConstants.REPORT_ENCODING
        
    return encoding

def get_default_platform_encoding():
    return pywin.default_platform_encoding