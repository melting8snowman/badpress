from app import app
from flask import render_template, request, redirect
import posts, users



# initial
@app.route("/")
def index():
    list = posts.get_list()
    return render_template("index.html", count=len(list), posts=list)

# add post
@app.route("/new_entry")
def new():
    return render_template("new_entry.html")

@app.route("/send", methods=["POST"])
def send():
    company = request.form["company"]
    content = request.form["content"]

    if posts.send(company, content):
        return redirect("/")
    else:
        return render_template("error.html", message="An error occurred while trying to add post. Please try again.")

#search
@app.route("/search")
def search():
    query = request.args["query"]
    sql = "SELECT id, company_id, content, user_id, posted_at FROM posts WHERE company LIKE :query"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    posts = result.fetchall()
    return render_template("results.html", posts=posts, company=company)

## Users 
#login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Wrong username or password")

#logout
@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

#register new user
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Please use same passwords")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Registration unsuccessful")