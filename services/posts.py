from db import db
import services.users as users

def get_list():
    if users.is_admin(): 
        sql = """SELECT p.id, p.company_id, c.companyname, p.content, p.user_id, p.posted_at, a.likes, a.nonlikes, p.visible 
               FROM posts p 
               LEFT JOIN alikes a ON p.id = a.post_id
               LEFT JOIN companies c ON p.company_id = c.company_id
               ORDER BY p.id ASC"""
    else:
        sql = """SELECT p.id, p.company_id, c.companyname, p.content, p.user_id, p.posted_at, a.likes, a.nonlikes, p.visible 
               FROM posts p 
               LEFT JOIN alikes a ON p.id = a.post_id
               LEFT JOIN companies c ON p.company_id = c.company_id
               WHERE p.visible = true 
               ORDER BY likes DESC, posted_at ASC"""
    result = db.session.execute(sql)
    return result.fetchall()

def get_own(user_id):
    if users.is_admin(): 
        sql = """SELECT p.id, p.company_id, c.companyname, p.content, p.user_id, p.posted_at, a.likes, a.nonlikes, p.visible 
               FROM posts p 
               LEFT JOIN alikes a ON p.id = a.post_id
               LEFT JOIN companies c ON p.company_id = c.company_id
               WHERE p.user_id = :user_id
               ORDER BY p.id ASC"""
    else:
        sql = """SELECT p.id, p.company_id, c.companyname, p.content, p.user_id, p.posted_at, a.likes, a.nonlikes, p.visible 
               FROM posts p 
               LEFT JOIN alikes a ON p.id = a.post_id
               LEFT JOIN companies c ON p.company_id = c.company_id
               WHERE p.user_id = :user_id AND p.visible = TRUE 
               ORDER BY likes DESC, posted_at ASC"""
    
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()


def get_comp_list(query):
    if users.is_admin(): 
        sql = """SELECT p.id, p.company_id, c.companyname, p.content, p.user_id, p.posted_at, a.likes, a.nonlikes, p.visible 
               FROM companies c 
               LEFT JOIN posts p ON c.company_id = p.company_id
               INNER JOIN alikes a ON p.id = a.post_id   
               WHERE c.companyname LIKE :query 
               ORDER BY p.id ASC"""
    else:
        sql = """SELECT p.id, p.company_id, c.companyname, p.content, p.user_id, p.posted_at, a.likes, a.nonlikes, p.visible 
               FROM companies c 
               LEFT JOIN posts p ON c.company_id = p.company_id
               INNER JOIN alikes a ON p.id = a.post_id   
               WHERE c.companyname LIKE :query AND p.visible = TRUE 
               ORDER BY likes DESC, posted_at ASC"""
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    list = result.fetchall()
    rowcount = len(list)    
    return rowcount, list

def send(company, content):
    
    company = company.lower()
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql_check = "SELECT company_id FROM companies WHERE companyname LIKE :company"
    result = db.session.execute(sql_check, {"company":company})
    num_result = result.rowcount
    if int(num_result) == 0:  
        #Create company
        sqlinsert = "INSERT INTO companies (companyname, visible) VALUES (:company, TRUE)"
        db.session.execute(sqlinsert, {"company":company})
        db.session.commit()
        result = db.session.execute(sql_check, {"company":company})
    
    companyid = result.fetchone()[0]
    # create post
    sql = "INSERT INTO posts (company_id, companyname, content, user_id, posted_at, visible) VALUES (:companyid, :company, :content, :user_id, NOW(), TRUE)"
    db.session.execute(sql, {"companyid":companyid, "company":company, "content":content, "user_id":user_id})
    db.session.commit()
    # initialize alikes
    sql = "INSERT INTO alikes (likes, nonlikes) VALUES (0, 0)"
    db.session.execute(sql)
    db.session.commit()
    return True

def add_like(id):
    if id == 0:
        return False
    sql = "UPDATE alikes SET likes = likes +1 where post_id = :id"
    result = db.session.execute(sql, {"id":id})
    db.session.commit()
    return True

def dislike(id):
    if id == 0:
        return False
    sql = "UPDATE alikes SET nonlikes = nonlikes -1 where post_id = :id"
    result = db.session.execute(sql, {"id":id})
    db.session.commit()
    return True

def toggle_visibility(id):
    if id == 0:
        return False
    sqlfind = "SELECT visible FROM posts WHERE id = :id LIMIT 1"
    result = db.session.execute(sqlfind, {"id":id})
    print("visible:" ,result)
    num_result = result.rowcount
    if int(num_result) == 0:  
        return False
    else:
        # set visible to opposite
        sql = "UPDATE posts SET visible = NOT visible where id = :id"
        result = db.session.execute(sql, {"id":id})
        db.session.commit()
        return True
 