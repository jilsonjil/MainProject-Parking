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


    if result is not None:
        lid = result[0]
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

        lid=iud(qry2, val2)
        qry = "insert into registration values(null,%s,%s,%s,%s,%s)"

        val = (lid,name, email, vnum, phone)
        iud(qry, val)

        return jsonify({"task": "success"})
    else:
        return jsonify({"task": "failed"})
@app.route('/booking',methods=['post'])
def booking():
    print(request.form)
    uid=request.form['uid']
    uname=request.form['username']
    endate = request.form['endate']
    exdate = request.form['exdate']
    sid=request.form['sid']
    vid=request.form['vid']
    slot = request.form['slot']
    floor=request.form['floor']
    qry = "insert into booking values(null,%s,%s,%s,%s,'booked',%s,%s,%s)"
    print("f==",floor)

    val=(uid,endate,exdate,sid,vid,slot,uname)
    bid=iud(qry,val)
    qry="select datediff(extime,entime) from booking where bookid=%s"
    res=selectone(qry,bid)
    day=int(res[0])+1
    amount=day*15
    return jsonify({"task": "success","bid":bid,"amt":amount})

@app.route('/searchslot',methods=['post'])
def searchslot():
    aid=request.form['aid']
    endate = request.form['endate']
    exdate = request.form['exdate']
    floor=request.form['floor']

    result=[]
    qry = "select * from slot WHERE `aid`=%s AND  `floor`= %s and type='R'"
    val=(aid,floor)
    res=androidselectall(qry,val)
    for i in res:
        sid=i['sid']
        qry="SELECT * FROM `booking` WHERE sid=%s and `sid` IN(SELECT `sid` FROM `slot` WHERE `aid`=%s AND `floor`=%s) AND ((`entime` BETWEEN %s AND %s) or (`extime` BETWEEN %s AND %s))"
        val=(sid,aid,floor,endate,exdate,endate,exdate)
        print(qry,val)
        rr=selectone(qry,val)
        row=i
        if rr is None:
            row['cs']="free"
        else:
            row['cs'] = "booked"
        result.append(row)
        print(result)
    return jsonify(result)




@app.route('/viewarea')
def viewarea():
    qry="SELECT *FROM addarea"
    res = androidselectallnew(qry)
    return jsonify(res)

@app.route('/afeedback',methods=['post'])
def afeedback():


    feed=request.form['feed']
    bid=request.form['bid']
    lid=request.form['lid']
    qry="select aid from slot where sid in(select sid from booking where bookid=%s)"
    res=selectone(qry,bid)
    qry="insert into feedback values(null,%s,%s,%s,curdate())"
    val=(res[0],lid,feed)
    iud(qry,val)

    return jsonify({"task":"success"})
@app.route('/acomplaint',methods=['post'])
def acomplaint():


    feed=request.form['comp']
    bid=request.form['bid']
    lid=request.form['lid']
    qry="select aid from slot where sid in(select sid from booking where bookid=%s)"
    res=selectone(qry,bid)
    qry="insert into complaint values(null,%s,%s,%s,curdate(),'pending')"
    val=(res[0],lid,feed)
    iud(qry,val)

    return jsonify({"task":"success"})

@app.route('/Payment',methods=['post'])
def Payment():

    bid=request.form['bid']
    amt=request.form['amt']
    cnum=request.form['cnum']
    exdate=request.form['exdate']
    cvv=request.form['cvv']

    qry="insert into payment values(null,%s,%s,%s,%s,%s,curdate(),'completed')"
    val=(bid,amt,cnum,exdate,cvv)
    iud(qry,val)
    return jsonify({"task": "success"})



@app.route('/viewprofile',methods=['post'])
def viewprofile():
    lid=request.form['lid']
    qry="select * from registration where lid=%s"
    res=androidselectall(qry,lid)
    print(res,lid)
    return jsonify(res[0])

@app.route('/update',methods=['post'])
def update():


    username=request.form['username']
    mail=request.form['mail']
    vno=request.form['vno']
    phno=request.form['phno']
    lid=request.form['lid']

    qry="update registration set name=%s,email=%s,vno=%s,phone=%s where lid=%s"
    val=(username,mail,vno,phno,lid)
    iud(qry,val)
    return jsonify({"task": "success"})


@app.route('/viewslot',methods=['post'])
def viewslot():
    aid=request.form['aid']

    qry = "select * from slot WHERE `aid`=%s AND  `type`='R'"
    res = androidselectall(qry, aid)

    return jsonify(res)

@app.route('/viewareas',methods=['post'])
def viewareas():
    qry = "SELECT * FROM `addarea`"
    res = androidselectallnew(qry)
    ress=[]
    for i in res:
        row=i
        id=i["aid"]
        qry="SELECT * FROM `slot` WHERE `aid`=%s AND `type`='R'"

        qry1="SELECT * FROM `slot` WHERE `aid`=%s AND STATUS='free' AND  `type`='R'"

        qry2="SELECT * FROM `slot` WHERE `aid`=%s AND `type`='NR'"

        qry3="SELECT * FROM `slot` WHERE `aid`=%s AND STATUS='free' AND`type`='NR'"


        res1=selectall2(qry,id)
        res2=selectall2(qry1,id)
        res3=selectall2(qry2,id)
        res4=selectall2(qry3,id)

        row['ra']=str(len(res2))+"/"+str(len(res1))
        row['na']=str(len(res4))+"/"+str(len(res3))

        qry="SELECT DISTINCT `floor` FROM `slot` WHERE `aid`=%s"
        res5=selectall2(qry,id)
        rr=["Select"]
        for i in res5:
            rr.append(str(i[0]))
        flrs=','.join(rr)
        row['flr']=flrs

        ress.append(row)

    return jsonify(ress)


@app.route('/viewbookings',methods=['post'])
def viewbookings():
    aid=request.form['lid']

    qry = "select booking.bookid,booking.entime,booking.extime,booking.slot,slot.floor from booking,slot where booking.sid=slot.sid and booking.uid='"+aid+"'"
    res = androidselectallnew(qry)

    return jsonify(data=res,status="ok")



app.run(host="0.0.0.0",port=5000)