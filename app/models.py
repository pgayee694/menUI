from app import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    password = db.Column(db.String(128))
    location = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Restaurant(db.Model):
    __tablename__ = 'restaurant'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def __repr(self):
        return '<Restaurant {}>'.format(self.name)

class User_Restaurants(db.Model):
    __tablename__ = 'user_restaurants'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))

class Friends(db.Model):
    __tablename__ = 'friends'

    id = db.Column(db.Integer, primary_key=True)
    friend1_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    friend2_id = db.Column(db.Integer, db.ForeignKey('user.id'))