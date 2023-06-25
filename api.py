# flask imports
from flask import request
import uuid  # for public id
from werkzeug.security import generate_password_hash, check_password_hash
# imports for PyJWT authentication
import jwt
from datetime import datetime, timedelta
from app import app, rbac
from flask import g, current_app
from models import User, db, roles_users
from flask_restful import Api, Resource

api = Api(app)


def get_current_user():
  with current_app.request_context():
    return g.current_user


rbac.set_user_loader(get_current_user)


class LoginAPI(Resource):

  def post(self):
    # creates dictionary of form data
    auth = request.form

    if not auth or not auth.get('username') or not auth.get('password'):
      # returns 401 if any email or / and password is missing
      return 'Could not verify', 401, {
        'WWW-Authenticate': 'Basic realm ="Login required !!"'
      }

    user = User.query\
        .filter_by(username = auth.get('username'))\
        .first()

    if not user:
      # returns 401 if user does not exist
      return 'Could not verify', 401, {
        'WWW-Authenticate': 'Basic realm ="User does not exist !!"'
      }

    if check_password_hash(user.password, auth.get('password')):
      # generates the JWT Token
      token = jwt.encode(
        {
          'public_id': user.public_id,
          'exp': datetime.utcnow() + timedelta(minutes=30)
        }, app.config['SECRET_KEY'])

      g.current_user = user
      g.current_user.role = roles_users.select().where(user_id=user.id)
      
      return {'token': token}, 201
    # returns 403 if password is wrong
    return 'Could not verify', 403, {
      'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'
    }


api.add_resource(LoginAPI, '/login')


class SignupAPI(Resource):

  # # @app.route('/user', methods=['GET'])
  # @token_required
  # def get(self, current_user):
  #   # querying the database
  #   # for all the entries in it
  #   users = User.query.all()
  #   # converting the query objects
  #   # to list of jsons
  #   output = []
  #   for user in users:
  #     # appending the user data json
  #     # to the response list
  #     output.append({
  #       'public_id': user.public_id,
  #       'first name': user.first_name,
  #       'last name': user.first_name,
  #       'email': user.email,
  #       'username': user.email,
  #     })

  #   return {'users': output}

  # route for logging user in
  # @app.route('/login', methods=['POST'])

  # signup route

  # @app.route('/signup', methods=['POST'])

  def post(self):
    # creates a dictionary of the form data
    data = request.form
    print('data', data.get('username'))
    # gets name, email and password
    username, first_name, last_name, email, password = data.get(
      'username'), data.get('first_name'), data.get('last_name'), data.get(
        'email'), data.get('password')

    # checking for existing user
    user = User.query\
        .filter_by(username = username)\
        .first()

    if not user:
      # database ORM object
      user = User(
        public_id=str(uuid.uuid4()),
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=generate_password_hash(password),
      )
      print('user', user)
      # insert user
      
      db.session.add(user)
      db.session.commit()
      user = User.query\
        .filter_by(username = username)\
        .first()
      roles_users.insert().values(role_id=1, user_id = user.id)
      return 'Successfully registered.', 201
    else:
      # returns 202 if user already exists
      return 'User already exists. Please Log in.', 202


class UserAPI(Resource):
  pass


class BookingAPI(Resource):
  pass


api.add_resource(SignupAPI, '/signup')
