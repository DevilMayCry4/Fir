import os
import sqlite3
from flask import g


current_dir = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(current_dir,'data.sqlite')

class DataBase(object):
    @staticmethod
    def get_db():
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(DATABASE)
        return db


    @staticmethod
    def query_db(query, args=(), one=False):
        cur = DataBase.get_db().execute(query, args)
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv

    @staticmethod
    def excute_db(query,args=()):
        DataBase.get_db().execute(query, args)
        DataBase.get_db().commit()

    @staticmethod
    def getUser(name, password):
        return DataBase.query_db('select * from user where username = (?) and password = (?)' ,args=(name,password),one=True)


    @staticmethod
    def getUserWithId(user_id):
        return DataBase.query_db('select * from user where user_id = ?',args=(user_id,),one=True)

    @staticmethod
    def getAllApplication():
        return DataBase.query_db('select *from app')

    @staticmethod
    def findUser(name):
         return DataBase.query_db('select *from user where username= (?)',args=(name,),one=True) != None

    @staticmethod
    def register(username,password):
        return DataBase.excute_db('insert into user (username,password) values (?,?)',args=(username,password))