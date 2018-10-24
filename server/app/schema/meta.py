from app import db

from datetime import datetime
from sqlalchemy import and_

class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        id = self.id if self.id else None
        return '<{} {}>'.format(self.__class__.__name__, id)

    def save(self, session=None):
        self.updated_at = datetime.utcnow()
        if not session:
            session = db.session
        session.add(self)

        return self

    def delete(self, force=False):
        db.session.delete(self)
