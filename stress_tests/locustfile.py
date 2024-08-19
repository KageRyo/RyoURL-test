import os

BASE_URL = os.getenv('BASE_URL', 'http://172.21.0.2:8000/api')

from anonymous_user import AnonymousUser
from authenticated_user import AuthenticatedUser
from admin_user import AdminUser