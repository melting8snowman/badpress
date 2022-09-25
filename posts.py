from db import db
import users

def get_list():
    #sql = "SELECT P.content, U.username, P.sent_at FROM posts P, users U WHERE P.user_id=U.id ORDER BY P.id"
    sqlall = "SELECT * FROM posts as P ORDER BY P.id"
    result = db.session.execute(sqlall)
    return result.fetchall()

def send(content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    
    sql = "INSERT INTO posts (content, user_id, posted_at) VALUES (:content, :user_id, NOW())"
    db.session.execute(sql, {"content":content, "user_id":user_id})
    db.session.commit()
    return True