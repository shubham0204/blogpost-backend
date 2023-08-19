from typing import List
from models import Blog , User
import mariadb
import os
import time
import random
import string

class DatabaseHandler:

    __sql_scripts_dir = "sql"

    def __init__( self ):
        # TODO: Add connection checking here
        time.sleep( 10 )
        self.connection = mariadb.connect( host="database", user='root', password='root' , database='blogs_database' )
        self.cursor = self.connection.cursor()
        print(f"Database connection established")

    def initialize(self):
        self.__create_tables()

    def insert_blog( self , blog: Blog ) -> bool:
        query = "insert into blogs( id , title , content ) values( '{}' , '{}' , '{}' );".format(
                DatabaseHandler.__generate_uid() , blog.title , blog.content )
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

    def get_blog_from_id(self, blog_id: str) -> Blog:
        self.cursor.execute(
            "select * from blogs where id='{}';".format(
                blog_id
            ) )
        for ( _ , blog_title , blog_content ) in self.cursor:
            return Blog( id=blog_id , title=blog_title , content=blog_content )

    def update_blog(self, blog_id: str, new_blog: Blog) -> bool:
        query = "update blogs set title='{}', content='{}' where id='{}';".format(
            new_blog.title, new_blog.content, blog_id)
        self.cursor.execute(query)
        self.connection.commit()
        return self.cursor.affected_rows > 0

    def delete_blog(self, blog_id: str) -> bool:
        query = "delete from blogs where id='{}';".format( blog_id )
        self.cursor.execute(query)
        self.connection.commit()
        return self.cursor.affected_rows > 0

    def insert_user( self , user: User ) -> bool:
        query = "insert into users( id , name, email_address, password , tagline , join_date ) values( '{}', '{}', '{}' , '{}' , '{}', '{}' );".format(
            DatabaseHandler.__generate_uid(), user.name, user.email_address, user.password, user.tagline, user.join_date)
        self.cursor.execute(query)
        self.connection.commit()
        return self.cursor.affected_rows > 0

    def get_user_from_id(self, user_id: str) -> User:
        self.cursor.execute(
            "select * from users where id='{}';".format(
                user_id
            ) )
        for ( _ , user_name, user_email_address, user_password , user_tagline , user_join_date ) in self.cursor:
            return User( id=user_id , name=user_name , email_address=user_email_address, password=user_password , tagline=user_tagline , join_date=user_join_date )

    def update_user( self , user_id: str , user: User ) -> bool:
        query = "update users set name='{}', tagline='{}' where id='{}';".format(
            user.name, user.tagline, user_id)
        self.cursor.execute(query)
        self.connection.commit()
        return self.cursor.affected_rows > 0

    def delete_user( self , user_id: str ) -> bool:
        query = "delete from users where id='{}';".format( user_id )
        self.cursor.execute(query)
        self.connection.commit()
        return self.cursor.affected_rows > 0

    def release(self):
        self.connection.close()

    def __create_tables( self ):
        for script_path in os.listdir( DatabaseHandler.__sql_scripts_dir ):
            create_tables_script = DatabaseHandler.__read_sql_script( script_path )
            self.cursor.execute( create_tables_script )
            self.connection.commit()
            print( f"Executed { script_path }..." )

    @staticmethod
    def __read_sql_script( script_file_name ) -> str:
        return open(os.path.join(DatabaseHandler.__sql_scripts_dir, script_file_name) , "r" ).read()

    @staticmethod
    def __generate_uid() -> str:
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))


