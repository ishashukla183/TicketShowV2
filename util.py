# flask imports
from flask import request
# imports for PyJWT authentication
from config import app
import jwt
from functools import wraps
from models import User


def token_required(f):

  @wraps(f)
  def decorated(*args, **kwargs):
    token = None
    # jwt is passed in the request header
    if 'x-access-token' in request.headers:
      token = request.headers['x-access-token']
    # return 401 if token is not passed
    if not token:
      return {'message': 'Token is missing !!'}, 401

    try:
      # decoding the payload to fetch the stored details
      data = jwt.decode(token, app.config['SECRET_KEY'])
      current_user = User.query\
          .filter_by(public_id = data['public_id'])\
          .first()
    except:
      return {'message': 'Token is invalid !!'}, 401
    # returns the current logged in users context to the routes
    return f(current_user, *args, **kwargs)

  return decorated
