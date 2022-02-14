from flask_restx import Api
from flask import Blueprint

from .controller import api as auth_ns

auth_bp = Blueprint('auth', __name__)


auth = Api(auth_bp, title='Application Authentication', version='1.0')

auth.add_namespace(auth_ns)