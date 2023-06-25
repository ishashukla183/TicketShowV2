from flask import Flask
from flask_rbac import RBAC

# Create app
app = Flask(__name__)
rbac = RBAC(app)