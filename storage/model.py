from base import BaseDatabaseWrapper
from lxml import etree
import sqlite3

database_file = 'gudids.sqlite'


class SqliteDatabase (BaseDatabaseWrapper):
    '''
    An abstract class representing a connection to a SQLite database
    '''

    def __init__(self, filename=None):
        super(SqliteDatabase, self).__init__()

        self._connection_params = {
            "database_location": database_file
        }

        self.cursor = None

    def get_connection_params(self):
        return self._connection_params

    def get_new_connection(self):
        if self.connection is not None:
            self.connection.commit()
            self.connection.close()

        self.connection = sqlite3.connect(
            self._connection_params["database_location"])
        self.cursor = self.connection.cursor()

    def _verify_database_schema(self):
        raise NotImplementedError(
            'subclasses of SqliteDatabase require a _verify_database_schema() method')

    def _table_has_cols(self, tablename, col_list):
        ''' col_list must be a list of dictionaries, each one with at least a 'name' key. '''
        reference = set([x['name'] for x in col_list])
        sch_res = self.cursor.execute("pragma table_info('" + tablename + "')")
        current_cols = []
        for s in sch_res:
            current_cols.append({"name": s[1]})
        current = set([x['name'] for x in current_cols])

        return current.issuperset(reference)

    def _create_table(self, tablename, col_list):
        ''' col_list must be a list of dictionaries, each one with at least a 'name' key. '''
        create_str = self._build_table_schema_str(tablename, col_list)
        self.cursor.execute(create_str)

    def _build_table_schema_str(self, tablename, col_list):
        col_names = [x['name'] for x in col_list]
        create_str = "CREATE TABLE {}(".format(
            tablename) + ','.join(col_names) + ")"
        return create_str


class GUDIDModel(SqliteDatabase):

    def __init__(self, header=None, schema_file=None):
        super(GUDIDModel, self).__init__()

        self.header = header
        self.get_new_connection()
        self._verify_database_schema(schema_file)

    def _verify_database_schema(self, schema_file):
        '''
        Does a check of the database schema to ensure that a GUDIDModel can be written to it.
        Top-level children with a 'name' attribute are assigned a table in the schema, while
        each of their children with a 'name' attribute are assigned a column.
        '''
        schema_tree = etree.parse(schema_file)
        schema_root = schema_tree.getroot()

        # The set of tables required in the schema by GudidModel
        table_names = {}

        for child in schema_root:
            if etree.iselement(child):
                if 'name' in child.attrib:
                    table = child.attrib['name'].lower()
                    table_names[table] = []

                    for col_entry in child.findall('.//*[@name]'):
                        table_names[table].append(col_entry.attrib)

        result = self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table';")
        existing_tables = set()
        for res in result:
            existing_tables.add(res[0])

        for table_name in table_names:
            if table_name not in existing_tables:
                self._create_table(table_name, table_names[table_name])
            else:
                if self._table_has_cols(
                        table_name, table_names[table_name]) == False:
                    print(
                        "The current db schema doesn't support writing new objects of type " + str(self.__class__))
                    return False
        return True


class DeviceModel (GUDIDModel):

    def __init__(self, header=None):
        super().__init__(self, header)

    def _verify_database_schema(self, schema_file):
        '''
        Does a check of the database schema to ensure that a DeviceModel and any inherited models can be written
        '''
        pass
