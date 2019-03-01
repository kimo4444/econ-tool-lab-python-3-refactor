import sqlite3


def connectDb(path):
    dbConnection = sqlite3.connect(path)
    return dbConnection
