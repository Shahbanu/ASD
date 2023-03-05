from flask import Flask, render_template, request, redirect, session, jsonify
from DBConnection import Db

app = Flask(__name__)
app.secret_key="hi"

status_path=r"D:\ASWIN\2022-2023 workspace\LBS\Autism_spectrum_disorder\static\\"


@app.route('/')
def login():
    return render_template("login_temp.html")
    # return render_template("login.html")



@app.route("/login_post", methods=['post'])
def login_post():
    username=request.form['textfield']
    password=request.form['textfield2']
    db=Db()
    res=db.selectOne("SELECT * FROM login WHERE username='"+username+"' AND PASSWORD='"+password+"'")
    if res is not None:
        if res['usertype']=="admin":
            session['lg']="yes"
            return redirect("/admin_home")
        else:
            return "<script>alert('Unauthorised user');window.location='/';</script>"
    else:
        return "<script>alert('Invalid Details');window.location='/';</script>"


@app.route("/logout")
def logout():
    session['lg']=""
    return "<script>alert('Logged out');window.location='/';</script>"

######              ADMIN
@app.route("/admin_home")
def admin_home():
    if session['lg']!='yes':
        return "<script>alert('You are logged out');window.location='/';</script>"
    return render_template("admin/admin_index.html")
    # return render_template("admin/home.html")

@app.route("/admin_add_notif")
def admin_add_notif():
    if session['lg']!='yes':
        return "<script>alert('You are logged out');window.location='/';</script>"
    return render_template("admin/add_notification.html")

@app.route("/admin_add_notif_post", methods=['post'])
def admin_add_notif_post():
    title=request.form['textfield']
    content=request.form['textarea']
    db=Db()
    db.insert("INSERT INTO `notification`(DATE, title, content) VALUES(CURDATE(), '"+title+"', '"+content+"')")
    return "<script>alert('Notification Added');window.location='/admin_add_notif';</script>"

@app.route("/admin_view_notification")
def admin_view_notification():
    if session['lg']!='yes':
        return "<script>alert('You are logged out');window.location='/';</script>"
    db=Db()
    res=db.select("select * from notification")
    return render_template("admin/view_notification.html", data=res)

@app.route("/admin_delete_notification/<nid>")
def admin_delete_notification(nid):
    if session['lg']!='yes':
        return "<script>alert('You are logged out');window.location='/';</script>"
    db=Db()
    db.delete("delete from notification where notification_id='"+nid+"'")
    return redirect("/admin_view_notification")


@app.route("/admin_add_activities")
def admin_add_activities():
    if session['lg']!='yes':
        return "<script>alert('You are logged out');window.location='/';</script>"
    return render_template("admin/add_activities.html")


@app.route("/admin_add_activities_post", methods=['post'])
def admin_add_activities_post():
    name = request.form['textfield']
    description = request.form['textarea']
    db = Db()
    db.insert("INSERT INTO `activities`(activity_name, description) VALUES('"+name+"', '"+description+"')")
    return "<script>alert('Notification Added');window.location='/admin_add_activities';</script>"

@app.route("/admin_view_activities")
def admin_view_activities():
    if session['lg']!='yes':
        return "<script>alert('You are logged out');window.location='/';</script>"
    db=Db()
    res=db.select("select * from activities")
    return render_template("admin/view_activities.html", data=res)

@app.route("/admin_delete_activities/<aid>")
def admin_delete_activities(aid):
    if session['lg']!='yes':
        return "<script>alert('You are logged out');window.location='/';</script>"
    db=Db()
    db.delete("delete from activities where activity_id='"+aid+"'")
    return  redirect("/admin_view_activities")


@app.route("/admin_view_users")
def admin_view_users():
    if session['lg']!='yes':
        return "<script>alert('You are logged out');window.location='/';</script>"
    db=Db()
    res=db.select("select * from users")
    return render_template("admin/view_users.html", data=res)


@app.route("/admin_view_complaints")
def admin_view_complaints():
    if session['lg']!='yes':
        return "<script>alert('You are logged out');window.location='/';</script>"
    db=Db()
    res=db.select("select * from complaints, users where complaints.user_id=users.user_id and complaints.reply='pending'")
    return render_template("admin/view_complaints.html", data=res)

@app.route("/send_reply/<id>")
def send_reply(id):
    if session['lg']!='yes':
        return "<script>alert('You are logged out');window.location='/';</script>"
    return render_template("admin/send_reply.html", id=id)

@app.route("/send_reply_post", methods=['post'])
def send_reply_post():
    id=request.form['hid']
    reply=request.form['textarea']
    db=Db()
    db.update("update complaints set reply='"+reply+"' where complaint_id='"+id+"'")
    return "<script>alert('Reply sent');window.location='/admin_view_complaints';</script>"


