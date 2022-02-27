import math
import time


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getMenu(self):
        sql = """SELECT * FROM mainmenu"""
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except Exception as e:
            print('Ошибка чтения БД')
        return ()

    def addPost(self, title, text, url):
        try:
            self.__cur.execute(
                f"SELECT COUNT() as 'count' FROM posts WHERE url LIKE '{url}'"
            )
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Статья с таким url уже существует")
                return False

            tm = math.floor(time.time())
            self.__cur.execute(
                "INSERT INTO posts VALUES(NULL, ?, ?, ?, ?)", (title, text, url, tm)
            )
            self.__db.commit()
        except Exception as e:
            print('Ошибка добавления статьи в БД')
            return False
        return True

    def getPost(self, alias):
        sql = f"SELECT title, text FROM posts WHERE url LIKE '{alias}' LIMIT 1"
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchone()
            if res:
                return res
        except Exception as e:
            print('Ошибка получения статьи из БД')
        return (False, False)

    def getPosts(self):
        sql = """SELECT id, title, text, url FROM posts ORDER BY time DESC"""
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except Exception as e:
            print('Ошибка чтения постов из БД')
        return ()
