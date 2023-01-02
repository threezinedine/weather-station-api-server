from pydantic import BaseModel


class RegisterOrLoginUserInfo(BaseModel):
    username: str 
    password: str

    class Config:
        orm_mode = True


class RegisterResponseUserInfo(BaseModel):
    userId: int
    username: str 

    class Config:
        orm_mode = True
    
