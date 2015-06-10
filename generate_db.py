# Parse AccessGUDID xml data into a database

import sys
from dataloader import GUDIDLoader

if '__main__' == __name__:
	loader = GUDIDLoader()
	if loader.reqs_present() == True:
		loader.validate_xml()