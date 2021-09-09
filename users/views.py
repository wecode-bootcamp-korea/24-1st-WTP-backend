import json
from json import decoder
import re
from users.utils import login_decorator
import bcrypt, jwt
from json.decoder import JSONDecodeError

from django.http.response   import HttpResponse, JsonResponse
from django.views           import View
from django.http            import JsonResponse

from users.models           import User
from movies.models           import Rating
from my_settings      import SECRET_KEY, ALGORITHM


class SignUpView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            name     = data['name']
            email    = data['email']
            password = data['password']

            if not re.match('^[a-zA-Z가-힣]{2,}$', name):
                return JsonResponse({'MESSAGE' : 'Wrong Name Form'}, status = 400)

            if not re.match('^[a-zA-Z\d+-.]+@[a-zA-Z\d+-.]+\.[a-zA-Z]{2,3}$', email):
                return JsonResponse({'MESSAGE' : 'Wrong E-mail Form'}, status = 400)

            if not re.match('^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{10,}$',password):
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


class Login(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if not User.objects.filter(email=data['email']).exists():
                return JsonResponse({"message": "존재하지 않는 아이디입니다!"}, status=401)

            # db 안에 들어있는 비밀번호
            current_user = User.objects.get(email=data['email'])
            
            if not bcrypt.checkpw(data['password'].encode(), current_user.password.encode()):
                return JsonResponse({"message": "비밀번호가 일치하지 않습니다!"}, status=401)
                
            token = jwt.encode({"id": current_user.id}, SECRET_KEY, algorithm=ALGORITHM)
            
            return JsonResponse({
                "message"   : "accepted",
                "auth_token": token,
                "user_name" : current_user.name
            }, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY ERROR"}, status=400)

        except ValueError:
            return JsonResponse({"message": "VALUE ERROR"}, status=400)
        
        except JSONDecodeError:
            return JsonResponse({"message": "INVALID DATA FORMAT"}, status=400)


class MyPageView(View):
    @login_decorator
    def get(self, request):
        user_id = request.user.id

        movies = Rating.objects.select_related('movie').filter(user_id=user_id)

        if movies:
            my_movies = [{
                "title" : movie.movie.title,
                "rating": movie.rate,
                "poster": movie.movie.poster_image,
            }for movie in movies]
                
            return JsonResponse({"movies": my_movies}, status=200)
        
        return HttpResponse('NO CONTENTS', status=204)
        