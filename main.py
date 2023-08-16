from db_handler import DatabaseHandler
from fastapi import FastAPI
from models import Blog
import uvicorn

handler = DatabaseHandler()
app = FastAPI( title="Blogpost Backend" )

@app.post( "/blogs/" )
async def insert_blog( blog: Blog ):
    is_inserted = handler.insert_blog( blog )
    return { "is_inserted" : is_inserted }

@app.get( "/blogs/{blog_id}" )
async def get_blog_from_id( blog_id: int ):
    blog = handler.get_blog_from_id( blog_id )
    return { "blog" : blog }

@app.get( "/blogs" )
async def get_all_blogs():
    blogs = handler.get_all_blogs()
    return { "blogs" : blogs }

@app.put( "/blogs/{blog_id}" )
async def update_blog( blog_id , new_blog: Blog ):
    is_updated = handler.update_blog( blog_id , new_blog )
    return { "is_updated" : is_updated }

@app.delete( "/blogs/{blog_id}" )
async def delete_blog( blog_id: int ):
    is_deleted = handler.delete_blog( blog_id )
    return {"is_deleted": is_deleted}

if __name__ == "__main__":
    uvicorn.run( app, host="0.0.0.0" , port=8080 )



