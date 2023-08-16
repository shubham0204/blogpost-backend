from typing import List
from models import Blog
import mariadb

class DatabaseHandler:

    def __init__( self ):
        self.connection = mariadb.connect( host="database", user='root', password='root' , database='blogs_database' )
        self.cursor = self.connection.cursor()

    def insert_blog( self , blog: Blog ) -> bool:
        query = "insert into blog( title , content ) values( '{}' , '{}' );".format(
                blog.title , blog.content )
        self.cursor.execute( query )
        self.connection.commit()
        return self.cursor.affected_rows > 0

    def get_all_blogs( self ) -> List[Blog]:
        self.cursor.execute(
            "select * from blog;"
            )
        blogs = []
        for (blog_id, blog_title, blog_content) in self.cursor:
            blogs.append( Blog( id=blog_id , title=blog_title , content=blog_content ) )
        return blogs

    def get_blog_from_id(self, blog_id: int) -> Blog:
        self.cursor.execute(
            "select * from blog where id={};".format(
                blog_id
            ) )
        for ( _ , blog_title , blog_content ) in self.cursor:
            return Blog( id=blog_id , title=blog_title , content=blog_content )

    def update_blog(self, blog_id: int, new_blog: Blog):
        query = "update blog set title='{}', content='{}' where id={};".format(
            new_blog.title, new_blog.content, blog_id)
        self.cursor.execute(query)
        self.connection.commit()
        return self.cursor.affected_rows > 0

    def delete_blog(self, blog_id: int):
        query = "delete from blog where id={};".format( blog_id )
        self.cursor.execute(query)
        self.connection.commit()
        return self.cursor.affected_rows > 0

    def __del__( self ):
        self.connection.close()
