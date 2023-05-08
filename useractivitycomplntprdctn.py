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
