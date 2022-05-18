from flask import *
import os
from src.dbconnection import *
from werkzeug.utils import secure_filename

app= Flask(__name__)
app.secret_key="sdsd"

@app.route('/')
def main():
    return render_template('index.html')
@app.route('/logins')
def logins():
    return render_template('signin.html')
@app.route('/admin_home')
def admin_home():
    return render_template('dash.html')
@app.route('/manager_home')
def manager_home():
    return render_template('mdash.html')
@app.route('/parea',methods=['post'])
def parea():
    return  render_template('parkareaadd.html')
@app.route('/pmanager',methods=['post','get'])
def pmanager():
    qry="SELECT * FROM  `addarea`"
    res=selectall(qry)
    return  render_template('addmanager.html',val=res)



@app.route('/latilongi',methods=['post'])
def latilongi():
    return render_template('lati longi.html')
@app.route('/pstaff',methods=['post'])
def pstaff():
    return  render_template('addstaff.html')
@app.route('/uparea')
def uparea():
    areaid=request.args.get('id')
    session['areaid']=areaid
    qry="select * from addarea where aid=%s"
    val=(areaid)
    res=selectone(qry,val)
    return render_template("parkareaupdate.html",val=res)
@app.route('/upmanager')
def upmanager():
    mid=request.args.get('id')
    session['mid']=mid
    qry="select * from manager where pm_id=%s"
    qry2 = "select * from addarea"
    val=(mid)
    res=selectone(qry,val)
    res2=selectall(qry2)
    return render_template("managerupdate.html",val=res,data=res2)
@app.route('/upstaff')
def upstaff():
    mid=request.args.get('id')
    session['mid']=mid
    qry="select * from staff where sid=%s"
    val=(mid)
    res=selectone(qry,val)
    return render_template("updatestaff.html",val=res)



@app.route('/logincode',methods=['post'])
def logincode():
    uname=request.form['textfield']
    pswrd=request.form['textfield2']
    qry="select * from login where username=%s and password=%s"
    val=(uname,pswrd)
    result=selectone(qry,val)
    if result is None:
        return render_template('signin.html',a=-1)
    elif result[3]=="admin":
        return redirect('/admin_home')
    elif result[3]=="manager":
        return redirect('/manager_home')
    else:
        return ''''<script>alert("error");
                window.location='/logins'</script>'''
@app.route('/areaadd',methods=['post','get'])
def areaadd():
    name=request.form['textfield']
    place=request.form['textfield2']
    des=request.form['textarea']
    lat=request.form['lat']
    lon=request.form['lng']
    qry=" insert into addarea values(null,%s,%s,%s,%s,%s)"
    val=(name,place,des,lat,lon)
    iud(qry,val)
    return   ''''<script>alert("successfully added");
        window.location='/viewparea'</script>'''
@app.route('/manageradd',methods=['post','get'])
def manageradd():
    name=request.form['name']
    add=request.form['address']
    gender=request.form['gender']
    dob=request.form['dob']
    mail=request.form['mail']
    ph = request.form['phone']
    photo = request.files['photo']
    pic = secure_filename(photo.filename)
    photo.save(os.path.join('static', pic))
    arplace=request.form['area']
    qry=" insert into manager values(null,%s,%s,%s,%s,%s,%s,%s,%s)"
    qry2="insert into login values(null,%s,%s,'manager')"
    val2=(mail,dob)
    iud(qry2,val2)
    val=(name,add,gender,dob,mail,ph,pic,arplace)
    iud(qry,val)
    return   ''''<script>alert("successfully added");
        window.location='/viewmanager'</script>'''
@app.route('/upareacode',methods=['post'])
def upareacode():
    name = request.form['textfield']
    place = request.form['textfield2']
    des = request.form['textarea']
    lat = request.form['lat']
    lon = request.form['lng']
    qry2="UPDATE `addarea` SET `arname`=%s,`arplace`=%s,`desc`=%s,`latitude`=%s,`longitude`=%s WHERE `aid`=%s"
    val2=(name,place,des,lat,lon,session['areaid'])
    iud(qry2,val2)
    return ''''<script>alert("successfully updated");
        window.location='/viewparea'</script>'''
