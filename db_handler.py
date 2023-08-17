from typing import List
from models import Blog
import mariadb
import os
import time

class DatabaseHandler:

    __sql_scripts_dir = "sql"

    def __init__( self ):
        # TODO: Add connection checking here
        time.sleep( 10 )
        self.connection = mariadb.connect( host="database", user='root', password='root' , database='blogs_database' )
        self.cursor = self.connection.cursor()

    def initialize(self):
        self.__create_tables()

    def insert_blog( self , blog: Blog ) -> bool:
        query = "insert into blogs( title , content ) values( '{}' , '{}' );".format(
                blog.title , blog.content )
        self.cursor.execute( query )
        self.connection.commit()
        return self.cursor.affected_rows > 0

    def get_all_blogs( self ) -> List[Blog]:
        self.cursor.execute(
            "select * from blogs;"
            )
        blogs = []
        for (blog_id, blog_title, blog_content) in self.cursor:
            blogs.append( Blog( id=blog_id , title=blog_title , content=blog_content ) )
        return blogs

    def get_blog_from_id(self, blog_id: int) -> Blog:
        self.cursor.execute(
            "select * from blogs where id={};".format(
                blog_id
            ) )
        for ( _ , blog_title , blog_content ) in self.cursor:
            return Blog( id=blog_id , title=blog_title , content=blog_content )

    def update_blog(self, blog_id: int, new_blog: Blog) -> bool:
        query = "update blogs set title='{}', content='{}' where id={};".format(
            new_blog.title, new_blog.content, blog_id)
        self.cursor.execute(query)
        self.connection.commit()
        return self.cursor.affected_rows > 0

    def delete_blog(self, blog_id: int) -> bool:
        query = "delete from blogs where id={};".format( blog_id )
        self.cursor.execute(query)
        self.connection.commit()
        return self.cursor.affected_rows > 0

    def release(self):
        self.connection.close()

    def __create_tables( self ):
        create_tables_script = DatabaseHandler.__read_sql_script( "create_tables.sql" )
        self.cursor.execute( create_tables_script )
        self.connection.commit()

    @staticmethod
    def __read_sql_script( script_file_name ) -> str:
        return open(os.path.join(DatabaseHandler.__sql_scripts_dir, script_file_name) , "r" ).read()


