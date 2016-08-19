from app import db
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, UserMixin

lm = LoginManager(app)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    # interestingly, this creates an 'author' property on the 'post'
    # object. when we pass a User object to this author property,
    # the ORM figures out which user wrote the post
    # there MUST be a db.ForeignKey object pointing back at this object
    # for the relationship to be complete. That is to say -- there must
    # be a column in the class we're pointing to -- in this case, the Post
    # class, that includes a ForeignKey pointing back to some column in this
    # table. this does not create any fields in this table, but it provides
    # a convenience method for getting all of the items in the Post table that
    # are linked back to a given record in the User table
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % (self.nickname)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)
