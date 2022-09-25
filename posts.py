from db import db
import users

def get_list():
    #sql = "SELECT P.company, P.content, U.username, P.sent_at FROM posts P, users U WHERE P.user_id=U.id ORDER BY P.id"
    sqlall = "SELECT * FROM posts as P ORDER BY P.id"
    result = db.session.execute(sqlall)
    return result.fetchall()


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
    #print("companyid is now", companyid)

    sql = "INSERT INTO posts (company_id, companyname, content, user_id, posted_at) VALUES (:companyid, :company, :content, :user_id, NOW())"
    db.session.execute(sql, {"companyid":companyid, "company":company, "content":content, "user_id":user_id})
    db.session.commit()
    return True