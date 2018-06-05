# coding=utf-8
import json
from flask import Flask, render_template, redirect, request, session
from flaskext.mysql import MySQL



mysql = MySQL()
app = Flask(__name__)
app.secret_key = '3444345'
app.config['MYSQL_DATABASE_USER'] = ''
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = ''
app.config['MYSQL_DATABASE_HOST'] = '10.8.1.2'
mysql.init_app(app)
async_mode = None



@app.route('/', methods=['GET', 'POST'])
def index():
    # host = request.args.get('host')
    cursor = mysql.get_db().cursor()
    cursor.execute("select host from hostauthon".format('Red'))
    hostdata = [dict(item=row[0]) for row in cursor.fetchall()]
    return (render_template('index.html', hostjsonStr=hostdata))


@app.route('/app/hostname', methods=['POST'])
def selhost():
    if request.method == 'POST':
        rev = request.get_json()['host']
        result = selcity(rev)
        print ('----/app/hostname---返回的计算机名--%s----' % result)
        return result

    else:
        return 'Data  is not post woring'



def selcity(host):
    #print ('------host -%s ----------' % host)
    sql = "select s.logname from hostauthon as h,server_log_list as s where h.host = '"+host+"' and h.hostname = s.hostname"
    cursor = mysql.get_db().cursor()
    cursor.execute(sql)
    result=cursor.fetchall()
    SLog = []
    data = {}
    for r in result:
        logname = {}
        logname = r[0]
        SLog.append(logname)
    #data['name'] = 'logname'
    data['loglist'] = SLog

    results = json.dumps(data)
    print ('----发送的应用列表--%s---------' % results)

    return results



if __name__ == '__main__':
    app.run(app,debug=True)
