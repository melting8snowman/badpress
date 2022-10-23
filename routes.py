from app import app
from flask import session, render_template, request, redirect, abort, redirect
import posts, users



# initial
@app.route("/")
def index():
    list = posts.get_list()
    username = users.username()
    searched = bool(False)
    return render_template("index.html", count=len(list), posts=list, username=username, searched=searched)

# add post
@app.route("/new_entry")
def new():
    return render_template("new_entry.html")

@app.route("/send", methods=["POST"])
def send():
    # csrf security check
    if not users.csrf_token_ok(request.form["csrf_token"]):
        abort(403)
    # proceed with adding to db
    company = request.form["company"]
    content = request.form["content"]
    if (len(company) == 0 | len(content) == 0):
        return render_template("error.html", error="Please enter both company name and badpress", previous="/new_entry")
    if len(company) > 100:
        return render_template("error.html", error="Please use a shorter company name", previous="/new_entry")
    if len(content) > 5000:
        return render_template("error.html", error="Maximum badpress length is 5000 characters", previous="/new_entry")

    if posts.send(company, content):
        return redirect("/")
    else:
        return render_template("error.html", message="An error occurred while trying to add post. Please try again.", previous="/new_entry")

#search
@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/results")
def results():
    query = request.args["query"]
    rowcount, list = posts.get_comp_list(query)
    username = users.username()
    if rowcount == 0:
        return render_template("error.html", message="No data found. Please try again with another search item.", previous="/search")
    else:
        searched = bool(True)
        return render_template("index.html", count=len(list), posts=list, username=username, searched=searched, company=query)

# filter for user´s own reviews
@app.route("/filterown")
def filterown():
    username = users.username()
    userid = users.user_id()
    list = posts.get_own(userid)
    searched = bool(True)
    return render_template("index.html", count=len(list), posts=list, username=username, searched=searched)

#Individual view / currently not used, maybe will be available later
@app.route("/postview/<int:id>")
def postview(id):
    data = posts.get_single(id)
    return render_template("postview.html", company=data[2], content=data[3])

#Add Like
@app.route("/addlike/<int:id>")
def addlike(id):
    posts.add_like(id)
    return redirect("/")

#DisLike
@app.route("/dislike/<int:id>")
def dislike(id):
    posts.remove_like(id)
    return redirect("/")

## For Admin
# Toggle visibility of post
@app.route("/togglevisibility/<int:id>")
def togglevisibility(id):
    posts.toggle_visibility(id)
    return redirect("/")

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
            return render_template("error.html", message="Wrong username or password", previous="/login")

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
            return render_template("error.html", message="Registration unsuccessful", previous="/register")