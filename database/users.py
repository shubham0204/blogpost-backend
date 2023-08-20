import mariadb

from models import User
from .utils import generate_uid


class UserOps:

    def __init__( self ,  connection: mariadb.Connection ):
        self.connection = connection
        self.cursor = self.connection.cursor()

    def insert_user( self , user: User ) -> bool:
        query = "insert into users( id , name, email_address, password , tagline , join_date ) values( '{}', '{}', '{}' , '{}' , '{}', '{}' );".format(
            generate_uid(), user.name, user.email_address, user.password, user.tagline, user.join_date)
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