@app.route("/admin_change_password")
def admin_change_password():
    if session['lg']!='yes':
        return "<script>alert('You are logged out');window.location='/';</script>"
    return render_template("admin/change_password.html")

@app.route("/admin_change_password_post", methods=['post'])
def admin_change_password_post():
    psw=request.form['textfield']
    npsw=request.form['textfield2']
    db=Db()
    res=db.selectOne("select * from login where password='"+psw+"' and usertype='admin'")
    if res is None:
        return "<script>alert('Incorrect password');window.location='/admin_change_password';</script>"
    else:
        db.update("update login set password='"+npsw+"' where login_id='"+str(res['login_id'])+"'")
        return "<script>alert('Password Changed');window.location='/admin_change_password';</script>"



#################               android
@app.route("/user_reg", methods=['post'])
def user_reg():
    name=request.form['Name']
    hname=request.form['Hname']
    place=request.form['Place']
    pin=request.form['Pin']
    phn=request.form['Phone']
    email=request.form['Email']
    pswd=request.form['Password']
    img=request.form['Img']
    db=Db()
    res=db.selectOne("SELECT * FROM `login` WHERE username='"+email+"'")
    if res is not None:
        return jsonify(status="Already Exist")
    else:
        import time
        import base64
        timestr = time.strftime("%Y%m%d-%H%M%S")
        print(timestr)
        a = base64.b64decode(img)
        fh = open(status_path + "user_img\\" + timestr + ".jpg", "wb")
        path = "/static/user_img/" + timestr + ".jpg"
        fh.write(a)
        fh.close()

        db=Db()
        lid=db.insert("INSERT INTO login(username, PASSWORD, usertype) VALUES('"+email+"', '"+pswd+"', 'user')")
        db.insert("INSERT INTO users(NAME, email, phone, image, house, place, pin) VALUES('"+name+"', '"+email+"', '"+phn+"', '"+path+"', '"+hname+"', '"+place+"', '"+pin+"')")
        return jsonify(status="ok")

@app.route("/user_login", methods=['post'])
def user_login():
    username=request.form['u']
    password=request.form['p']
    db=Db()
    res=db.selectOne("SELECT * FROM login WHERE username='"+username+"' AND PASSWORD='"+password+"'")
    if res is None:
        return jsonify(status="no")
    else:
        if res['usertype']=="user":
            return jsonify(status="ok", lid=res['login_id'])
        else:
            return jsonify(status="no")


@app.route("/and_view_notifications", methods=['post'])
def and_view_notifications():
    db=Db()
    res=db.select("SELECT * FROM `notification` ORDER BY notification_id DESC")
    if len(res) > 0:
        return jsonify(status="ok", data=res)
    else:
        return jsonify(status="no")


@app.route("/and_view_activities", methods=['post'])
def and_view_activities():
    db=Db()
    res=db.select("SELECT * FROM `activities` ORDER BY activity_id DESC")
    if len(res) > 0:
        return jsonify(status="ok", data=res)
    else:
        return jsonify(status="no")

@app.route("/and_view_reply", methods=['post'])
def and_view_reply():
    lid=request.form['lid']
    db=Db()
    res=db.select("SELECT * FROM `complaints` where user_id='"+lid+"' order by complaint_id desc")
    if len(res) > 0:
        return jsonify(status="ok", data=res)
    else:
        return jsonify(status="no")

@app.route("/and_delete_complaint", methods=['post'])
def and_delete_complaint():
    cid=request.form['cid']
    db=Db()
    db.delete("delete FROM `complaints` where complaint_id='"+cid+"'")
    return jsonify(status="ok")

@app.route("/and_send_complaint", methods=['post'])
def and_send_complaint():
    lid=request.form['lid']
    comp=request.form['comp']
    db=Db()
    db.insert("INSERT INTO complaints(user_id, DATE, complaint, reply) VALUES('"+lid+"', CURDATE(), '"+comp+"', 'pending')")
    return jsonify(status="ok")

@app.route("/and_change_password", methods=['post'])
def and_change_password():
    lid=request.form['lid']
    psw=request.form['psw']
    db=Db()
    db.update("UPDATE login SET PASSWORD='"+psw+"' WHERE login_id='"+lid+"'")
    return jsonify(status="ok")

@app.route("/and_prediction", methods=['post'])
def and_prediction():
    feats=request.form['feats']
    features=feats.split("#")
    print(features)
    features.pop(0)
    from check import autism_pred
    obj=autism_pred()
    res=obj.predict(features)
    return jsonify(status="ok", res=res)

@app.route("/aa")
def aa():
    return render_template("admin/admin_index1.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0")
