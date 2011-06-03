from msgstore import MAPIMsgStore, GetPropFromStream
from win32com.mapi import mapi, mapitags
import win32com.mapi.exchange as exchange
import win32com.mapi.mapiutil as util
import os
import locale


class MAPIWrapper(MAPIMsgStore):

    def __init__(self, outlook = None):
        self.outlook = outlook
        cwd = os.getcwd()
	
        mapi.MAPIInitialize(None)	
	profiles = AdminProfiles().get_profiles_generator()	
	has_default = False
	for profile in profiles:
	    if profile.is_default:
		has_default = True
		break
	if not has_default:
	    profile.set_default_profile()
        logon_flags = (mapi.MAPI_EXTENDED | mapi.MAPI_USE_DEFAULT| mapi.MAPI_UNICODE)	
        self.session = mapi.MAPILogonEx(0, None, None, logon_flags)
	self.get_prop_from_stream = GetPropFromStream

        locale.setlocale(locale.LC_NUMERIC, "C")
        self.mapi_msg_stores = {}
        self.default_store_bin_eid = None
        os.chdir(cwd)
	self.store = None

    def open_user_store(self, user_name_legacy_dn):

	msg_store = exchange.HrOpenExchangePrivateStore(self.session)
	interface = msg_store.QueryInterface(exchange.IID_IExchangeManageStore)
	srv_dn = exchange.HrGetServerDN(self.session) + '/cn=Microsoft Private MDB'	
	store_id = interface.CreateStoreEntryID(srv_dn, user_name_legacy_dn, 0x9)
	self.store = self.session.OpenMsgStore (0, store_id, None, mapi.MAPI_BEST_ACCESS)        	

    def GetRootFolder(self, user_legacy_dn):
        # if storeID is None, gets the root folder from the default store.
        self.open_user_store(user_legacy_dn)
        hr, data = self.store.GetProps((mapitags.PR_ENTRYID, mapitags.PR_IPM_SUBTREE_ENTRYID), 0)
        store_eid = data[0][1]
        subtree_eid = data[1][1]
        eid = mapi.HexFromBin(store_eid), mapi.HexFromBin(subtree_eid)
        return self.GetFolder(eid)
    
    def get_hex_from_bin(self, value):
	return mapi.HexFromBin(value)

class AdminProfiles(object):
    
    def get_profiles_generator(self):
	profiles = mapi.MAPIAdminProfiles(0)
	rows = mapi.HrQueryAllRows(profiles.GetProfileTable(0),
	                           (mapitags.PR_DEFAULT_PROFILE, mapitags.PR_DISPLAY_NAME_A),
	                           None,
	                           None,
	                           0)	
	for row in rows:	  
	    is_default_profile, profile_name = row[0][1], row[1][1]	    
	    yield Profile(profiles, profile_name, is_default_profile)
	    
	
class Profile:    
    
    def __init__(self, profile, name, is_default):	
	self.name = name
	self.is_default = is_default
	self.profile = profile

    def set_default_profile(self):
	self.profile.SetDefaultProfile(self.name, 0)
	
    def is_default(self):
	return self.is_default