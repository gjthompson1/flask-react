# manage.py

import unittest

from flask_script import Manager
from flask_cors import CORS

from app import create_app, db
from app.api.models import Test

app = create_app()
manager = Manager(app)

@manager.command
def recreate_db():
    """Recreates a database."""
    db.drop_all()
    db.create_all()
    db.session.commit()

@manager.command
def seed_db():
    """Seeds the database."""
    db.session.add(Test(
        name='test',
    ))
    db.session.commit()

if __name__ == '__main__':
    manager.run()
