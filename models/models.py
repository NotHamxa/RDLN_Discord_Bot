from pydantic import BaseModel

class User(BaseModel):
    discord_id: int
    discord_username: str
    discord_time:int = 0
    received_num:int = 0
    wallet:int = 0
    alphaEmail:str = ""
    isStudent:bool = False

class PrivateVCBaseModel(BaseModel):
    owner_id:int
    people_num:int
    is_upgraded:bool
    people:list
    role_id:str

