from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    """connects db to app"""
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = "users"

    def __repr__(self):
        u = self
        return f'<User{u.id}{u.username}'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(15), nullable=False)
    last_name = db.Column(db.String(15), nullable=False) 
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(15), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    recipes =db.relationship("Recipes", backref="users")

    @classmethod
    def register (cls, first_name,last_name, email, username, pwd):
        hashed= bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode("utf8")

        user = User(
            first_name=first_name,
            last_name = last_name, 
            username=username,
            email=email,
            password=hashed_utf8,
        
        )

        db.session.add(user)
        return user
    
        
    
    @classmethod
    def authenticate(cls,username, password):
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password,password):
            return user
        else:
            return False 


class Recipes(db.Model):
    __tablename__ = "faved_recipes"

    def __repr__(self):
        r = self
        return f'<Recipes{r.id}{r.title}{r.recipe_id}{r.user_id}'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id= db.Column(db.Integer, nullable=False)
    title= db.Column(db.String, nullable=False)
    image= db.Column(db.String)
    user_id= db.Column(db.Integer, db.ForeignKey("users.id",ondelete="CASCADE"))
    



