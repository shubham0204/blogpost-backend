import time
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from database import BlogOps, UserOps
from database import create_db_connection, init_db, release_db_connection
from models import Blog, User

time.sleep( 5 )
db_connection = create_db_connection()
blog_ops = BlogOps( db_connection )
user_ops = UserOps( db_connection )

"""
Project TODO:
1. Add JWT
2. Add HTTP header caching
3. Return appropriate error codes
"""

@asynccontextmanager
async def lifespan( _ : FastAPI ):
    init_db( db_connection )
    yield
    release_db_connection( db_connection )

app = FastAPI( title="Blogpost Backend" , lifespan=lifespan )

@app.post( "/blogs/" )
async def insert_blog( blog: Blog ):
    is_inserted = blog_ops.insert_blog(blog)
    return { "is_inserted" : is_inserted }

@app.get( "/blogs/{blog_id}" )
async def get_blog_from_id( blog_id: str ):
    blog = blog_ops.get_blog_from_id(blog_id)
    return { "blog" : blog }

@app.get( "/blogs" )
async def get_all_blogs():
    blogs = blog_ops.get_all_blogs()
    return { "blogs" : blogs }

@app.put( "/blogs/{blog_id}" )
async def update_blog( blog_id , new_blog: Blog ):
    is_updated = blog_ops.update_blog(blog_id, new_blog)
    return { "is_updated" : is_updated }

@app.delete( "/blogs/{blog_id}" )
async def delete_blog( blog_id: str ):
    is_deleted = blog_ops.delete_blog(blog_id)
    return {"is_deleted": is_deleted}

@app.post( "/users/" )
async def insert_user( user: User ):
    is_inserted = user_ops.insert_user( user )
    return { "is_inserted" : is_inserted }

@app.get( "/users/{user_id}" )
async def get_user_from_id( user_id: str ):
    user = user_ops.get_user_from_id( user_id )
    return { "user" : user }

@app.put( "/users/{user_id}" )
async def update_user( user_id , new_user: User ):
    is_updated = user_ops.update_user( user_id , new_user )
    return { "is_updated" : is_updated }

@app.delete( "/users/{user_id}" )
async def delete_user( user_id: str ):
    is_deleted = user_ops.delete_user( user_id )
    return {"is_deleted": is_deleted}

if __name__ == "__main__":
    uvicorn.run( app, host="0.0.0.0" , port=8080 )



