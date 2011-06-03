import codecs
from common.constants import ReportConstants

class Report(object):

    def __init__(self, file_name):
	self.fp = codecs.open(file_name, encoding = ReportConstants.REPORT_ENCODING, mode = 'w')

    def write(self, row):	
	limit = 1024 * 1024
	while len(row) > 0:
		chunk = row[:limit]
		row = row[limit:]
		self.fp.write(chunk)
	self.fp.write('\n')

    def close(self):
	self.fp.close()