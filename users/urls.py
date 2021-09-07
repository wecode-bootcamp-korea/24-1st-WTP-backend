from django.urls import path

<<<<<<< HEAD
from users.views import Login


urlpatterns = [
    path('/login', Login.as_view()),
]
=======
from users.views import Login, SignUpView 

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/login', Login.as_view()),
]
>>>>>>> main