@app.route('/upmanagercode',methods=['post'])
def upmanagercode():
    name = request.form['name']
    add = request.form['address']
    gender = request.form['gender']
    dob = request.form['dob']
    mail = request.form['mail']
    ph = request.form['phone']
    photo = request.files['photo']
    pic = secure_filename(photo.filename)
    photo.save(os.path.join('static', pic))
    arplace = request.form['area']

    qry2="UPDATE `manager` SET `fullname`=%s,`address`=%s,`gender`=%s,`dob`=%s,`mail`=%s,`phone`=%s,`photo`=%s,`aid`=%s WHERE `pm_id`=%s"
    val2=(name,add,gender,dob,mail,ph,pic,arplace,session['mid'])
    iud(qry2,val2)
    return ''''<script>alert("successfully updated");
        window.location='/viewmanager'</script>'''
@app.route('/staffaddcode',methods=['post','get'])
def staffaddcode():
    name=request.form['name']
    add=request.form['address']
    gender=request.form['gender']
    dob=request.form['dob']
    mail=request.form['mail']
    ph = request.form['phone']
    photo = request.files['photo']
    pic = secure_filename(photo.filename)
    photo.save(os.path.join('static', pic))

    qry=" insert into staff values(null,%s,%s,%s,%s,%s,%s,%s)"
    qry2="insert into login values(null,%s,%s,'staff')"
    val2=(mail,dob)
    iud(qry2,val2)
    val=(name,add,gender,dob,mail,ph,pic)
    iud(qry,val)
    return   ''''<script>alert("successfully added");
        window.location='/viewstaff'</script>'''

@app.route('/upmanagercode',methods=['post'])
def upstaffcode():
    name = request.form['name']
    add = request.form['address']
    gender = request.form['gender']
    dob = request.form['dob']
    mail = request.form['mail']
    ph = request.form['phone']
    photo = request.files['photo']
    pic = secure_filename(photo.filename)
    photo.save(os.path.join('static', pic))

    qry2="UPDATE `staff` SET `fullname`=%s,`address`=%s,`gender`=%s,`dob`=%s,`mail`=%s,`phone`=%s,`photo`=%s WHERE `sid`=%s"
    val2=(name,add,gender,dob,mail,ph,pic,session['mid'])
    iud(qry2,val2)
    return ''''<script>alert("successfully updated");
        window.location='/viewstaff'</script>'''

@app.route('/viewparea',methods=['post','get'])
def viewparea():
    qry="select * from addarea "
    res=selectall(qry)
    return render_template('view.html', val=res)
@app.route('/viewmanager',methods=['post','get'])
def viewmanager():
    qry="SELECT manager.*,addarea.arname FROM  manager inner join addarea on manager.aid=addarea.aid "
    res=selectall(qry)
    return render_template('view_pmanager.html', val=res)
@app.route('/viewstaff',methods=['post','get'])
def viewstaff():
    qry="select * from staff "
    res=selectall(qry)
    return render_template('viewstaff.html', val=res)

@app.route('/delparea',methods=['post','get'])
def delparea():
    eid=request.args.get('id')
    session['eid2']=eid
    qry="delete from addarea where aid=%s"
    val=(eid)
    iud(qry,val)
    return ''''<script>alert("successfully deleted");
           window.location='/viewparea'</script>'''

@app.route('/delpm',methods=['post','get'])
def delpm():
    eid=request.args.get('id')
    session['eid2']=eid
    qry="delete from manager where pm_id=%s"
    val=(eid)
    iud(qry,val)
    return ''''<script>alert("successfully deleted");
           window.location='/viewmanager'</script>'''
def delstaff():
    eid=request.args.get('id')
    session['eid2']=eid
    qry="delete from staff where sid=%s"
    val=(eid)
    iud(qry,val)
    return ''''<script>alert("successfully deleted");
           window.location='/viewstaff'</script>'''

app.run(debug=True)