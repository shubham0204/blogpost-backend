from db_handler import DatabaseHandler
from models import Blog , User
from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn

db_handler = DatabaseHandler()

"""
Project TODO:
1. Add auto table creation
2. Add user authentication
3. Add JWT
4. Add HTTP header caching
6. Return appropriate error codes
"""

@asynccontextmanager
async def lifespan( _ : FastAPI ):
    db_handler.initialize()
    yield
    db_handler.release()

app = FastAPI( title="Blogpost Backend" , lifespan=lifespan )

@app.post( "/blogs/" )
async def insert_blog( blog: Blog ):
    is_inserted = db_handler.insert_blog(blog)
    return { "is_inserted" : is_inserted }

@app.get( "/blogs/{blog_id}" )
async def get_blog_from_id( blog_id: str ):
    blog = db_handler.get_blog_from_id(blog_id)
    return { "blog" : blog }

@app.get( "/blogs" )
async def get_all_blogs():
    blogs = db_handler.get_all_blogs()
    return { "blogs" : blogs }

@app.put( "/blogs/{blog_id}" )
async def update_blog( blog_id , new_blog: Blog ):
    is_updated = db_handler.update_blog(blog_id, new_blog)
    return { "is_updated" : is_updated }

@app.delete( "/blogs/{blog_id}" )
async def delete_blog( blog_id: str ):
    is_deleted = db_handler.delete_blog(blog_id)
    return {"is_deleted": is_deleted}

@app.post( "/users/" )
async def insert_user( user: User ):
    is_inserted = db_handler.insert_user( user )
    return { "is_inserted" : is_inserted }

@app.get( "/users/{user_id}" )
async def get_user_from_id( user_id: str ):
    user = db_handler.get_user_from_id( user_id )
    return { "user" : user }

@app.put( "/users/{user_id}" )
async def update_user( user_id , new_user: User ):
    is_updated = db_handler.update_user( user_id , new_user )
    return { "is_updated" : is_updated }

@app.delete( "/users/{user_id}" )
async def delete_user( user_id: str ):
    is_deleted = db_handler.delete_user( user_id )
    return {"is_deleted": is_deleted}

if __name__ == "__main__":
    uvicorn.run( app, host="0.0.0.0" , port=8080 )



