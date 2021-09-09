from django.urls import path

from users.views import Login, SignUpView, MyPageView

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/login', Login.as_view()),
    path("/mypage", MyPageView.as_view()),
]
