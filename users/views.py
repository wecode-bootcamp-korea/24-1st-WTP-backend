import json
import re
import bcrypt

from django.http.response   import JsonResponse
from django.shortcuts       import render
from django.views           import View
from django.http            import JsonResponse

from users.models           import User


class SignUpView(View):
    def post(self, request):
        try:
            data             = json.loads(request.body)
            sign_up_name     = data['name']
            sign_up_email    = data['email']
            sign_up_password = data['password']

            # Name Validation
            if not re.match('^[a-zA-Z가-힣]{2,}$', sign_up_name):
                return JsonResponse({'MESSAGE' : 'Wrong Name Form'}, status = 400)

            # E-mail Validation
            if not re.match('^[a-zA-Z\d+-.]+@[a-zA-Z\d+-.]+\.[a-zA-Z]{2,3}$', sign_up_email):
                return JsonResponse({'MESSAGE' : 'Wrong E-mail Form'}, status = 400)

            # Password Validation
            if not re.match('^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*-_])[A-Za-z\d!@#$%^&*-_]{10,}$',sign_up_password):
                return JsonResponse({'MESSAGE' : 'Wrong Password Form'}, status = 400)

            # Duplicated E-mail Validation
            if User.objects.filter(email = sign_up_email).exists():
                return JsonResponse({'MESSAGE':'Existed E-Mail'}, status = 400)

            decoded_password = bcrypt.hashpw(sign_up_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # User Registration
            User.objects.create(
                name     = sign_up_name,
                email    = sign_up_email,
                password = decoded_password,
            )

            return JsonResponse({'MESSAGE':'User Registered!'}, status = 201)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)

        except ValueError:
            return JsonResponse({'MESSAGE':'VALUE_ERROR'}, status = 400)
