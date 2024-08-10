from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding='utf-8')
    botKey: str


class Configuration(BaseModel):
    botAnnouncementsChannelId: int = 1178684719144128533
    privateChannelsCategoryId: int = 1190401067813453984
    generalChannelId: int = 1157024450504560651
    serverId: int = 819441557664169994
    myId: int = 829376179706134558
    hammadBaddieId: int = 377823365689245699
    botCommandsChannelId: int = 1157041206572892169
    botTestingChannelId: int = 1167100338914988112
    mainBotChannels: list = [botCommandsChannelId, botTestingChannelId]
    mainAdminIds: list = [myId, hammadBaddieId]


configuration = Configuration()
settings = Settings()
