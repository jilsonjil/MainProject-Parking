from flask import *
import os
from src.dbconnection import *
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "sdsd"
import functools


def login_required(func):
    @functools.wraps(func)
    def secure_function():
        if "lid" not in session:
            return render_template('signin.html')
        return func()

    return secure_function


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/logins')
def logins():
    return render_template('signin.html')


@app.route('/logout')
def logout():
    session.clear()
    return render_template('signin.html')


@app.route('/admin_home')
@login_required
def admin_home():

    qry="select count(*),sum(amount) from bill where date=curdate()"
    res=selectall(qry)

    tc=res[0][0]
    tamt=0
    try:
        tamt=int(res[0][1])
    except:
        pass

    qry="select count(*),sum(amount) from bill where month(date)=month(curdate())"
    res=selectall(qry)

    mc=res[0][0]
    mamt=0
    try:
        mamt=int(res[0][1])
    except:
        pass
    row=[tc,tamt,mc,mamt]
    qry="select day(date),sum(amount) from bill where month(date)=month(curdate()) group by date"
    res=selectall(qry)
    x=[]
    y=[]

    max=0
    for i in res:
        x.append(int(i[0]))
        y.append(int(i[1]))
        if int(i[1])>max:
            max=int(i[1])
    max=max+10
    return render_template('dash.html',v=row,x=x,y=y,m=max)


@app.route('/manager_home')
@login_required
def manager_home():
    qry = "select count(*),sum(amount) from bill where date=curdate() and  vid in(select id from vehicle where sid in(select sid from slot where aid=%s))"
    res = selectall2(qry,session['lid'])

    tc = res[0][0]
    tamt = 0
    try:
        tamt = int(res[0][1])
    except:
        pass

    qry = "select count(*),sum(amount) from bill where month(date)=month(curdate())  and  vid in(select id from vehicle where sid in(select sid from slot where aid=%s))"
    res = selectall2(qry,session['lid'])

    mc = res[0][0]
    mamt = 0
    try:
        mamt = int(res[0][1])
    except:
        pass
    row = [tc, tamt, mc, mamt]
    qry = "select day(date),sum(amount) from bill where month(date)=month(curdate())  and  vid in(select id from vehicle where sid in(select sid from slot where aid=%s)) group by date"
    res = selectall2(qry,session['lid'])
    x = []
    y = []

    max = 0
    for i in res:
        x.append(int(i[0]))
        y.append(int(i[1]))
        if int(i[1]) > max:
            max = int(i[1])
    max = max + 10


    return render_template('mdash.html', v=row, x=x, y=y, m=max)

@app.route('/staff_home')
def staff_home():
    return render_template('sdash.html')


@app.route('/parea', methods=['post'])
@login_required
def parea():
    return render_template('parkareaadd.html')


@app.route('/addslot', methods=['post'])
@login_required
def addslot():
    return render_template('addslot.html')


@app.route('/pmanager', methods=['post', 'get'])
@login_required
def pmanager():
    qry = "SELECT * FROM  `addarea`"
    res = selectall(qry)
    return render_template('addmanager.html', a='0', val=res)


@app.route('/latilongi', methods=['post'])
@login_required
def latilongi():
    return render_template('lati longi.html')




@app.route('/pstaff', methods=['post', 'get'])
def pstaff():
    return render_template('addstaff.html')


@app.route('/uparea')
def uparea():
    areaid = request.args.get('id')
    session['areaid'] = areaid
    qry = "select * from addarea where aid=%s"
    val = (areaid)
    res = selectone(qry, val)
    return render_template("parkareaupdate.html", val=res)


@app.route('/upslot')
@login_required
def upslot():
    slid = request.args.get('id')
    session['slid'] = slid
    qry = "select * from slot where sid=%s"
    val = (slid)
    res = selectone(qry, val)
    return render_template("updateslot.html", val=res)


@app.route('/upmanager')
def upmanager():
    mid = request.args.get('id')
    session['mid'] = mid
    qry = "select * from manager where pm_id=%s"
    qry2 = "select * from addarea"
    val = (mid)
    res = selectone(qry, val)
    res2 = selectall(qry2)
    return render_template("managerupdate.html", val=res, data=res2)


@app.route('/upstaff')
def upstaff():
    mid = request.args.get('id')
    session['mid'] = mid
    qry = "select * from staff where sid=%s"
    val = (mid)
    res = selectone(qry, val)
    return render_template("updatestaff.html", val=res)


