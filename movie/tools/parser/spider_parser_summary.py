import urllib2
import MySQLdb
from bs4 import BeautifulSoup


class SpiderMain(object):
    def __init__(self):
        self.start = 0
        self.limit = 50
        self.stopinstance = False
        self.data = []

    def craw(self, root_url):
        while self.stopinstance is False:
            # try:
            if len(self.data) == 0:
                self.data = list(self.getUrls(self.start))
                if len(self.data) == 0:
                    self.stopinstance = True
                    return
                self.start += self.limit
            current_data = self.data.pop()
            summary = self.getData(root_url + current_data[2])
            if len(summary) != 0:
                self.saveData({'id': current_data[0], 'introfuce': summary})
            # except:
            #     print "failed"

    def saveData(self, data):
        db = MySQLdb.connect(host = "localhost", user = "fuming", passwd = "123456", db = "movie", charset="utf8")
        cursor = db.cursor()
        sql = "UPDATE web_actor SET introduce='" + data['introfuce'].encode('utf-8') + "' WHERE id=" + str(data['id']);
        try:
            cursor.execute(sql)
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()

        db.close()

    def getData(self, url):
        if url is None:
            return None

        response = urllib2.urlopen(url)
        if response.getcode() != 200:
            return None
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        summary_node = soup.find('div', class_="lemma-summary")
        return summary_node.get_text()

    def getUrls(self, limit):
        db = MySQLdb.connect(host="localhost", user="fuming", passwd="123456", db="movie", charset="utf8")
        cursor = db.cursor()
        sql = "SELECT id, `name`, baidu_url, introduce FROM web_actor WHERE introduce = '' LIMIT " + str(self.start) + "," + str(self.limit);

        # try:
        cursor.execute(sql)
        results = cursor.fetchall()
        # except:
        # Rollback in case there is any error
        db.rollback()

        db.close()

        return results



# if __name__ == 'main':
root_url = 'http://baike.baidu.com'
obj_spider = SpiderMain()
obj_spider.craw(root_url)