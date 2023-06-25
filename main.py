from app import app
from database import db
from config import *
from api import *
from flask_security import Security
from models import user_datastore

app.security = Security(app, user_datastore)
db.init_app(app)
app.app_context().push()


@app.route('/')
def index():
  return 'Hello from Flask!'


app.run(host='0.0.0.0', port=81)
