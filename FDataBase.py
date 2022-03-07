import math
import sqlite3
import time


class FDataBase:

    def getMenu(self):
        try:
            qs = MenuElements.query.all()
            return qs
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

    def addUser(self, username, email, password_hash):
        try:
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM users WHERE email LIKE '{email}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Пользователь с таким email уже существует")
                return False

            tm = math.floor(time.time())
            self.__cur.execute(
                "INSERT INTO users VALUES(NULL, ?, ?, ?, NULL, ?)", (username, email, password_hash, tm)
            )
            self.__db.commit()
        except Exception as e:
            print('Ошибка получения статьи из БД')
            return False
        return True

    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except Exception as e:
            print("Ошибка получения данных из бд" + str(e))
        return False

    def getUserByEmail(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except Exception as e:
            print("Ошибка получения данных из бд" + str(e))

        return False

    def updateUserAvatar(self, avatar, user_id):
        if not avatar:
            return False

        try:
            binary = sqlite3.Binary(avatar)
            self.__cur.execute(f"UPDATE users SET avatar = ? where id = ?", (binary, user_id))
            self.__db.commit()
        except Exception as e:
            print("Ошибка обновления аватара" + str(e))
            return False
        return True
