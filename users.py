from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
import secrets

def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = username
            session["is_admin"] = is_admin()
            session["csrf_token"] = secrets.token_hex(16)
            print("sessionadmin:", session["is_admin"], "userin is_admin()", is_admin())
            return True
        else:
            return False

def logout():
    del session["user_id"]
    del session["username"]
    del session["is_admin"]
    del session["csrf_token"]

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username,password) VALUES (:username,:password)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def user_id():
    return session.get("user_id",0)

def csrf_token_ok(token):
    return session["csrf_token"] == token

#def get_username():
#    uname = user_id()
#    sql = "SELECT username FROM users WHERE id = :uname"
#    result = db.session.execute(sql, {"uname":uname})
#    return result.fetchone()

def username():
    return session.get("username",0)


def is_admin():
    if not session:
        return False
    if session["username"]:
        username = session["username"]
    else:
        return False
    if username == 0 :
        return False
    sql = "SELECT 1 FROM admins WHERE username=:username AND active = TRUE"
    result = db.session.execute(sql, {"username":username})
    if result.fetchone():
        return True
    return False