"""Database models."""
from flag import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from time import time
import datetime
import jwt # pip install flask-jwt
from flask import current_app as app
from sqlalchemy.sql import func

class User(UserMixin, db.Model):
    """Model for user accounts."""

    __tablename__ = 'flagusers'

    id = db.Column(db.Integer,
                   primary_key=True)
    firstName = db.Column(db.String,
                     nullable=False,
                     unique=False)
    lastName = db.Column(db.String,
                     nullable=False,
                     unique=False)
    email = db.Column(db.String(40),
                      unique=True,
                      nullable=False)
    password = db.Column(db.String(200),
                         primary_key=False,
                         unique=False,
                         nullable=False)
    phone = db.Column(db.String(15),
                        index=False,
                        unique=False,
                        nullable=True)
    website = db.Column(db.String(150),
                        index=False,
                        unique=False,
                        nullable=True)                    
    userRole = db.Column(db.String(1),
                        index=False,
                        unique=False,
                        nullable=False)
    created_On = db.Column(db.DateTime,
                           index=False,
                           unique=False,
                           nullable=False,
                           default=datetime.datetime.now)
    last_login = db.Column(db.DateTime,
                           index=False,
                           unique=False,
                           nullable=True)
    memberStartDate = db.Column(db.DateTime,
                           index=False,
                           unique=False,
                           nullable=True)
    memberExpireDate = db.Column(db.DateTime,
                           index=False,
                           unique=False,
                           nullable=True)
    

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def get_reset_password_token(self, expires_in=60*60*24): # token expires in 1 day
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)