from win32com.client import GetObject

class ADUsers(object):
	
	def __init__(self, container_dn = None):
		if container_dn is not None:
			self.container_dn = container_dn
		else:
			root = GetObject('LDAP://RootDSE')
			domain = root.Get('DefaultNamingContext')
			self.container_dn = 'LDAP://cn=users,' + domain
			
	def get_legacy_exchange_dn(self, user_name):
		dn = self.container_dn.replace('LDAP://', 'LDAP://cn=%s,' %user_name)
		return self._get_ad_container_object(dn).LegacyExchangeDN
							
	def get_legacy_exchange_dns_generator(self):
		for item in self._get_ad_container_object():
			yield item.LegacyExchangeDN
	
	def _get_ad_container_object(self, dn = None):
		if dn is None:
			return GetObject(self.container_dn)
		else:
			return GetObject(dn)
					