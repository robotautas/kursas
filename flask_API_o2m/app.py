import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import ModelSchema


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfgsfdgsdfgsdfgsdf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'paskaitos.db?check_same_thread=False')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.String)
    
    def __repr__(self):
        return self.name

    

# class UserSchema(ma.SQLAlchemySchema):
#     class Meta:
#         model = User
#     id = ma.auto_field()
#     name = ma.auto_field()
#     posts = ma.auto_field()
    


# user_schema = UserSchema()
# users_schema = UserSchema(many=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column('title', db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", backref='posts')


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
    id = ma.auto_field()
    name = ma.auto_field()
    posts = ma.auto_field()
    


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        include_fk = True

post_schema = PostSchema()
posts_schema = PostSchema(many=True)

#sukurti user

@app.route('/create_user', methods=['POST'])
def create_user():
    name = request.json['name']
    new_user = User(name=name)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)

@app.route('/create_post', methods=['POST'])
def create_post():
    title = request.json['title']
    user = request.json['user']
    user_object = User.query.filter_by(name=user).one()
    print(user, user_object.id)
    new_post = Post(title=title, user_id=user_object.id)
    db.session.add(new_post)
    db.session.commit()
    return post_schema.jsonify(new_post)

@app.route('/users', methods=['GET'])
def users():
    all_users = User.query.all()
    res = users_schema.dump(all_users)
    return jsonify(res)

@app.route('/posts', methods=['GET'])
def posts():
    posts = Post.query.all()
    res = posts_schema.dump(posts)
    return jsonify(res)

@app.route('/update_user/<int:id>', methods=['PUT'])
def update_user(id):
    updated_user = User.query.get(id)
    updated_user.name = request.json['name']
    db.session.commit()
    return user_schema.jsonify(updated_user)

@app.route('/update_post/<int:id>', methods=['PUT'])
def update_post(id):
    updated_post = Post.query.get(id)
    updated_post.title = request.json['title']
    user = request.json['user']
    user_object = User.query.filter_by(name=user).one()
    updated_post.user_id = user_object.id
    db.session.commit()
    return post_schema.jsonify(updated_post)

@app.route('/delete_user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)


@app.route('/delete_post/<int:id>', methods=['DELETE'])
def delete_post(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return post_schema.jsonify(post)

@app.route('/posts/<int:id>', methods=['GET'])
def single_post(id):
    post = Post.query.get(id)
    return post_schema.jsonify(post)

@app.route('/users/<int:id>', methods=['GET'])
def single_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)


if __name__ == '__main__':
    app.run('127.0.0.1', port=5000, debug=True)