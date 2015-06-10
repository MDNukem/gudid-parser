import io
import os
from lxml import etree
from logger import logger

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

	def reqs_present(self):
		""" Checks that all required files are present
		:returns: True if all necessary files are present.  False if files are missing.
		"""
		missing = []
		for fname in self.__class__.schema_requirements:
			if os.path.exists(os.path.join(self.base_path,self.__class__.schema_dir,fname)) == False:
				missing.append(fname)
		
		for fname in self.__class__.data_requirements:
			if os.path.exists(os.path.join(self.base_path,self.__class__.data_dir, fname)) == False:
				missing.append(fname)

		if len(missing) != 0:
			for fname in missing:
				logger.error("Missing file: %s",fname)

			logger.error("--- Cannot continue due to missing files ---")
			return False

		return True

	def validate_xml(self):

		with io.open(os.path.join(self.base_path, self.__class__.schema_dir, self.__class__.base_schema), 'rb') as schema_file:
			schema_doc = etree.parse(schema_file)
			gudid_schema = etree.XMLSchema(schema_doc)

			for data_fname in self.__class__.data_requirements:
				with io.open(os.path.join(self.base_path, self.__class__.schema_dir, data_fname), 'rb') as data_file:
					data_doc = etree.parse(data_file)
					logger.info("Validating %s",data_fname)
					gudid_schema.assertValid(data_doc)
				