@app.route('/logincode', methods=['post'])
def logincode():
    uname = request.form['textfield']
    pswrd = request.form['textfield2']
    qry = "select * from login where username=%s and password=%s"
    val = (uname, pswrd)
    result = selectone(qry, val)

    print(val)
    if result is None:
        return render_template('signin.html', a='-1')
    elif result[3] == "admin":
        session['lid'] = result[0]

        return redirect('/admin_home')
    elif result[3] == "staff":
        qry = "SELECT `aid` FROM `staff` WHERE `mail`=%s"
        session['lid'] = result[0]
        return redirect('/staff_home')

    elif result[3] == "manager":
        qry = "SELECT `aid` FROM `manager` WHERE `mail`=%s"
        res11 = selectone(qry, uname)
        session['aid'] = res11[0]
        session['lid'] = result[0]
        qry = "SELECT addarea.aid,manager.pm_id FROM `addarea` inner join manager on addarea.aid=manager.aid inner join login on login.username=manager.mail WHERE login.`lid`=%s"
        res1 = selectone(qry, result[0])
        session['pm_id'] = result[1]

        return redirect('/manager_home')
    else:

         return ''''<script>alert("error");
                 window.location='/logins'</script>'''


@app.route('/areaadd', methods=['post', 'get'])
def areaadd():
    name = request.form['textfield']
    place = request.form['textfield2']
    des = request.form['textarea']
    lat = request.form['lat']
    lon = request.form['lng']
    qry = " insert into addarea values(null,%s,%s,%s,%s,%s)"
    val = (name, place, des, lat, lon)
    iud(qry, val)
    return ''''<script>alert("successfully added");
        window.location='/viewparea'</script>'''


@app.route('/addslotcode', methods=['post', 'get'])
def addslotcode():
    floor = request.form['textfield']
    slot = request.form['textfield2']
    slot1 = request.form['textfield3']
    type=request.form['s']
    s = int(slot1)
    s1 = int(slot)
    for i in range(s1, s+s1):
        qry = " insert into slot values(null,%s,%s,%s,'free',%s)"
        val = (session['aid'], i , floor,type)
        iud(qry, val)
    return ''''<script>alert("successfully added");
        window.location='/viewslot'</script>'''


@app.route('/updateslotcode', methods=['post'])
def updateslotcode():
    floor = request.form['textfield']
    slot = request.form['textfield2']
    type = request.form['s']
    status = request.form['status']

    qry2 = "UPDATE `slot` SET `slot_no`=%s,`floor`=%s,`status`=%s,`type`=%s WHERE `sid`=%s"
    val2 = (slot, floor, status,type, int(session['slid']))
    iud(qry2, val2)
    print(qry2)
    return ''''<script>alert("successfully updated");
        window.location='/viewslot'</script>'''


@app.route('/manageradd', methods=['post', 'get'])
def manageradd():
    name = request.form['name']
    add = request.form['address']
    gender = request.form['gender']
    dob1 = request.form['dob']
    mail = request.form['mail']
    ph = request.form['phone']
    photo = request.files['photo']
    pic = secure_filename(photo.filename)
    photo.save(os.path.join('static', pic))
    tmp = str(dob1).split('-')
    dob = tmp[2] + "-" + tmp[1] + "-" + tmp[0]
    arplace = request.form['area']
    qry = "select * from manager where `mail`=%s"
    v = (mail)
    re = selectone(qry, v)
    print("-------------------------", dob)
    if re is not None:
        qry = "SELECT * FROM  `addarea`"
        res = selectall(qry)
        return render_template('addmanager.html', a='-1', val=res)
    qry = " insert into manager values(null,%s,%s,%s,%s,%s,%s,%s,%s,'Active')"
    print("---- ", qry)
    qry2 = "insert into login values(null,%s,%s,'manager')"
    val2 = (mail, dob)
    iud(qry2, val2)
    val = (name, add, gender, dob1, mail, ph, pic, arplace)
    iud(qry, val)
    print(val)
    return ''''<script>alert("successfully added");window.location='/viewmanager'</script>'''


@app.route('/upareacode', methods=['post'])
def upareacode():
    name = request.form['textfield']
    place = request.form['textfield2']
    des = request.form['textarea']
    lat = request.form['lat']
    lon = request.form['lng']
    qry2 = "UPDATE `addarea` SET `arname`=%s,`arplace`=%s,`desc`=%s,`latitude`=%s,`longitude`=%s WHERE `aid`=%s"
    val2 = (name, place, des, lat, lon, session['areaid'])
    iud(qry2, val2)
    return ''''<script>alert("successfully updated");
        window.location='/viewparea'</script>'''


