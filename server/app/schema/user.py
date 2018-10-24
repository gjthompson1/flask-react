from app import db

from .meta import Base

class User(Base):
    __tablename__ = 'user'

    name = db.Column(db.String)
    email = db.Column(db.String)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def to_dict(self):
        d = {}
        d['name'] = self.name
        d['email'] = self.email
        return d
