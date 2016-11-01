# coding:utf-8
import urllib2
import json
import MySQLdb

class SpiderMain(object):
    def __init__(self):
        self.count = 0
        self.stopinstance = False

    def craw(self, root_url):
        while self.stopinstance is False:
            try:
                json_data = self.getData(root_url + str(self.count))
                if json_data is False:
                    return
                info = self.parserInfo(json_data)
                self.saveData(info)
                self.count += 1
            except:
                print "failed"

    def saveData(self, data):
        # 打开数据库连接
        db = MySQLdb.connect(host = "localhost", user = "fuming", passwd = "123456", db = "movie", charset="utf8")

        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        item_arr = []
        for item in data:
            item_arr.append("('" + item['name'] + "','" + item['avatar'] + "','" + item['baidu_url'] + "','')")

        sql = "INSERT IGNORE INTO web_actor(name, avatar, baidu_url, introduce) VALUES " + ','.join(item_arr);

        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()

        # 关闭数据库连接
        db.close()

    def parserInfo(self, data):
        if data:
            json_data = json.loads(data)
            user_list = json_data['data']['thisWeek']
        infos = []
        for item in user_list:
            infos.append({
                'name' : item['name'],
                'baidu_url' : item['url'],
                'avatar' : item['picUrl']
            })
        return infos

    def getData(self, url):
        if url is None:
            return None

        response = urllib2.urlopen(url)
        if response.getcode() != 200:
            return None
        json_data = response.read()
        if len(json_data) < 50:
            self.stopinstance = True
            print "parser over. exit"
            return False
        return json_data


# if __name__ == 'main':
root_url = 'http://baike.baidu.com/operation/api/starflowerstarlist?rankType=thisWeek&pg='
obj_spider = SpiderMain()
obj_spider.craw(root_url)