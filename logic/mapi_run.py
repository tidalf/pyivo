# -*- coding: utf-8 -*-
from wrap_mapi.ad import ADUsers
from wrap_mapi.msg_store_wrapper import MAPIWrapper, GetPropFromStream
from win32com.mapi import mapi, mapitags, mapiutil as util
from report import Report
from common.constants import ReportConstants, Config
from exclusions import Exclusions
from common.utils import get_default_platform_encoding
from handler_loader import Loader
import types

class MapiRunnerError(Exception):
    pass

class MapiRunner(ReportConstants):
    
    def __init__(self, log, context):
	self.legacy_dns = None
	self.unique_properties = []
	self.log = log
	self.context = context
	classes, instances = Loader(Config.HANDLERS_DIR, ['__init__.py']).load_handlers()		
	self.handlers = [classes]
	insts = []
	for i in range(len(classes)):
	    insts.append(getattr(instances[i], classes[i]))	
	self.handlers.append(insts)
	self.log.debug('handlers: %s' %str(self.handlers))
    
    def open(self):
	"""
	opens mapi connection and etc
	"""
	self.mapi = MAPIWrapper()
	
    def set_users_legacy_dns(self, legacy_dns_generator):
	"""
	sets the generator of legacy dns
	"""
	self.legacy_dns = legacy_dns_generator		    
	
    def process(self):
	"""
	walks mapi properties and get them into use
	"""
	if self.legacy_dns is None:
	    raise MapiRunnerError('no legacy dns are set for users')
	exclusion = Exclusions(self.context)
	for item in self.legacy_dns:
	    if item is not None:	
		if exclusion.check_excluded(item):		    
		    self.log.debug('item excluded: %s' %item)
		else:			    
		    self.log.debug('processing %s' %item)
		    mailbox = item.split('/cn=')		    
		    if len(mailbox) < 3:
			self.log.debug('item doesn\'t look like legacy dn: %s. skipping.' %str(item))
			continue		
		    r = Report(mailbox[2] + '.csv')
		    try:
			root = self.mapi.GetRootFolder(item)			
		    except:
			self.log.debug('root folder is not found for %s. skipping this item.' %item)
			continue	    
		    
		    folder = self.mapi._OpenEntry(root.id)
		    for f in self.mapi._GetSubFolderIter(folder):		    
			sub_folder = self.mapi._OpenEntry(f.id)		    
			mailbox, folder = f.GetFQName()			
			folder_path = 'Mailbox - %s/%s' %(mailbox, folder)
			r.write(folder_path.decode(get_default_platform_encoding()))
			self.collect_properties(sub_folder, r)			
			try:
			    self.log.debug('processing folder: %s/%s' %(mailbox, folder))
			except:
			    try:
				self.log.debug('processing folder: %s/%s' %(mailbox, folder.decode(get_default_platform_encoding())))				
			    except:
				try:
				    self.log.debug('processing folder: %s/%s' %(mailbox, repr(folder)))
				except:
				    pass
				
			count = f.GetItemCount()
			r.write('messages count: %d' %count)

			for msg in f.GetMessageGenerator(False):
			    msg_subject = str(msg.GetSubject())
			    r.write('message subject: %s' %msg_subject.decode(get_default_platform_encoding()))				
				
			    mail = self.mapi._OpenEntry(msg.id, flags = mapi.MAPI_BEST_ACCESS)
			    self.collect_properties(mail, r)			    			    
			    attachments = msg.GetAttachmentGenerator()
			    i = 0
			    for attach in attachments:
				r.write('processing attachment number: %d' %i)
				self.collect_properties(attach, r)
			        i += 1
			    i = 0				
			    for recipient in msg.GetRecipientGenerator():
				r.write('processing recipient number: %d' %i)
				self.collect_recipient_properties(recipient, r, mail)
				i += 1
		    r.close()
		    
    def collect_recipient_properties(self, recipients, report_inst, mapi_obj):
	"""
	collects recipients table properties
	"""
	for recipient in recipients:
	    hex_tag, prop_name, prop_type = self._get_property_name(recipient[0], mapi_obj)
	    value = recipient[1]
	    if prop_type in self.handlers[0]:
		index = self.handlers[0].index(prop_type)
		value = self.handlers[1][index](self.mapi).get_value(value)	
	    else:
		if type(value) in (types.TupleType, types.GeneratorType):
		    value = [item for item in value]
	    report_inst.write('%s, %s, %s, %s' %(hex_tag, prop_name, prop_type, str(value)))		    

    def collect_properties(self, mapi_obj, report_inst):
	"""
	collects properties, creates report
	"""
	properties_list = mapi_obj.GetPropList(0)
	n_props, props = mapi_obj.GetProps(properties_list, 0)
	for tag, value in props:
	    hex_tag, prop_name, prop_type = self._get_property_name(tag, mapi_obj)
		    
	    prop_index = props.index((tag, value))
	    initial_tag = properties_list[prop_index]
	    
	    if initial_tag != tag:		
		try:
		    value = self.mapi.get_prop_from_stream(mapi_obj, initial_tag)
		    hex_tag, prop_name, prop_type = self._get_property_name(initial_tag, mapi_obj)			
		except:
		    pass		
	    if prop_type in self.handlers[0]:
		index = self.handlers[0].index(prop_type)
		value = self.handlers[1][index](self.mapi, mapi_obj, initial_tag).get_value(value)	
	    else:
		if type(value) in (types.TupleType, types.GeneratorType):
		    value = [item for item in value]
	    report_inst.write('%s, %s, %s, %s' %(hex_tag, prop_name, prop_type, str(value)))		    

    def _get_property_name(self, id, mapi_obj):
	hex_tag = hex(id&0xFFFFFFFF).replace('L', '')
	if int(hex_tag, 16) > 0x80000000:
	    hr, tags, array = mapi_obj.GetNamesFromIDs((id,))
	    prop_name = array
	else:
	    prop_name = util.GetPropTagName(id)
	prop_type = util.GetMapiTypeName(mapitags.PROP_TYPE(id))
	return hex_tag, prop_name, prop_type
	    
    def close(self):
	"""
	closes work with mapi
	"""
	self.mapi.Close()