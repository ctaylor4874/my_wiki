import mysql.connector
import dbconfig


class Page:
    def placeHolder(self):
        exists = Database.checkTitles(self.title)
        if exists:
            query = "select page_content,last_modified_date,author_last_modified, id from page where title = '%s'" % self.title
            entry = Database.getAll(query)
            self.page_content = entry[0]
            self.last_modified_date = entry[1]
            self.author_last_modified = entry[2]
        return exists

    def save(self):
        exists = Database.checkTitles(self.title)
        if exists:
            query = "UPDATE page SET page_content = '%s', author_last_modified = '%s', last_modified_date = now() WHERE title = '%s'" % (
                Database.escape(self.page_content), Database.escape(self.author_last_modified), self.title)
            Database.doQuery(query)
            query = "select page_content,last_modified_date,author_last_modified, id from page where title = '%s'" % self.title
            entry = Database.getAll(query)
            self.page_content = entry[0]
            self.last_modified_date = entry[1]
            self.author_last_modified = entry[2]
            self.id = entry[3]
            self.pageid = self.id
            query = "insert into pagehistory (title, page_content, author_last_modified, last_modified_date, pageid) values('%s', '%s', '%s',now(), %d)" % (
                self.title, Database.escape(self.page_content), Database.escape(self.author_last_modified), self.pageid)
            Database.doQuery(query)
        else:
            query = "insert into page (title, page_content, author_last_modified, last_modified_date) values('%s', '%s', '%s',now())" % (
                self.title, Database.escape(self.page_content), Database.escape(self.author_last_modified))
            Database.doQuery(query)
            query = "select page_content,last_modified_date,author_last_modified,id from page where title = '%s'" % self.title
            entry = Database.getAll(query)
            self.page_content = entry[0]
            self.last_modified_date = entry[1]
            self.author_last_modified = entry[2]
            self.id = entry[3]
            self.pageid = self.id
            query = "insert into pagehistory (title, page_content, author_last_modified, last_modified_date, pageid) values('%s', '%s', '%s',now(), %d)" % (
                self.title, Database.escape(self.page_content), Database.escape(self.author_last_modified), self.pageid)
            Database.doQuery(query)

    def update(self):
        exists = Database.checkTitles(self.title)
        if exists:
            query = "select page_content from page where title = '%s'" % self.title
            self.page_content = Database.getContent(query)

    # def __str__(self):
    #     return self.name

    @staticmethod
    def getObjects():
        query = "SELECT title FROM page"
        pages = []
        result_set = Database.getResult(query)
        for item in result_set:
            pages.append(item[0])
        return pages


class Database(object):
    @staticmethod
    def getConnection():
        return mysql.connector.connect(user=dbconfig.dbUser, password=dbconfig.dbPassword, host=dbconfig.dbHost,
                                       database=dbconfig.dbName)

    @staticmethod
    def escape(value):
        return value.replace("'", "''")

    @staticmethod
    def getAll(query):
        conn = Database.getConnection()
        cur = conn.cursor()
        cur.execute(query)
        entry = cur.fetchone()
        cur.close()
        conn.close()
        return entry

    @staticmethod
    def getContent(query):
        conn = Database.getConnection()
        cur = conn.cursor()
        cur.execute(query)
        entry = cur.fetchone()
        page_content = entry[0]
        cur.close()
        conn.close()
        return page_content

    @staticmethod
    def getResult(query, getOne=False):
        conn = Database.getConnection()
        cur = conn.cursor()
        cur.execute(query)
        if getOne:
            result_set = cur.fetchone()
        else:
            result_set = cur.fetchall()
        cur.close()
        conn.close()
        return result_set

    @staticmethod
    def checkTitles(title):
        conn = Database.getConnection()
        cur = conn.cursor()
        sql = "SELECT COUNT(1) FROM page WHERE title = '%s'" % title
        cur.execute(sql)
        if cur.fetchone()[0]:
            exists = True
        else:
            exists = False
        cur.close()
        conn.close()
        return exists

    @staticmethod
    def doQuery(query):
        conn = Database.getConnection()
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        cur.close()
        conn.close()
