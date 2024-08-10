from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import string
import random

from models.models import User


class Database():
    def __init__(self, url, database):
        self.uri = url
        self.client = MongoClient(self.uri, server_api=ServerApi('1'))

        self.db = self.client.get_database(database)
        self.discordData = self.db.get_collection("discord")
        self.discordCodes = self.db.get_collection("discordCodes")
        self.privateVcs = self.db.get_collection("discordPrivVcs")
        self.fiverrDb = self.client.get_database("fiverr").get_collection("collection")
        self.timeThreshold = 1
        self.codeLenght = 6

    def getUserData(self, Id, username=None) -> User:
        """
        returns the data of the user.
        Returns a base format with all attributes as 0 if user not found
        :param Id:
        :param username:
        :return: The User class with the users data
        """
        data = self.discordData.find_one({"discord_id": Id})

        if data is None:
            baseUser = User(**{"discord_id": Id, "username": username})
            self.discordData.insert_one(baseUser.model_dump())

            return baseUser
        user = User(**data)
        return user

    def setTime(self, Id, time):
        self.discordData.update_one(
            {"discord_id": Id},
            {"$set": {"discord_time": time}}
        )

    def setCode(self, id):
        data:User = self.getUserData(id)
        x = (data.discord_time // 3600) // self.timeThreshold
        receivable = x - data.received_num
        self.discordData.find_one_and_update({"discord_id": id},
                                             {"$set": {"wallet": data.wallet + receivable,
                                                       "received_num": data.received_num + receivable}})

    def verifyCode(self, code, idk):
        data = self.discordCodes.find_one({"code": code})
        if data == None:
            return None

        return data

    def generateCode(self, id, usedFor, price) -> dict:
        data:User = self.getUserData(id)
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            checkCode = self.discordCodes.find_one({"code": code})
            if checkCode == None:
                self.discordCodes.insert_one({"code": code,
                                              "used": False,
                                              "givenTo": id,
                                              "usedFor": usedFor})

                self.discordData.update_one({"discord_id": id},
                                            {"$set": {"wallet": data.wallet - price}})
                break
        return {"status": True, "code": code}

    def useCode(self, code) -> dict:
        data = self.discordCodes.find_one({"code": code})
        if data == None:
            return {"present": False}
        if data["used"]:
            return {"present": True, "success": False}
        self.discordCodes.update_one({"code": code},
                                     {"$set": {"used": True}})
        return {"present": True, "success": True}

    def TopTen(self):
        data = self.discordData.find().sort({"discord_time": -1})
        records = []
        for d in data:
            records.append(d)
        if len(records) > 10:
            return records[0:10]
        else:
            return records

    def cnvrtTime(self, secs):
        hrs = int((secs // 3600))
        mins = int((secs - (hrs * 3600)) // 60)
        return f'{hrs}hrs {mins}mins'

    def createPrivateVc(self, id, roleName):

        data = {"owner_id": id,
                "people_num": 0,
                "is_upgraded": False,
                "people": [],
                "role_id": roleName}
        self.privateVcs.insert_one(data)


database = Database("mongodb://localhost:27017/", "RDLN")

uwuImg = """
⠀⠀⠀⠀⠀⠀⠀⠀⠻⣽⠀⣿⣿⡟⣼⡀⠜⣯⣟⣳⣟⠀⠀⣿⡀⣼⡳⠀⣇⢸⡿⡽⢃⢃⣿⡿⡘⢐⣻⢿⠀⣿⣳⡏⢸⣷⠃⢀⣾⢡⠇⡸⣸⡏⢠⣿⣿⣿⣷⢸⢢⣿⡸⢠⢘⠻⣽⢸⣿⡏
⠀⠀⠀⠀⠀⢀⡒⡀⠀⠉⠄⢹⣿⢰⣟⣇⢂⠰⣯⢷⢯⡀⠄⢟⠀⣷⡇⢲⠹⠘⠁⠁⠀⠀⠉⠁⠁⠹⣻⣿⠀⢹⣿⠇⣾⠇⢀⡾⢡⢪⢆⢳⣿⠃⡾⣛⣛⡿⠿⢸⢸⣿⣇⠃⢸⣿⣮⠈⣷⠇
⠀⠀⠀⠀⠀⢆⡱⠨⢄⠀⠈⠸⣧⠸⣻⢾⡄⠂⢹⣞⣟⡆⠀⢬⠀⠋⠀⠀⠀⠀⢀⠠⠀⡔⠠⠰⣶⣦⣤⣉⠀⡀⣿⢡⡿⢠⡞⠁⣵⠏⣠⣿⠃⣼⠯⠛⠋⠙⠛⠘⠸⠟⣿⠀⢸⣿⢾⢰⣿⢀
⠀⠀⠀⢠⠘⠤⢒⡉⢦⠀⡄⠀⢻⡄⢫⣟⢷⡘⡀⢹⡞⣷⡀⠸⠈⠀⢀⣤⠐⡂⢌⡘⢡⢈⣱⠂⢿⣿⣿⣿⣤⣧⣄⡜⠡⠋⣠⣾⣟⣰⣿⣯⣾⡇⠀⡀⠠⣀⠀⢀⠀⠈⠛⠇⢽⣿⡇⣼⡏⣸
⠀⠀⢀⠆⠘⢬⡁⡈⢠⡇⠐⡆⠈⢳⡄⠻⣎⠳⣌⠀⠙⣍⣁⠀⠀⠀⣾⣷⠠⣵⡀⢘⡀⣼⢣⠇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠰⠠⢌⡁⢄⢋⡈⣷⣄⠀⠀⠠⣴⢠⡿⢱⣻
⠀⠀⣌⠂⣍⠢⢀⡇⢸⠇⣦⠈⡅⠀⠘⢄⠈⠳⡝⢦⡂⠈⠛⣧⡘⣦⡙⢿⡄⢳⣟⡟⡾⣭⡐⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢰⠈⠆⢰⣊⢦⠅⣿⣿⣇⠀⠀⠁⡾⢁⣿⠍
⠀⡔⢢⠁⡆⠁⡼⡆⢸⡃⣽⠀⠆⣴⡶⢀⠁⠀⠈⠳⣍⠂⡀⠀⠑⠈⠿⣷⣿⣦⣨⣭⣥⣴⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡈⡷⣖⣿⢚⣍⣰⣿⣿⠇⡠⠂⠔⢠⡾⠋⡰
⠰⡈⠦⠑⣠⢯⣝⡃⢸⡇⢀⡘⠠⣿⢸⢻⠛⡖⡀⠤⡈⠛⠒⠤⡀⠑⣶⣌⣙⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣍⡈⢃⣹⣿⣿⣯⣾⠀⠀⠴⠋⠁⡴⠁
⠡⡅⠃⣰⢯⣳⢾⠀⢸⡇⢸⣃⠀⣿⡈⣿⡆⢹⠀⢶⣥⣉⠒⠄⠀⢠⣝⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠠⡔⠀⢌⠊⢀⡀
⠱⢀⡃⣽⢺⡵⣫⠀⠊⡅⢰⣻⠀⠘⢷⣬⡳⣈⡁⢸⡾⣝⡿⡆⣮⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢀⠓⢀⡜⢬⠇⠸⡄
⠁⠼⢐⡃⠿⣜⠷⠀⢂⠅⣤⡟⣆⢄⠀⠙⢿⣮⣕⠸⣽⣫⢷⢁⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⡏⣠⢡⣞⡟⡏⠀⣇⠇
⠀⠀⠌⡐⠀⠀⠀⠈⠂⠆⢸⣳⠈⡌⡴⣄⡀⠙⠿⢠⢿⣵⡏⢸⣽⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢟⣫⣾⣿⣶⣝⡿⣿⣿⣿⣿⣿⣿⣿⡿⣟⣵⣿⣷⡅⢡⣟⡾⡽⠐⢰⣊⢧
⠀⠀⢣⠀⠀⠀⠀⠀⡁⠄⠘⢽⡆⠰⠀⢻⣳⡄⠀⠘⣿⣞⠇⣟⣾⠁⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢟⣯⣾⣿⣿⣿⣿⣿⣿⣿⣶⣔⠙⣿⣿⡿⣫⣾⣿⣿⣿⢿⣿⣦⡙⡾⢡⠃⢦⡙⣮
⠀⠀⢂⠆⠀⠀⠀⠀⢐⠈⠐⡀⠻⣄⠣⠈⢷⣻⡄⠈⣷⡟⢨⣟⣾⠀⡇⠻⣿⣿⣿⣿⣿⣿⡿⢫⣵⣶⣿⣿⣿⣿⣿⣿⢏⣽⣛⠿⣿⣿⡿⠼⣿⠏⣾⣿⣿⢋⡋⠘⣿⣿⣿⣿⣦⡙⢰⢢⡝⣳
⢀⠀⠀⠂⠀⡀⠀⠀⢈⠜⡀⠐⠄⡈⠂⡡⠀⢻⣽⠀⣿⠇⣼⣟⡾⠈⣇⢸⣮⡛⢿⣿⠟⣡⣾⣿⣿⣿⣿⣿⣿⠿⣫⣿⣿⣿⣿⣷⡘⢿⡀⠀⠁⢀⣾⢟⡵⠋⠀⡇⢈⠻⠯⣿⡿⣻⣦⣬⣘⠳
⠀⠈⠀⠀⠀⠀⠀⠀⢀⠊⡔⠈⠰⠠⠁⠄⠁⠀⠹⡀⣿⢀⣿⣿⣽⠃⣯⠀⢿⡿⢃⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣭⡻⢿⣿⣿⣿⣿⣮⣑⣀⣤⣭⡷⠋⠀⠀⢰⢁⡾⣷⠀⣩⣾⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠌⠀⠀⠀⠐⠠⠈⡐⠀⠀⠀⡏⣼⣿⣿⣯⡇⣿⠄⣠⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣍⣻⢿⣿⣿⣿⡿⠟⠁⠀⠀⠀⠀⠼⣸⡽⡞⣰⣿⣿⣿⣿⡿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠡⡁⢄⡈⠐⠀⠃⣿⣿⣿⡿⢃⣡⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣍⠛⠿⢿⣿⣿⣿⣿⣷⣝⠛⠁⠀⠀⠀⠀⠀⠀⠀⡇⣟⢎⣼⣿⣿⣿⠟⠉⣴⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡁⠂⠐⠡⠂⢠⣿⠟⣫⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣀⠈⠛⢿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠈⠀⡿⢣⣾⣿⣿⠟⢡⢎⣾⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡐⡀⠀⠀⠀⠘⣡⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣟⡿⣿⣿⣿⣿⣿⣿⣦⡀⠈⠻⢿⣿⣿⣿⣦⡀⠀⠀⠀⠀⢃⣿⣿⡿⠁⠀⢠⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢄⠡⡁⢆⢀⣿⣿⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣽⡻⢿⣿⣿⠟⠀⠀⠀⠀⠙⠻⣿⣿⣿⣄⠀⠀⢠⣿⣿⠟⣽⡅⠀⢜⡿⡿⣻⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠢⠁⠀⠘⡉⢉⠀⡀⠀⠙⠛⠿⠿⠿⠛⠿⠋⠉⠛⠛⠻⢿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⡟⠁⠀⠁⢈⠏⣶⢹⠆⠀⠀⠉⠀⠹⢿⡿⠀⠀
"""
uwuImg2 = """⣽⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⢁⠠⠀⣀⣤⣤⣴⢶⣲⢯⡟⣟⢯⢷⣳⠶⣦⣤⣤⣂⠀⠤⡂⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠉⠄⣠⣤⣶⢿⢿⣹⢾⣹⢾⣹⢯⡾⣽⣫⢾⣵⡻⣵⣫⢟⡽⣿⣶⣤⡁⠢⡉⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠟⣩⣶⢶⣾⣻⢳⣽⡻⣾⣭⢿⣭⢷⣫⣟⣳⢯⣝⡟⣾⣹⡗⣯⣻⣝⣞⣳⣏⡿⣷⣤⡑⠈⠹⣿⣿⣿⣿⣿⣿⢿⣿
⣿⣿⣿⣿⣿⠟⠁⢨⣾⡽⣯⢶⣯⣟⡾⣽⣳⣞⣯⣞⣷⣳⠾⣽⣻⢮⣟⣳⣭⣟⣳⢯⡾⣝⡷⣾⡝⡷⣯⢿⣶⣄⠈⠻⣿⣿⣿⣿⣿⣿
⣿⣿⣿⡿⠁⢂⣴⢿⣱⣟⣾⡻⠞⢁⣿⣳⡽⣞⡼⣞⡶⢯⣷⣄⠈⠛⠾⠽⠞⣷⣫⢷⣻⣭⢷⣳⠿⣝⡾⣛⡾⣽⣭⡁⡘⢿⣿⣷⣿⣿
⣿⣿⠟⠀⢠⣾⢯⡟⠗⠛⢈⣀⣴⣟⡾⢧⡿⣝⣻⣽⣺⢟⡾⣽⣻⢷⡶⣶⢶⡾⣽⢯⣳⣞⡯⣽⣻⡽⣻⣝⡯⣷⢯⣷⣞⠌⢿⣿⣿⣿
⡟⠋⠀⣠⡟⣽⣻⡴⣶⣟⣯⣟⡷⣻⣞⣯⢿⣝⡷⣭⣟⡾⣝⡷⡯⠛⠙⢉⣈⣁⣉⡙⠳⢯⣷⣻⢶⣛⡷⢯⣗⣯⣻⢾⡽⣞⣆⢻⣿⣿
⠀⡠⢁⣿⣽⣳⢯⣟⣷⣻⢾⣽⣻⢷⣹⠾⣽⢮⣟⡷⡽⢾⡽⠉⠀⠊⠉⠉⢉⣿⣿⣿⣷⣤⡁⠻⣻⣞⣽⣛⡾⢧⡿⣭⣟⡿⣞⣿⣿⣿
⠀⠁⣼⢷⡯⠟⢉⣈⡤⠈⠅⠈⠛⢯⣷⡻⣭⠷⣾⡽⣛⡧⠊⠀⠀⡀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣶⡈⠹⣞⣳⡟⣯⣽⣳⡭⣟⣿⣿⡜⢻
⠀⢸⣯⡟⢁⣴⡿⠋⠀⠀⠀⢠⣶⣄⠹⢿⣭⢻⣗⣻⣭⠃⠀⠀⡐⠀⠀⣿⣿⣿⣽⣻⣿⣿⣿⣿⣿⣆⠙⣯⣟⣳⡽⡾⣝⣻⣞⣿⣏⠀
⡄⢺⡗⢀⣾⡟⠀⠀⠀⢀⠂⠀⣿⣿⣦⠘⣯⣟⣮⢷⠃⠀⠀⠐⠀⠠⠀⠘⢿⣿⣿⣿⠛⢿⣿⣿⣿⣿⣆⠘⣯⢷⣻⡽⣏⡷⣯⢿⢹⢀
⡄⢻⠀⣾⣿⠃⠀⠀⢀⠂⠀⡀⠈⠻⠿⠆⠸⣟⣮⢻⠀⠀⠀⠁⠐⠀⡐⠀⠀⠀⠈⠀⠀⣻⣿⣿⣿⣿⣿⡆⢸⣟⣷⣻⣽⢻⣞⣿⢸⢸
⠆⡁⢸⣿⣿⠀⠀⠀⢀⠀⠂⠀⠄⠀⠀⠀⠀⠿⣜⡏⠀⠀⢠⣶⣤⡀⠀⠐⠀⠀⠀⠀⠀⣿⣯⣿⣿⢯⣿⣏⠠⣟⡾⣵⢯⣟⡾⣽⢻⠸
⠀⢡⢸⣿⣿⡄⠀⠀⣀⣀⠀⠁⠠⠈⠀⠀⢰⠈⡶⢥⠘⡄⠘⢿⣿⠇⠀⠀⠀⠀⠀⠀⣸⣿⣟⣿⢿⡿⣿⡧⠰⣿⡽⢯⡷⣾⡽⣿⣯⠀
⠀⠘⢈⣿⣿⣷⠀⠘⢿⣿⠃⠀⠀⠀⠀⢀⣾⠀⣝⣶⠀⢿⣄⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⣿⣾⣿⣿⣿⣿⡇⢸⣷⡻⢯⣟⡵⣿⣿⡇⣈
⠀⠆⠀⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⣠⣾⣿⠀⣿⣾⣧⠘⣿⣿⣦⣤⣤⣤⣤⣾⠟⠿⣿⣿⣿⣿⣿⣿⡿⠁⣼⣷⢿⣟⡾⣽⡗⠋⢰⣾
⣶⡀⢂⠹⣿⣿⣿⡿⢉⠐⣶⣤⣶⣿⣿⣿⡏⢰⣿⣳⣯⣧⠘⣿⣿⣿⣿⣿⣿⠁⣶⣶⡈⢻⣿⣿⣿⣿⠁⣾⡻⣜⣳⢮⡟⠇⡠⢡⣿⣿
⣿⣇⠀⢆⠙⢿⠟⢠⣾⡇⢸⣿⣿⣿⣿⡟⢠⣿⣟⣾⣽⡿⣧⡌⠻⣿⣿⣿⣿⠀⢿⡿⣿⣤⡙⠻⢿⠃⣸⢷⡹⢮⡽⢾⡝⡐⢠⣿⣿⣿
⣿⣿⠁⠀⠀⣀⣴⡿⣯⠅⠘⠛⣉⣉⣉⣤⣷⣌⠉⣴⣶⣾⣶⣿⣶⣤⣤⣤⣭⣤⣄⣿⣻⡽⣿⣷⣦⣄⠙⢷⣫⢷⣻⠃⠄⢠⣷⣿⣿⣿
⠓⠀⠄⣰⣾⢿⣛⣿⣻⣿⢿⣿⢿⡿⣿⣻⠯⠟⣀⡙⠻⠽⠷⢿⡾⢟⣿⣻⡽⣯⡿⣷⣟⣿⣳⢯⣟⡿⣷⣄⠙⢧⠤⠂⣴⣿⣿⣿⣿⣿
⠀⠈⣰⣿⣯⢿⣽⣳⡿⣽⣻⣾⡏⢉⣁⣤⣴⣾⢿⡿⣷⣶⣾⣶⣶⡆⢸⣿⣽⣳⢿⣻⣾⢯⣟⣿⢾⣽⣻⣿⣶⠀⠄⢸⣿⣿⣿⣿⣿⣿
⠀⢸⣿⣻⣭⢿⡾⣽⣟⡷⣿⣳⠃⢨⣿⣯⣟⣾⢯⣽⣟⣾⢧⣟⣯⣷⡀⢻⣯⣟⡿⣽⣾⢯⣿⢾⣯⣷⢯⣷⡿⡇⠀⢸⣿⣿⣿⣿⣿⣿
⠃⢺⣿⣳⣯⢿⡽⣿⣞⡿⣽⣿⠂⠀⠉⡛⠹⠯⣿⣿⢾⣟⣿⣻⣾⣟⣧⠘⣷⣯⣟⡿⣾⣻⢯⡿⣾⣽⣻⣾⡿⠁⠄⢸⣿⣿⣿⣿⣿⣿
⠀⠈⢿⣷⣯⢿⡽⣷⣻⣟⣿⡞⠀⠀⣶⣌⣁⡒⠀⠄⠉⠉⢉⣙⢃⣋⡙⠁⠻⣶⣿⣽⣷⢿⣯⣿⣷⣟⠯⠗⠁⠄⣰⣿⣿⣿⣿⣿⣿⣿
⣀⠉⠀⠛⠋⠛⠛⠛⠙⠋⠓⡁⠈⢰⣿⣿⣿⡿⡿⢶⡶⣶⣦⠤⡤⢠⠄⠀⠂⠀⣤⣉⣈⢉⣌⣠⠀⠀⠐⠂⠀⢶⣿⣿⣿⣿⣿⣿⣿⣿"""
