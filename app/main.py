from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel           # title str, content str , category, Bool published
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from .import models
from app.database import engine, get_db  
 

models.Base.metadata.create_all(bind=engine)

app = FastAPI()






class Post(BaseModel):
    title: str
    content: str
    published: bool = True        

while True:
        
    try:
        conn = psycopg2.connect(host='localhost',database='vikas',user='postgres',password='Deep@9852',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull")
        break
    except Exception as error:
        print("connection to database failed")
        print("Error",error)
        time.sleep(2)

    
    
    
    
    
my_posts = [{"title":"title of post 1","content":"content of post 1","id":1},{"title":"favorite foods","content":"i like pizza","id":2}]

def find_post(id):
    for p in my_posts:
        if p["id"]==id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] ==id:
           return i
        
        
# @app.get("/")
# def root():
#     return {"message": "Hello World"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status":"success"}

@app.get("/posts")
def get_posts():
    cursor.execute("""select * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
                   (post.title,post.content, post.published))
    new_post = cursor.fetchone()
    
    conn.commit()
    
    return {"data": new_post}


#through error while executing a latest because of same path parameter given to post/{id}
# @app.get("/post/latest")
# def get_latest_posts():
#     post = my_posts[len(my_posts)-1]
#     return {"detail":post}

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * from posts WHERE id=%s """,(str(id),))
    test_post = cursor.fetchone()
    print(test_post)
    post= find_post(id)
    if not post:
        # response.status_code = status.HTTP_202_ACCEPTED
        # return {'message': f"post with id: {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} was not found")
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    
    cursor.execute("""DELETE FROM posts WHERE id = %s returning *""",(str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    
    cursor.execute("""UPDATE posts SET title =%s, content =%s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, str(id)))
    
    updated_post = cursor.fetchone()
    conn.commit()
    
    
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
        
        
    return {"data": updated_post}
