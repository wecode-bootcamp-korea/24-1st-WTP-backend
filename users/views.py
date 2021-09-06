import json
import re
import bcrypt

from django.http.response   import JsonResponse
from django.views           import View
from django.http            import JsonResponse

from users.models           import User


class SignUpView(View):
    def post(self, request):
        try:
            data             = json.loads(request.body)
            name     = data['name']
            email    = data['email']
            password = data['password']

            if not re.match('^[a-zA-Z가-힣]{2,}$', name):
                return JsonResponse({'MESSAGE' : 'Wrong Name Form'}, status = 400)

            if not re.match('^[a-zA-Z\d+-.]+@[a-zA-Z\d+-.]+\.[a-zA-Z]{2,3}$', email):
                return JsonResponse({'MESSAGE' : 'Wrong E-mail Form'}, status = 400)

            if not re.match('^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*-_])[A-Za-z\d!@#$%^&*-_]{10,}$',password):
                return JsonResponse({'MESSAGE' : 'Wrong Password Form'}, status = 400)

            if User.objects.filter(email = email).exists():
                return JsonResponse({'MESSAGE':'Existed E-Mail'}, status = 400)

            decoded_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            User.objects.create(
                name     = name,
                email    = email,
                password = decoded_password,
            )

            return JsonResponse({'MESSAGE':'User Registered!'}, status = 201)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)

        except ValueError:
            return JsonResponse({'MESSAGE':'VALUE_ERROR'}, status = 400)
