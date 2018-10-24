# manage.py

import unittest

from flask_script import Manager
from flask_cors import CORS

from app import create_app, db
from app.schema import User, Role

app = create_app()
manager = Manager(app)

@manager.command
def seed_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

    user = User('test', 'test@test.com')
    user.save()

    role = Role()
    role.type = 'admin'
    role.save()

    db.session.commit()

if __name__ == '__main__':
    manager.run()
