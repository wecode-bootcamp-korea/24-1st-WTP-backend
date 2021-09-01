import json
import re
import bcrypt

from django.http.response import JsonResponse
from django.shortcuts import render
from users.models     import User
from django.views     import View
from django.http      import JsonResponse


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
            if not re.match('^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$', sign_up_email):
                return JsonResponse({'MESSAGE' : 'Wrong E-mail Form'}, status = 400)

            # Password Validation
            if not re.match('^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*-_])[A-Za-z\d!@#$%^&*-_]{10,}$',sign_up_password):
                return JsonResponse({'MESSAGE' : 'Wrong Password Form'}, status = 400)

            # Duplicated E-mail Validation
            if User.objects.filter(email = sign_up_email).exists():
                return JsonResponse({'MESSAGE':'Existed E-Mail'}, status = 400)

            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(sign_up_password.encode('utf-8'), salt)
            decoded_password = hashed_password.decode('utf-8')
            
            # User Registration
            User.objects.create(
                name     = sign_up_name,
                email    = sign_up_email,
                password = decoded_password,
            )

            return JsonResponse({'MESSAGE':'User Registered!'}, status = 200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)