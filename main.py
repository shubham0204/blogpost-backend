import time
from contextlib import asynccontextmanager
from typing import Annotated

import uvicorn
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Header

from database import BlogOps, UserOps
from database import create_db_connection, init_db, release_db_connection
from models import Blog, User
from auth import generate_jwt_token
from auth import validate_jwt_token

time.sleep( 5 )
db_connection = create_db_connection()
blog_ops = BlogOps( db_connection )
user_ops = UserOps( db_connection )


"""
- Server optimization
2. Add HTTP header caching
3. Return appropriate error codes
4. Database realtime updates
5. Logging (ELK stack)

- Database optimization
1. Store passwords securely in DB
2. Add indexes

- Documentation
1. Add FastAPI docs
2. Host FastAPI docs on GitHub pages
"""

@asynccontextmanager
async def lifespan( _ : FastAPI ):
    init_db( db_connection )
    yield
    release_db_connection( db_connection )

app = FastAPI( title="Blogpost Backend" , lifespan=lifespan )

@app.post( "/blogs/" )
async def insert_blog(
    token: Annotated[ str , Header() ],
    blog: Blog
):
    if validate_jwt_token( token ):
        is_inserted = blog_ops.insert_blog(blog)
        return { "is_inserted" : is_inserted }
    else:
        return HTTPException( status_code=401 , detail="JWT token not recognized." )

@app.get( "/blogs/{blog_id}" )
async def get_blog_from_id(
    token: Annotated[ str , Header() ],
    blog_id: str
):
    if validate_jwt_token( token ):
        blog = blog_ops.get_blog_from_id(blog_id)
        if blog is None:
            return HTTPException( status_code=404 , detail="Could not find blog associated with blog_id" )
        return { "blog" : blog }
    else:
        return HTTPException(status_code=401, detail="JWT token not recognized.")

@app.get( "/blogs" )
async def get_all_blogs(
    token: Annotated[ str , Header() ]
):
    if validate_jwt_token(token):
        blogs = blog_ops.get_all_blogs()
        return { "blogs" : blogs }
    else:
        return HTTPException(status_code=401, detail="JWT token not recognized.")

@app.put( "/blogs/{blog_id}" )
async def update_blog(
    token: Annotated[ str , Header() ],
    blog_id ,
    new_blog: Blog
):
    if validate_jwt_token(token):
        is_updated = blog_ops.update_blog(blog_id, new_blog)
        return {"is_updated": is_updated}
    else:
        return HTTPException(status_code=401, detail="JWT token not recognized.")


@app.delete( "/blogs/{blog_id}" )
async def delete_blog(
    token: Annotated[ str , Header() ],
    blog_id: str
):
    if validate_jwt_token(token):
        is_deleted = blog_ops.delete_blog(blog_id)
        return {"is_deleted": is_deleted}
    else:
        return HTTPException(status_code=401, detail="JWT token not recognized.")

@app.post( "/users/" )
async def insert_user(
    user: User
):
    is_inserted , user_id = user_ops.insert_user( user )
    jwt_token = generate_jwt_token( user_id )
    return { "is_inserted" : is_inserted , "token": jwt_token , "user_id": user_id }

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



