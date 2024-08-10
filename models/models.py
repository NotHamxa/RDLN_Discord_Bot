from pydantic import BaseModel

class User(BaseModel):
    discord_id: int
    discord_username: str
    discord_time:int
    received_num:int
    wallet:int
    alphaEmail:str
    isStudent:bool

class PrivateVCBaseModel(BaseModel):
    owner_id:int
    people_num:int
    is_upgraded:bool
    people:list
    role_id:str

