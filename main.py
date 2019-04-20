# we gun build a blog bish
#BuildingBlogsBish = password for build-a-blog

from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:BuildingBlogsBish@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(500))

    def __init__(self, title, content):
        self.title = title
        self.content = content

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
        
            new_blog = Blog(blog_title, blog_content)
            db.session.add(new_blog)
            db.session.commit()
            return redirect("/blog?id=" + str(new_blog.id))

    return render_template('newpost.html',title="Add Blog Entry", title_error_message=title_error_message,
    content_error_message=content_error_message, blog_title=blog_title, blog_content=blog_content)        

if __name__ == '__main__':
    app.run()
    