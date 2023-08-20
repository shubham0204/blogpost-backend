import os
import random
import string

import mariadb


def create_db_connection() -> mariadb.Connection:
    return mariadb.connect(host="database", user='root', password='root', database='blogs_database')

def release_db_connection( connection: mariadb.Connection ):
    connection.close()

def init_db( connection: mariadb.Connection ):
    create_tables( connection )

def create_tables( connection: mariadb.Connection ):
    for script_path in os.listdir( "database/sql_scripts" ):
        create_tables_script = read_sql_script( script_path )
        connection.cursor().execute( create_tables_script )
        connection.commit()
        print( f"Executed { script_path }..." )

def generate_uid() -> str:
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))

def read_sql_script( script_file_name ) -> str:
    return open(os.path.join( "database/sql_scripts" , script_file_name) , "r" ).read()