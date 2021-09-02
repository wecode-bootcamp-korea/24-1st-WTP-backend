from my_settings import SECRET_KEY
import jwt

from .models import User
from my_settings import SECRET_KEY

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get("Authorization", None)
            user = jwt.decode(access_token, SECRET_KEY, algorithms='HS256')
            request.user = User.objects.get(id = user['id'])
            
        
        except:
            pass
