# -*- coding: utf-8 -*-
from mapi_run import MapiRunner
from win32com.mapi import mapi, mapitags, mapiutil as util

class MapiCalc(MapiRunner):
    
    def __init__(self, log, context):
	self.legacy_dns = None
	self.unique_properties = []
	self.log = log
	self.context = context

	self.folders_num = 0
	self.mails_num = 0
	self.attach_num = 0
	self.recip_num = 0
    
    def process(self):
	"""
	walks mapi properties and get them into use
	"""
	if self.legacy_dns is None:
	    raise MapiRunnerError('no legacy dns are set for users')
	for item in self.legacy_dns:
	    if item is not None:	
                self.log.debug('processing %s' %item)
                mailbox = item.split('/cn=')		    
                if len(mailbox) < 3:
                    self.log.debug('item doesn\'t look like legacy dn: %s. skipping.' %str(item))
                    continue		
                try:
                    root = self.mapi.GetRootFolder(item)			
                except:
                    self.log.debug('root folder is not found for %s. skipping this item.' %item)
                    continue	    

                mails = 0
		folders = 0
		attachs = 0
		recips = 0

                folder = self.mapi._OpenEntry(root.id)
                for f in self.mapi._GetSubFolderIter(folder):		    
                    folders += 1			
                    sub_folder = self.mapi._OpenEntry(f.id)		    				

                    mails += f.GetItemCount()
                    for msg in f.GetMessageGenerator(False):
                            
                        mail = self.mapi._OpenEntry(msg.id, flags = mapi.MAPI_BEST_ACCESS)
                        attachments = msg.GetAttachmentGenerator()

                        for attach in attachments:
                            attachs += 1			
                        for recipient in msg.GetRecipientGenerator():
                            recips += 1
		log_line = 'mailbox folders: %d, mails: %d, attachments: %d, recipients: %d' %(folders, 												mails, 
												attachs, 
												recips)
		self.folders_num += folders
		self.mails_num += mails
		self.attach_num += attachs
		self.recip_num += recips

		self.log.debug(log_line)
	self.print_stat()

    def print_stat(self):
	out_line = 'folders: %d, mails: %d, attachments: %d, recipients: %d' %(self.folders_num, 
										self.mails_num, 
										self.attach_num, 
										self.recip_num)
	print (out_line)
		    