from db import db
import users

def get_list():
    #sql = "SELECT P.company, P.content, U.username, P.sent_at FROM posts P, users U WHERE P.user_id=U.id ORDER BY P.id"
    sqlall = "SELECT id, company_id, companyname, content, user_id, posted_at FROM posts ORDER BY company_id"
    result = db.session.execute(sqlall)
    return result.fetchall()

def get_comp_list(query):
    print("searching for", query)
    sql = "SELECT id, company_id, companyname, content, user_id, posted_at FROM posts WHERE companyname LIKE :query"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    list = result.fetchall()
    rowcount = len(list)    
    return rowcount, list

def send(company, content):
    company = company.lower()
    user_id = users.user_id()
    if user_id == 0:
        return False
    #sql_check = "SELECT company_id FROM companies WHERE EXISTS (SELECT * FROM companies where companyname LIKE :company)"
    sql_check = "SELECT company_id FROM companies WHERE companyname LIKE :company"
    result = db.session.execute(sql_check, {"company":company})
    
    num_result = result.rowcount
    if int(num_result) == 0:  
        sqlinsert = "INSERT INTO companies (companyname) VALUES (:company)"
        db.session.execute(sqlinsert, {"company":company})
        db.session.commit()
        result = db.session.execute(sql_check, {"company":company})
    
    companyid = result.fetchone()[0]

    sql = "INSERT INTO posts (company_id, companyname, content, user_id, posted_at) VALUES (:companyid, :company, :content, :user_id, NOW())"
    db.session.execute(sql, {"companyid":companyid, "company":company, "content":content, "user_id":user_id})
    db.session.commit()
    return True