@app.route('/upmanagercode', methods=['post'])
def upmanagercode():
    try:
        name = request.form['name']
        add = request.form['address']
        gender = request.form['gender']
        dob = request.form['dob']
        mail = request.form['mail']
        ph = request.form['phone']
        photo = request.files['photo']
        pic = secure_filename(photo.filename)
        tmp = str(dob).split('-')
        dob = tmp[2] + "-" + tmp[1] + "-" + tmp[0]
        arplace = request.form['area']
        status = request.form['status']
        photo.save(os.path.join('static', pic))
        qry2 = "UPDATE `manager` SET `fullname`=%s,`address`=%s,`gender`=%s,`dob`=%s,`mail`=%s,`phone`=%s,`photo`=%s,`aid`=%s, `status`=%s WHERE `pm_id`=%s"
        val2 = (name, add, gender, str(dob), mail, ph, pic, arplace, status, session['mid'])
        iud(qry2, val2)
        return ''''<script>alert("successfully updated");
            window.location='/viewmanager'</script>'''
    except Exception as e:
        name = request.form['name']
        add = request.form['address']
        gender = request.form['gender']
        dob = request.form['dob']
        mail = request.form['mail']
        ph = request.form['phone']
        status = request.form['status']
        arplace = request.form['area']

        qry2 = "UPDATE `manager` SET `fullname`=%s,`address`=%s,`gender`=%s,`dob`=%s,`mail`=%s,`phone`=%s,`aid`=%s,`status`=%s WHERE `pm_id`=%s"
        val2 = (name, add, gender, str(dob), mail, ph, arplace, status, session['mid'])
        iud(qry2, val2)
        return ''''<script>alert("successfully updated");
                    window.location='/viewmanager'</script>'''


@app.route('/staffaddcode', methods=['post', 'get'])
def staffaddcode():
    name = request.form['name']
    add = request.form['address']
    gender = request.form['gender']
    dob1 = request.form['dob']
    mail = request.form['mail']
    ph = request.form['phone']
    photo = request.files['photo']

    pic = secure_filename(photo.filename)
    photo.save(os.path.join('static', pic))
    tmp = str(dob1).split('-')
    dob = tmp[2] + "-" + tmp[1] + "-" + tmp[0]
    qry=" select aid from manager where pm_id=%s"
    res=selectone(qry,session['lid'])

    qry = " insert into staff values(null,%s,%s,%s,%s,%s,%s,%s,%s)"
    qry2 = "insert into login values(null,%s,%s,'staff')"
    val2 = (mail, dob)
    iud(qry2, val2)
    val = (name, gender, add, dob1, mail, ph, pic,res[0])
    iud(qry, val)
    return ''''<script>alert("successfully added");
        window.location='/viewstaff'</script>'''


@app.route('/upstaffcode', methods=['post'])
def upstaffcode():
    name = request.form['name']
    add = request.form['address']
    gender = request.form['gender']
    dob1 = request.form['dob']
    mail = request.form['mail']
    ph = request.form['phone']
    tmp = str(dob1).split('-')
    dob = tmp[2] + "-" + tmp[1] + "-" + tmp[0]
    status = request.form['status']


    qry2 = "UPDATE `staff` SET `name`=%s,`address`=%s,`gender`=%s,`dob`=%s,`mail`=%s,`phone`=%s  WHERE `sid`=%s"
    val2 = (name, gender, add, dob1, mail, ph, session['mid'])
    iud(qry2, val2)
    return ''''<script>alert("successfully updated");
        window.location='/viewstaff'</script>'''


@app.route('/viewparea', methods=['post', 'get'])
@login_required
def viewparea():
    qry = "select * from addarea "
    res = selectall(qry)
    return render_template('view.html', val=res)

@app.route('/admin_feedback', methods=['post', 'get'])
@login_required
def admin_feedback():
    qry = "select feedback.*,addarea.arname,registration.name from addarea join feedback on feedback.pid=addarea.aid join registration on registration.lid=feedback.lid order by feedback.id desc"
    res = selectall(qry)

    return render_template('admin_feedback.html', val=res)

@app.route('/manager_complaint', methods=['post', 'get'])
@login_required
def manager_complaint():
    qry = "select complaint.*,addarea.arname,registration.name from addarea join complaint on complaint.pid=addarea.aid join registration on registration.lid=complaint.lid where addarea.aid=%s and reply='pending' order by complaint.id desc"
    res = selectall2(qry,session['lid'])
    f="0"
    if len(res)>0:
        f="1"
    return render_template('manager_complaint.html', val=res,f=f)


@app.route('/reply', methods=['post', 'get'])
@login_required
def reply():
    id=request.args.get("id")
    session['cid']=id
    return render_template('complaint_reply.html')


@app.route('/addreply', methods=['post', 'get'])
@login_required
def addreply():

    id=session['cid']
    repl=request.form['textfield']
    qry="update complaint set reply=%s where id=%s"
    val=(repl,id)
    iud(qry,val)
    return redirect("/manager_complaint")


@app.route('/admin_report', methods=['post', 'get'])
@login_required
def admin_report():
    qry = "select feedback.*,addarea.arname,registration.name from addarea join feedback on feedback.pid=addarea.aid join registration on registration.lid=feedback.lid order by feedback.id desc"
    res = selectall(qry)
    return render_template('admin_feedback.html', val=res)
