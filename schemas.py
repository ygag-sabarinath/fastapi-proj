from pydantic import BaseModel


class Blog(BaseModel):#for simple data
    title: str
    body: str #| None = None
    # published : bool  | None = None
    class Config():
        orm_mode = True




class User(BaseModel):
    name : str
    email : str
    password : str
    class Config():
        orm_mode = True

class User_display(BaseModel):
    name : str
    email : str
    #blogs: list # also gives the details with user id and with blod id , below gives the titel and body
    blogs : list[Blog] = []

    class Config():
        orm_mode = True

class ShowBlog(Blog):#just extending to save code
    creator : User_display

    class Config():#this class also needed for the proper working of orm
        orm_mode = True



class Login(BaseModel):
    username : str
    password : str
    class Config():
        orm_mode = True