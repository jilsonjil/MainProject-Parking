from flask import *

from src.dbconnection import *

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
@app.route('/parea',methods=['post'])
def parea():
    return  render_template('parkareaadd.html')
@app.route('/uparea')
def uparea():
    areaid=request.args.get('id')
    session['areaid']=areaid
    qry="select * from addarea where aid=%s"
    val=(areaid)
    res=selectone(qry,val)
    return render_template("parkareaupdate.html",val=res)


@app.route('/logincode',methods=['post'])
def logincode():
    uname=request.form['textfield']
    pswrd=request.form['textfield2']
    qry="select * from login where username=%s and password=%s"
    val=(uname,pswrd)
    result=selectone(qry,val)
    print(result)
    if result is None:
        return render_template('/signin.html',a=-1)
    else:
        return redirect('/admin_home')
@app.route('/areaadd',methods=['post','get'])
def areaadd():
    name=request.form['textfield']
    place=request.form['textfield2']
    des=request.form['textarea']
    lat=request.form['textfield3']
    lon=request.form['textfield4']
    qry=" insert into addarea values(null,%s,%s,%s,%s,%s)"
    val=(name,place,des,lat,lon)
    iud(qry,val)
    return   ''''<script>alert("successfully added");
        window.location='/viewparea'</script>'''
@app.route('/upareacode',methods=['post'])
def upareacode():
    name = request.form['textfield']
    place = request.form['textfield2']
    des = request.form['textarea']
    lat = request.form['textfield3']
    lon = request.form['textfield4']
    qry2="UPDATE `addarea` SET `arname`=%s,`arplace`=%s,`desc`=%s,`latitude`=%s,`longitude`=%s WHERE `aid`=%s"
    val2=(name,place,des,lat,lon,session['areaid'])
    iud(qry2,val2)
    return ''''<script>alert("successfully updated");
        window.location='/viewparea'</script>'''


@app.route('/viewparea',methods=['post','get'])
def viewparea():
    qry="select * from addarea "
    res=selectall(qry)
    return render_template('view.html', val=res)

@app.route('/delparea',methods=['post','get'])
def delparea():
    eid=request.args.get('id')
    session['eid2']=eid
    qry="delete from addarea where aid=%s"
    val=(eid)
    iud(qry,val)
    return ''''<script>alert("successfully deleted");
           window.location='/viewparea'</script>'''


    return render_template('viewarea.html',val=res)
app.run(debug=True)