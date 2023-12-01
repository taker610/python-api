from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
#import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#basedir = os.path.abspath(os.path.dirname(__file__))
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://lxctgcxqqgogle:d8348ea5a21e37b22d34b6459ed6c8862abb283f4cdee8ab4f03fd702f6ab747@ec2-52-206-38-187.compute-1.amazonaws.com:5432/d3pgbges6bt8l0'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://jafjilbllqlkym:2917c8ddd24c8cace3eea776165605b1c45f4a4592a4779e7c17f19acabb4534@ec2-44-206-204-65.compute-1.amazonaws.com:5432/db8k0g41shj1bl'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), unique=False)
    author = db.Column(db.String(100), unique=False)
    title = db.Column(db.String(100), unique=False)
    content = db.Column(db.String(1000), unique=False)

    def __init__(self, category, author, title, content):
       self.category = category
       self.author = author
       self.title = title
       self.content = content 
       

class BlogSchema(ma.Schema):
    class Meta:
        fields = ('id','category', 'author', 'title', 'content')

blog_schema = BlogSchema()
blogs_schema = BlogSchema(many=True)

#Endpoint to create a new blog
@app.route('/blog', methods=['POST'])
def add_Blog():
    category = request.json['category']
    author = request.json['author']
    title = request.json['title']
    content = request.json['content']

    new_blog = Blog(category, author, title, content)

    db.session.add(new_blog)
    db.session.commit()

    blog = Blog.query.get(new_blog.id)

    return blog_schema.jsonify(blog)

# Endpoint to query all blogs
@app.route('/blogs', methods=['GET'])
def get_blogs():
    all_blogs = Blog.query.all()
    result = blogs_schema.dump(all_blogs)
    return jsonify(result)

# Endpoint to query a single blog
@app.route('/blog/<id>', methods=["GET"])
def get_blog(id):
    blog = Blog.query.get(id)
    return blog_schema.jsonify(blog)

# Endpoint for updating a blog
@app.route("/blog/<id>", methods=["PUT"])
def blog_update(id):
    blog = Blog.query.get(id)
    category = request.json['category']
    author = request.json['author']
    title = request.json['title']
    content = request.json["content"]

    blog.category = category
    blog.author = author
    blog.title = title
    blog.content = content

    db.session.commit()
    return blog_schema.jsonify(blog)

# Endpoint for deleting a blog
@app.route('/blog/<id>', methods=['DELETE'])
def blog_delete(id):
    blog = db.session.query(Blog).filter(Blog.id == id).first()
    db.session.delete(blog)
    db.session.commit()

    return blog_schema.jsonify(blog)

if __name__ == "__main__":
    app.run(debug=True)
