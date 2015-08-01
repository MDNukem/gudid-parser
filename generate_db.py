# Parse AccessGUDID xml data into a database

import sys
from dataloader import GUDIDLoader

if '__main__' == __name__:
    loader = GUDIDLoader()
    try:
        loader.reqs_present()
        loader.validate_xml()
    finally:
        loader.create_database()
