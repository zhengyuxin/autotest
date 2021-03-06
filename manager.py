# -*- coding: utf-8 -*-
"""
    manager.py
    ~~~~~~~~~~~

    flask manager script

    :copyright: (c) 2013.
    :license: BSD, see LICENSE for more details.
"""
from flask.ext.script import Server, Manager, prompt_bool
from autotest.application import setup_app
from autotest.extensions import db
from autotest.models.users import User
import uuid

manager = Manager(setup_app())
manager.add_command("runserver", Server('0.0.0.0', port=5000))


@manager.option('-r', '--role', dest='role', default="member")
def createuse(role):
    user = User()
    info = unicode(uuid.uuid4())
    user.username, user.email, user.password = info.split('-')[:3]
    user.email = user.email + u"@autotest.com"
    password = info.split('-')[2]
    if role == "admin":
        user.role = User.ADMIN
    elif role == "moderator":
        user.role = User.MODERATOR
    else:
        user.role = User.MEMBER
    db.session.add(user)
    db.session.commit()

    print "username:{0}, email:{1}, password:{2}, role:{3}".format(
        user.username, user.email, password, user.role)
    return


@manager.command
def createall():
    "Creates database tables"
    db.create_all()


@manager.command
def dropall():
    "Drops all database tables"

    if prompt_bool("Are you sure ? You will lose all your data !"):
        db.drop_all()

if __name__ == "__main__":
    manager.run()
