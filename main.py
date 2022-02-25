from fastapi import FastAPI
from typing import Optional

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




from schemas import Blog

@app.post("/blog")
def create_item(request : Blog):
    print(request.title)
    return request






# if __name__ == "__main__":
#     Uvicorn.run(app,host="127.0.0.1",port=9000)