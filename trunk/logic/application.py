from wrap_mapi.ad import ADUsers
from mapi_run import MapiRunner
from mapi_calc import MapiCalc
from common.context import Context
from common.logger import Logger
import traceback
import sys
import os

class MapiApplication(object):
	
	def __init__(self, users_container_dn):
		self.users_container_dn = users_container_dn
		self.context = Context()
		self.log = Logger(self.context.logfile.name, self.context.logfile.level)		
		
	def run(self, application):	
		try:			
			app = application(self.log, self.context)
			app.open()
			ad = ADUsers(self.users_container_dn)
			app.set_users_legacy_dns(ad.get_legacy_exchange_dns_generator())
			app.process()
		except KeyboardInterrupt:
			print 'Aborted'
		except:
			print ('Error see details in log')
			type,value,trace = sys.exc_info()
			self.log.warning(type)
			self.log.warning(value)
			self.log.warning(traceback.extract_tb(trace))								

class YivoApplication(MapiApplication):

	def run(self):
		self.log.info('Starting Yivo...')
		super(YivoApplication, self).run(MapiRunner)
		self.log.info('Yivo task completed.')
				
class MapiCalcApplication(MapiApplication):

	def run(self):
		self.log.info('Starting MapiCalc...')
		super(MapiCalcApplication, self).run(MapiCalc)
		self.log.info('MapiCalc task completed.')
				
	