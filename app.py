# coding=utf-8
import json
import paramiko
from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, disconnect
from flaskext.mysql import MySQL



mysql = MySQL()
app = Flask(__name__)
app.secret_key = '3444345'
app.config['MYSQL_DATABASE_USER'] = 'username'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Gs123*456'
app.config['MYSQL_DATABASE_DB'] = 'userauth'
app.config['MYSQL_DATABASE_HOST'] = '10.8.1.2'
mysql.init_app(app)
Session(app)
async_mode = None
socketio = SocketIO(app, async_mode=async_mode)


def get_ssh(ip, post,user, pwd):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, post, user, pwd, timeout=15)
        return ssh
    except Exception, e:
        print e
        return "False"


@app.route('/', methods=['GET', 'POST'])
def index():
    # host = request.args.get('host')
    cursor = mysql.get_db().cursor()
    cursor.execute("select host from hostauthon".format('Red'))
    hostdata = [dict(item=row[0]) for row in cursor.fetchall()]
    return (render_template('index.html', hostjsonStr=hostdata))


def numsort(obj):
    print obj
#    tmp=number.split(' *')
    tmp = re.split("\s+", obj)
    print tmp
    for i in range(len(tmp)):
        tmp[i] = int(tmp[i])
    print tmp
    tmp.sort()
    res = ""
    for i in tmp:
        res += (str(i) + " ")
    return res


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

@app.route('/app/logname', methods=['GET','POST'])
def requestlogname():
    if request.method == 'POST':
        logrev = request.get_json()['loglist']
        lognameresult = selcity(logrev)
        print ('--/app/logname--返回的应用名称--%s------' % lognameresult)
        return lognameresult
    else:
        return 'Data  is not post woring'


#@socketio.on('connect', namespace='/log')
def dojob(host,lognameresult):
    cursor =  mysql.get_db().cursor()                      
    sql="select hostname,port,user,password from hostauthon where host='"+host+"'"
    cursor.execute(sql)
    sqlconmmand = cursor.fetchone()
    for row in sqlconmmand:
        ip = row[0]
        port = row[1]
        user = row[2]
        password = row[3]
    return "ip=%s,port=%s,user=%s,pwd=%s" % \
             (ip, port, user, password)


if __name__ == '__main__':
    socketio.run(app,debug=True)
