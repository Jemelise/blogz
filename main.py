
from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:Unit2AssignmentBlogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

app.secret_key = "prtu3920fhsk57"

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.Text(500))
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))
 
    def __init__(self, title, content, owner):
        self.title = title
        self.content = content
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    blogs = db.relationship("Blog", backref="owner")

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login(): 
    allowed_routes = ["login", "blog_list", "index", "signup"]
    if request.endpoint not in allowed_routes and "user" not in session:
        return redirect("/login")  

@app.route("/signup", methods=["POST", "GET"])
def signup():

    username = ""
  
    username_error_message = ""
    password_error_message = ""
    verify_error_message = ""
    existing_username_error_message = ""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        verify = request.form["verify"]
        length_username = len(username)
        length_password = len(password)

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:  
            existing_username_error_message = "Username already exists" 

        elif not username:
            username_error_message = "*Incomplete form, enter username"

        elif length_username < 3:
            username_error_message = "Invalid username"

        if not password:
            password_error_message = "*Incomplete form, enter password"

        if length_password < 3:
            password_error_message = "Invalid password"    

        if not verify:
            verify_error_message = "*Incomplete form, verify password"     

        if password != verify:
            verify_error_message = "Passwords do not match"  

        if not existing_user and not username_error_message:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session["username"] = username
            return redirect("/newpost")                                     

    return render_template("signup.html", username_error_message=username_error_message, 
    password_error_message=password_error_message, verify_error_message=verify_error_message,
    username=username, existing_username_error_message=existing_username_error_message)    
   
@app.route("/login", methods=["POST", "GET"])
def login():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()

        if user.password != password:
            flash("Incorrect password")
            return redirect("/login")

        if user.password == password:
            session["user"] = username
            return redirect("/newpost")

    return render_template("login.html")        

@app.route("/")
def index():
    authors = User.query.all()
    return render_template("index.html", authors=authors)


@app.route("/logout")
def logout():
    del session["user"]
    return redirect("/blog")
#    session.pop('username', None)
#    return redirect("/blog")  

@app.route('/blog', methods=['GET'])
def blog_list():
  
    #if request.method == "GET":
    id=request.args.get("id")
    username=request.args.get("user")

    if id:
        blog=Blog.query.filter_by(id=id).first()
        author=User.query.filter_by(id=blog.owner_id).first()
        return render_template("blogpage.html", title=blog.title, content=blog.content, author=author)

    if username:
        author=User.query.filter_by(username=username).first()
        blogs=Blog.query.filter_by(owner_id=author.id).all()
        return render_template("singleuser.html", blogs=blogs, author=author)
    blogs = Blog.query.all()
    
    return render_template('blog.html',title="something blog",blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    title_error_message = ""
    content_error_message = ""
    blog_title = ""
    blog_content = ""

    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_content = request.form['blog_content']

        if not blog_title:   
            title_error_message = "please fill in title"

        if not blog_content:
            content_error_message = "please fill in content"    

        if not (title_error_message  + content_error_message):

            user = User.query.filter_by(username=session["user"]).first()
            new_blog = Blog(blog_title, blog_content, user)
            db.session.add(new_blog)
            db.session.commit()
            return redirect("/blog?id=" + str(new_blog.id)) 

    return render_template('newpost.html',title="Add Blog Entry", title_error_message=title_error_message,
    content_error_message=content_error_message, blog_title=blog_title, blog_content=blog_content)         

if __name__ == '__main__':
    app.run()
    