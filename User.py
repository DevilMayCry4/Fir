from flask_login import UserMixin
from DataBase import DataBase

class User(UserMixin):
    def test(self):
      return True

    def get_id(self):
        return self.user_id

    @staticmethod
    def register(username,password):
        return DataBase.register(username=username,password=password)

    @staticmethod
    def get(user_id):
        return User.getUserFromResult(DataBase.getUserWithId(user_id))

    @staticmethod
    def getUser(name,password):
        r = DataBase.getUser(name,password)
        return User.getUserFromResult(r)

    @staticmethod
    def findUser(username):
        return DataBase.findUser(username)

    @staticmethod
    def getUserFromResult(r):
        if r != None:
            user = User()
            user.user_id = r[0]
            user.username = r[1]
            user.password = r[2]
            return user
        else:
            return r
