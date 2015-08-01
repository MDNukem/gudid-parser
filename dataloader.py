import io
import os
from lxml import etree
from logger import logger
from storage.model import GUDIDModel, DeviceModel

class GUDIDLoader(object):
	schema_requirements = [
		'device.xsd',
		'gudid.xsd',
		'header.xsd'
	]

	schema_dir = 'xml_data'
	base_schema = 'gudid.xsd'

	data_requirements = [
		'FULLDownload_Part1_Of_3_2015-06-01.xml',
		'FULLDownload_Part2_Of_3_2015-06-01.xml',
		'FULLDownload_Part3_Of_3_2015-06-01.xml'
	]

	data_dir = 'xml_data'

	def __init__(self):
		self.base_path = os.getcwd()
		self.reqs_fulfilled = False
		self.reqs_validated = False

	def reqs_present(self):
		""" Checks that all required files are present
		:returns: True if all necessary files are present.  False if files are missing.
		"""
		missing = []
		self.reqs_fulfilled = False
		for fname in self.__class__.schema_requirements:
			if os.path.exists(os.path.join(self.base_path,self.__class__.schema_dir,fname)) == False:
				missing.append(fname)
		
		for fname in self.__class__.data_requirements:
			if os.path.exists(os.path.join(self.base_path,self.__class__.data_dir, fname)) == False:
				missing.append(fname)

		if len(missing) != 0:
			for fname in missing:
				logger.error("Missing file: %s",fname)

			raise IOError("--- Cannot continue due to missing files ---")
			

		self.reqs_fulfilled = True
		return True

	def validate_xml(self):
		assert self.reqs_fulfilled == True, 'Cannot validate XML, the required files are not all present'

		self.reqs_validated = False
		with io.open(os.path.join(self.base_path, self.__class__.schema_dir, self.__class__.base_schema), 'rb') as schema_file:
			schema_doc = etree.parse(schema_file)
			gudid_schema = etree.XMLSchema(schema_doc)

			for data_fname in self.__class__.data_requirements:
				with io.open(os.path.join(self.base_path, self.__class__.schema_dir, data_fname), 'rb') as data_file:
					data_doc = etree.parse(data_file)
					logger.info("Validating %s",data_fname)
					gudid_schema.assertValid(data_doc)

			self.reqs_validated = True
				
	def create_database(self):
		'''
		Creates a database or databases corresponding to the xsd definitions loaded.
		'''
		if self.reqs_fulfilled == False:
			self.reqs_present()

		if self.reqs_validated == False:
			self.validate_xml()

		assert self.reqs_fulfilled == True, 'Cannot create the database, there are missing XML files'
		assert self.reqs_validated == True, 'Cannot create the database, the XML files could not be validated'

		#Create the databases for each model
		gudid_table = GUDIDModel(
			schema_file=os.path.join(self.base_path, self.__class__.schema_dir, self.__class__.base_schema))
		gudid_table.get_new_connection()
		gudid_table.commit()
		gudid_table.close()

