import sqlite3

class HtmlOutputer(object):
    def __init__(self):
        self.datas = []

    def collect_data(self, data):
        if data is None:
            return
        # self.datas.append(data)
        self.interDb(data)

    def output_html(self):
        fout = open('output.html', 'w')
        fout.write('<html>')
        fout.write('<body>')

        fout.write('<table>')
        for data in self.datas:
            fout.write("<tr>")
            fout.write("<td>%s</td>" % data['url'].encode('utf-8'))
            fout.write("<td>%s</td>" % data['title'].encode('utf-8'))
            fout.write("<td>%s</td>" % data['summary'].encode('utf-8'))
            fout.write("</tr>")
        fout.write('</table>')

        fout.write('</body>')
        fout.write('</html>')

    def interDb(self, data):
        conn = sqlite3.connect('test.db')
        conn.execute("INSERT OR IGNORE INTO test (title,summary,url)  VALUES ('" +
                     data['title'].encode('utf-8') + "', '" +
                     data['summary'].encode('utf-8') + "', '" +
                     data['url'].encode('utf-8') + "')")
        conn.commit()
        conn.close()