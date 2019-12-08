from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(64), index=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password_passed):
        return check_password_hash(self.password, password_passed)

    def check_username(self, user_passed):
        return user_passed == self.username

class Restaurant(db.Model):
    __tablename__ = 'restaurant'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)

    def __repr(self):
        return '<Restaurant {}>'.format(self.name)

class UserRestaurant(db.Model):
    __tablename__ = 'user_restaurant'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)

class Friends(db.Model):
    __tablename__ = 'friends'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    friend1_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    friend2_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Location(db.Model):
    __tablename__ = 'location'

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(64), nullable=False)
    region = db.Column(db.String(64), nullable=False)
    country = db.Column(db.String(64), nullable=False)
