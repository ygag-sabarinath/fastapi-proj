from fastapi import FastAPI


app = FastAPI()



@app.get("/")
def index():
    print("haiii")
    return {'data':{'name':'sabari'}}


@app.get("/about")
def index():
    return {'data':{'about':'about the page'}}