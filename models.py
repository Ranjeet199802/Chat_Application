from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from sqlalchemy.sql import func
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/sqlite3/database/chat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


# associations = db.Table('associations',
#                         db.Column('Room_id', db.Integer, db.ForeignKey('room.id')),
#                         db.Column('User_id', db.Integer, db.ForeignKey('users.id')),
#
#                         db.PrimaryKeyConstraint('User_id', 'Room_id')
#                         )


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_no = db.Column(db.Integer, unique=True, nullable=False)
    city = db.Column(db.String(80), nullable=False)
    rooms = db.relationship('Room', backref='users')
    room_members = db.relationship('room_member', backref='users')
    message = db.relationship('messages', backref='users')
    # associations = db.relationship("Room", secondary=associations, backref=db.backref('creator', lazy=True))


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    r_name = db.Column(db.String(200), unique=False, nullable=False)
    date_time = db.Column(db.String(120))
    created_by = db.Column(db.String(200), db.ForeignKey('users.id'), nullable=False)
    r_description = db.Column(db.String(200), nullable=True)
    room_memberss = db.relationship('room_member')


class room_member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    Rid = db.Column(db.Integer, db.ForeignKey(Room.id), nullable=False)


class messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String(300), nullable=True)
    time = db.Column(db.String(100), nullable=False)


if __name__ == '__main__':
    # db.init_app(app)
    # with app.app_context():
    manager.run()
    db.create_all()
