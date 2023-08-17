from db_handler import DatabaseHandler
from models import Blog
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
async def get_blog_from_id( blog_id: int ):
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
async def delete_blog( blog_id: int ):
    is_deleted = db_handler.delete_blog(blog_id)
    return {"is_deleted": is_deleted}

if __name__ == "__main__":
    uvicorn.run( app, host="0.0.0.0" , port=8080 )



