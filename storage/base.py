class BaseDatabaseWrapper( object ):
	''' An abstract class representing a database connection
	'''

	def __init__(self):
		self.connection = None

	def get_connection_params(self):
		raise NotImplementedError('subclasses of BaseDatabaseWrapper require a get_connection_params() method')

	def get_new_connection(self, conn_params):
		raise NotImplementedError('subclasses of BaseDatabaseWrapper require a get_new_connection() method')

	def connect(self):
		conn_params = self.get_connection_params()
		#Establish a connection
		self.connection = self.get_new_connection(conn_params)

	def commit(self):
		'''
		Commits a transaction
		'''
		if self.connection is not None:
			return self.connection.commit()

	def close(self):
		'''
		Closes a connection
		'''
		if self.connection is not None:
			try:
				self.connection.close()
			finally:
				self.connection = None