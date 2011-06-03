from logic.application import MapiCalcApplication
import getopt
import sys
import os

def  usage():
    print """
	Simple exchange statistics collecting tool for default profile.
	Collects info about mailbox folders, mails, attachments, recipients.

	syntax: mapi_calc.[exe|py] [--container <container_dn>]	

	container_dn: distingueshed name of AD container - 
	place where tool looks for all AD users with mailboxes

	default value is 'LDAP:\\CN=Users,DC=test1,DC=local'

	example (stats about maiboxes in Third Storage Group filled by Loadgen, 
	domain - test1.local, machine name - CPU1):
 
	mapi_calc.exe --container "LDAP://OU=Mailbox Database,OU=Third Storage Group,OU=CPU1,OU=Users,OU=LoadGen Objects,DC=test1,DC=local"
	If you're not sure about exact container distingueshed name try to use
	ADSIEdit to detect correct one (just find 'distinguishedName' property)

        To get this help write --help 

	(c) 2011, Moscow, Acronis, alexey.ieshin@acronis.com
    """


def parse_input():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["container=", "help"])
    except getopt.GetoptError, err:
        print 'Error:', str(sys.exc_value)
        usage()
        sys.exit()

    container = None

    for o,a in opts:
        if o in ("--help"):
            usage()
            sys.exit()
        if o in ("--container"):
            container = a

    return container

if __name__ == '__main__':

    container = parse_input()
    try: 
        yivo = MapiCalcApplication(container)
        yivo.run()
    except:
        type,value,trace = sys.exc_info()
        print 'Error:', value
	raise
    
    
	