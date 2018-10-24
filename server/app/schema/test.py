import sqlite3
import pandas as pd
from hamilton.app import db, constants as c
from hamilton.app.utils.types import EnumType

from .meta import Base

class Test(Base):
    __tablename__ = 'test'

    name = db.Column(db.String)

    def __init__(self, name):
        self.name = name
