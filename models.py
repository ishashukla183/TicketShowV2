from database import db
from flask_security import RoleMixin, SQLAlchemyUserDatastore
from app import rbac

@rbac.as_user_model
class User(db.Model):
  __tablename__ = 'User'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  public_id = db.Column(db.String(50), nullable=False)
  username = db.Column(db.String(80), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(120), unique=False, nullable=False)
  first_name = db.Column(db.String(20), unique=False, nullable=False)
  last_name = db.Column(db.String(20), unique=False, nullable=False)

@rbac.as_role_model
class Role(db.Model, RoleMixin):
  __tablename__ = 'Roles'
  id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
  name = db.Column(db.String)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
roles_users = db.Table(
  'RolesUsers',
  db.Column('id', db.Integer(), primary_key=True, autoincrement=True),
  db.Column('user_id', db.Integer(), db.ForeignKey('User.id')),
  db.Column('role_id', db.Integer(), db.ForeignKey('Role.id')))

class Theatre(db.Model):
  __tablename__ = 'Theatre'
  id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
  name = db.Column(db.String(80), nullable=False)
  location = db.Column(db.String(80), nullable=False)
  capacity = db.Column(db.Integer, nullable=False)

class Show(db.Model):
  __tablename__ = 'Show'
  id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
  name = db.Column(db.String(80), nullable=False)
  rating = db.Column(db.Float, nullable=False)

class ShowTheatreTicket(db.Model):
  __tablename__ = 'ShowTheatreTicket'
  theatre_id = db.Column(db.Integer(),
                         db.ForeignKey('Theatre.id'),
                         primary_key=True)
  show_id = db.Column(db.Integer(), db.ForeignKey('Show.id'), primary_key=True)
  ticket_price = db.Column(db.Integer(), nullable=False)

class Tags(db.Model):
  __tablename__ = 'Tags'
  id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
  tag = db.Column(db.String(20), nullable=False)
  show_id = db.Column(db.Integer(), db.ForeignKey('Show.id'), nullable=False)

class Booking(db.Model):
  __tablename__ = 'Booking'
  id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
  theatre_id = db.Column(db.Integer(), db.ForeignKey('Theatre.id'))
  show_id = db.Column(db.Integer(), db.ForeignKey('Show.id'))
  user_id = db.Column(db.Integer(), db.ForeignKey('User.id'))
  qty = db.Column(db.Integer(), nullable=False)
