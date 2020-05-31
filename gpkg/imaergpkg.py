import sqlite3




class ImaerGpkg(object):

    def __init__(self, filename=None):
        self.filename = filename
        self.connect()
        self.init_db()


    def __del__(self):
        if self.connection:
            self.connection.close()
            print('Connection closed')


    def connect(self):
        try:
            self.connection = sqlite3.connect(self.filename)
            print('Connected')
        except:
            self.connection = None
            print('Cannot connect to file: {}'.format(self.filename))


    def run_query_text(self, sql_text, values=None, commit=True, multi=False):
        print(sql_text)
        cursor = self.connection.cursor()

        if multi:
            cursor.executescript(sql_text)
        else:
            if values is None:
                cursor.execute(sql_text)
            else:
                cursor.execute(sql_text, values)

        if commit:
            self.connection.commit()


    def run_query_file(self, filename, values=None, commit=True, multi=False):
        with open(filename, 'r') as sql_file:
            sql_text = sql_file.read()
        self.run_query_text(sql_text, values=values, commit=commit, multi=multi)


    def init_db(self):
        self.run_query_file('create_tables_gpkg.sql', multi=True)
        self.run_query_file('create_tables_imaer.sql', multi=True)
