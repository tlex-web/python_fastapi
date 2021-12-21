from fastapi import FastAPI, Response, status, HTTPException
from typing import Optional
from fastapi.params import Body
from pydantic import BaseModel

from database import Database


db = Database()
app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: str = 'Y'


@app.get("/")
async def root():
    return {"message": "Hello"}


@app.get("/posts", status_code=status.HTTP_200_OK)
def get_posts():
    posts = db.get_posts()
    return {"status": "success", "data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    new_post = db.create_post(post)
    return {"status": "OK", "data": new_post}


@app.get("/posts/{id}")
async def get_post(id: int):
    post = 56

    if not post:
        raise HTTPException(status_code=404, detail=f"{id} not found")
    return {"status": "OK", "data": post}


@app.put("/posts/{id}")
async def update_post(id: int):
    return {}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    return {}