@app.route('/viewreser', methods=['post', 'get'])
def viewreser():
    qry = "SELECT *,DATE_FORMAT(booking.entime,'%d-%m-%Y %H:%i:%S') AS DO ,DATE_FORMAT(booking.extime,'%d-%m-%Y %H:%i:%S') AS DOE FROM booking where  date(entime)=curdate()  ORDER BY entime"
    res = selectall(qry)
    return render_template('viewreserve.html', val=res,d="")

@app.route('/viewreser1', methods=['post', 'get'])
def viewreser1():
    d=request.form['d']

    qry = "SELECT *,DATE_FORMAT(booking.entime,'%d-%m-%Y %H:%i:%S') AS DO ,DATE_FORMAT(booking.extime,'%d-%m-%Y %H:%i:%S') AS DOE FROM booking where  date(entime)='"+d+"'  ORDER BY entime"
    res = selectall(qry)
    return render_template('viewreserve.html', val=res,d=d)

@app.route('/viewpark', methods=['post', 'get'])
def viewpark():
    qry=" select vehicle.*,slot.slot_no,slot.floor,slot.status,booking.status from vehicle left join slot on vehicle.sid=slot.sid left join booking on booking.bookid=vehicle.bookid where vehicle.status!='finished' and vehicle.aid in(select status from staff where sid="+str(session['lid'])+")"
    # qry = "select *,DATE_FORMAT(vehicle.entry,'%d-%m-%Y %H:%i:%S') as do from vehicle order by entry"
    res = selectall(qry)
    print(qry)
    return render_template('viewparking.html', val=res)


@app.route('/alocatesloat', methods=['post', 'get'])
def alocatesloat():
    id=request.args.get("id")
    session['vid']=id

    qry="select * from slot where status='free' and type='NR' and  aid in(select status from staff where sid="+str(session['lid'])+")"
    res=selectall(qry)
    return render_template('viewparking1.html', val=res)


@app.route('/alocate_sloat1', methods=['post', 'get'])
def alocate_sloat1():
    s=request.form['s']
    id=session['vid']
    print(s,)

    qry="update vehicle set sid=%s where id=%s"
    val=(s,id)
    iud(qry,val)

    qry="update slot set status='allocated' where sid=%s"
    iud(qry,s)

    qry="update booking set status='entered',sid=%s where bookid in(select bookid from vehicle where id=%s)"
    val=(s,id)
    iud(qry,val)

    return redirect("/viewpark")


@app.route('/viewmanager', methods=['post', 'get'])
@login_required
def viewmanager():
    qry = "SELECT manager.*,DATE_FORMAT(manager.dob,'%d-%m-%Y') as do,addarea.arname FROM  manager inner join addarea on manager.aid=addarea.aid order by manager.status"
    res = selectall(qry)
    return render_template('view_pmanager.html', val=res)


@app.route('/viewstaff', methods=['post', 'get'])
@login_required
def viewstaff():
    qry = " select aid from manager where pm_id=%s"
    res = selectone(qry, session['lid'])

    qry = "select *,DATE_FORMAT(dob,'%d-%m-%Y') as do from staff where staff.status="+str(res[0])
    res = selectall(qry)
    return render_template('viewstaff.html', val=res)


@app.route('/viewslot', methods=['post', 'get'])
@login_required
def viewslot():
    qry = "SELECT * FROM slot where aid=%s"
    res = selectall2(qry, session['aid'])
    print(session['aid'])
    return render_template('viewslot.html', val=res)


@app.route('/delparea', methods=['post', 'get'])
def delparea():
    eid = request.args.get('id')
    session['eid2'] = eid
    qry = "delete from addarea where aid=%s"
    val = (eid)
    iud(qry, val)
    return ''''<script>alert("successfully deleted");
           window.location='/viewparea'</script>'''


@app.route('/delpm', methods=['post', 'get'])
def delpm():
    eid = request.args.get('id')
    session['eid2'] = eid
    qry = "delete from manager where pm_id=%s"
    val = (eid)
    iud(qry, val)
    return ''''<script>alert("successfully deleted");
           window.location='/viewmanager'</script>'''


@app.route('/delstaff', methods=['post', 'get'])
def delstaff():
    eid = request.args.get('id')
    session['eid2'] = eid
    qry = "delete from staff where sid=%s"
    val = (eid)
    iud(qry, val)
    return ''''<script>alert("successfully deleted");
           window.location='/viewstaff'</script>'''


@app.route('/delslot', methods=['post', 'get'])
def delslot():
    sid = request.args.get('id')
    session['eid2'] = sid
    qry = "delete from slot where sid=%s"
    val = (sid)
    iud(qry, val)
    return ''''<script>alert("successfully deleted");
           window.location='/viewslot'</script>'''


app.run(debug=True)