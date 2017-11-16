from flask_login import  UserMixin

class User(UserMixin):
    def test(self):
      return True