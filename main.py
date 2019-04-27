
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
    content = db.Column(db.Text(500)) ## could be text instead
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, title, content, owner):
        self.title = title
        self.content = content
        self.owner = owner
        
# ## todo for blogz
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    blogs = db.relationship("Blog", backref="owner")

    def __init__(self, username, password):
        self.username = username
        self.password = password

     
@app.route("/signup")
def signup():
   
    return render_template("signup.html")
#
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
            session["user"] = user.username
            return redirect("/newpost")
    return render_template("login.html")        
# #
# @app.route("/index")
# def indexdup():

# #
# @app.route("/logout")
# def logout():
#     session.pop('username', None)
#     return redirect("/blog")  


@app.route('/blog', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blog_name = request.form['blog']
        new_blog = Blog(blog_name)
        db.session.add(new_blog)
        db.session.commit()
    
    if request.method == "GET":
        id=request.args.get("id")
        if id:
            blog=Blog.query.filter_by(id=id).first()
            return render_template("blogpage.html", title=blog.title, content=blog.content)

    blogs = Blog.query.all()
    
    return render_template('index.html',title="something blog",blogs=blogs)

# todo new parameter to consider with the relationship
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
    