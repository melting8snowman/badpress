from db import db
import users

def get_list():
    if users.is_admin(): 
        sql = "SELECT id, company_id, companyname, content, user_id, posted_at, likes, visible FROM posts ORDER BY id ASC"
    else:
        sql = "SELECT id, company_id, companyname, content, user_id, posted_at, likes FROM posts WHERE visible = TRUE ORDER BY likes DESC"
    result = db.session.execute(sql)
    return result.fetchall()

def get_own(user_id):
    if users.is_admin(): 
        sql = "SELECT id, company_id, companyname, content, user_id, posted_at, likes, visible FROM posts WHERE user_id = :user_id ORDER BY ID ASC"
    else:
        sql = "SELECT id, company_id, companyname, content, user_id, posted_at, likes FROM posts WHERE user_id = :user_id AND visible = TRUE ORDER BY posted_at DESC"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()


def get_comp_list(query):
    if users.is_admin(): 
        sql = "SELECT id, company_id, companyname, content, user_id, posted_at, visible, likes FROM posts WHERE companyname LIKE :query"
    else:
        sql = "SELECT id, company_id, companyname, content, user_id, posted_at, visible, likes FROM posts WHERE companyname LIKE :query AND visible = TRUE"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    list = result.fetchall()
    rowcount = len(list)    
    return rowcount, list

def get_single(id):
    print("IDnyt:", id)
    if users.is_admin(): 
        sql = "SELECT id, company_id, companyname, content, user_id, posted_at, likes, visible FROM posts WHERE id = :id LIMIT 1"
    else:
        sql = "SELECT id, company_id, companyname, content, user_id, posted_at, likes, visible FROM posts WHERE id = :id AND visible = TRUE LIMIT 1"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

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
    return True

def add_like(id):
    if id == 0:
        return False
    sql = "UPDATE posts SET likes = likes +1 where id = :id"
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
 