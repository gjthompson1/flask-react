# app/api/models.py
import datetime

from flask import current_app

from app import db
from sqlalchemy import orm, ForeignKey

class Test(db.Model):
    __tablename__ = "test"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, name, created_at=datetime.datetime.utcnow()):
        self.name = name
        self.created_at = created_at
