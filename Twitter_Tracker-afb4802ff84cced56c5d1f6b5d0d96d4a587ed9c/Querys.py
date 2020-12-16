import mysql.connector as db

HOST = "remotemysql.com"
PORT = 3306
USER = ""
PASSWORD = ""
DB = ""

try:
    connection = db.connect(host=HOST, port=PORT,
                            user=USER, passwd=PASSWORD, db=DB)

    dbhandler = connection.cursor()

    class historico:
        def __init__(self):
          dbhandler = connection.cursor()
          dbhandler.execute("select * from twitter")
          result = dbhandler.fetchall()
          for item in result:
              print(item)

    class save:
        def __init__(self):
            dbhandler = connection.cursor()
            sql = "INSERT INTO twitter (username, created_at, tweet, retweet_count,place, location) VALUES (%s, %s, %s, %s, %s, %s)"
            dbhandler.execute(sql)
            result = dbhandler.fetchall()
            for item in result:
                print(item)



    class delete:
        def __init__(self, name):
            self.name = name
            dbhandler = connection.cursor()
            dbhandler.execute("DELETE * FROM twitter WHERE ID = 6")
            result = dbhandler.fetchall()
            for item in result:
                print(item)

    connection.close()

except Exception as e:
    print(e)


