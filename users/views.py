import json, bcrypt
import jwt

from django.http      import JsonResponse
from django.views     import View

from users.models     import User
from my_settings      import SECRET_KEY, ALGORITHM


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
                "message": "accepted",
                "token": token,
            }, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY ERROR"}, status=400)

        except ValueError:
            return JsonResponse({"message": "VALUE ERROR"}, status=400)