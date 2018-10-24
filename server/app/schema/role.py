from app import db

from .meta import Base

class Role(Base):
    __tablename__ = 'role'

    type = db.Column(db.String)

    def to_dict(self):
        d = {}
        d['type'] = self.type
        return d
