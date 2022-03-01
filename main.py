from fastapi import FastAPI, Depends, status, Response, HTTPException
from typing import Optional , List

app = FastAPI()



@app.get("/")
def index():
    return {'data':{'name':'sabari'}}

#for similar endpoint , make sure the url without parameter should written first
@app.get("/blog/forum")
def index():# only acccepts int , default is string
    return {'data':'forum'}
#after the normal url , url with parameter written second
@app.get("/blog/{id}")
def index(id:int):#we can define the data type ,only acccepts int , default is string
    return {'data':{'blog':id}}

@app.get("/blog/{id}/comments")#we can pass parameter btn path aslo , fastapi know if the variable in path , its a path parameter and others are query parameter
def index(id:int):
    return {'data':{'comments':f'comments of {id}'}}

#passing filter parameters / qury filter using parameters
#eg getting blogs by  limit 10 and filter published ,   ?limit=10&pub=true

@app.get("/query")
def index(limit=10,pub:bool=True,sort : str | None = None ):# = means default value , we need to add sort which is optional , not compulsary , use the | None = None
    return {'data':f'the  limit is {limit,pub,sort} '}




import schemas
# @app.post("/blog")
# def create_item(request : schemas.Blog):#here blog is the schema which displayed on the doc
#     print(request.title)
#     return request


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


from database import *
from sqlalchemy.orm import Session
import models


#crud operations

# @app.post("/blog",status_code=201)

@app.post("/blog",status_code=status.HTTP_201_CREATED,tags=['Blogs'])
def create_item(request : schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body,user_id = 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog





@app.get('/blogs',response_model=List[schemas.ShowBlog],tags=['Blogs']) #must to use list while returning query set
def all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blogs/{id}",response_model=schemas.ShowBlog,tags=['Blogs']) #response_model is like serilaizer (customize in schema)
def index(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND # insted of using the 2 lines ,
        # return {'message':f'Blog with id {id} not found'}# we can use httpexception
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} not found')
    return blog


@app.delete("/blogs/{id}",status_code=status.HTTP_204_NO_CONTENT,tags=['Blogs'])
def destroy(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} not found')
    blog.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/blogs/{id}",status_code=status.HTTP_202_ACCEPTED,tags=['Blogs'])
def update(id: int, request : schemas.Blog, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} not found')
    blog.update(request.dict())
    db.commit()
    return request




#user part

from passlib.context import CryptContext  #password hashing

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # for password hashing

@app.post("/user",response_model=schemas.User_display,status_code=status.HTTP_201_CREATED,tags=['User'])
def create_user(request : schemas.User, db: Session = Depends(get_db)):
    password = pwd_context.hash(request.password)
    new_user = models.User(name=request.name,email=request.email,password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/user/{id}",response_model=schemas.User_display,tags=['User'])#tag for seperation in swagrdoc
def get_user(id: int, response: Response, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        # response.status_code = status.HTTP_404_NOT_FOUND # insted of using the 2 lines ,
        # return {'message':f'Blog with id {id} not found'}# we can use httpexception
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} not found')
    return user


#log in
@app.post("/login")#,response_model=schemas.User_display,status_code=status.HTTP_201_CREATED,tags=['Login'])
def log_in(request : schemas.Login, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid Username')
    verification = pwd_context.verify(request.password,user.password)
    if not verification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid password')

    return user







# if __name__ == "__main__":
#     Uvicorn.run(app,host="127.0.0.1",port=9000)

#creating database table
from database import *
import schemas
import models
models.Base.metadata.create_all(engine)# fire this line create the database