from django.urls import path

from users.views import Login, SignUpView 

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/login', Login.as_view()),
]