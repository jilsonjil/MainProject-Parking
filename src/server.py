from  flask import *

from src.dbconnection import *

app=Flask(__name__)

@app.route('/login',methods=['post'])
def login():
    uname = request.form['username']
    pswrd = request.form['password']
    qry = "select * from login where username=%s and password=%s"
    val = (uname, pswrd)
    result = selectone(qry, val)

    lid=result[0]
    if result is not None:
        return jsonify({"task":"success","id":lid})

    else:
        return jsonify({"task": "failed"})



@app.route('/registration',methods=['post'])
def registration():
    name = request.form['username']
    email = request.form['mail']
    vnum=request.form['vno']
    phone = request.form['phno']
    password = request.form['password']
    cpassword = request.form['cpassword']
    if password==cpassword:

        qry2 = "insert into login values(null,%s,%s,'user')"
        val2 = (email, password)

        iud(qry2, val2)
        qry = " insert into registration values(null,%s,%s,%s,%s)"

        val = (name, email, vnum, phone)
        iud(qry, val)

        return jsonify({"task": "success"})
    else:
        return jsonify({"task": "failed"})
@app.route('/viewarea')
def viewarea():
    qry="SELECT *FROM addarea"
    res = androidselectallnew(qry)
    return jsonify(res)
@app.route('/viewslot')
def viewslot():
    aid=request.form['aid']
    qry = "select * from slot WHERE `aid`=%s"
    res = selectall2(qry, session['aid'])
    return


app.run(host="0.0.0.0",port=5000)