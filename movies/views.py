import json

from django.shortcuts import render
from django.views     import View

from users.models import User
from .models import *


# 상세페이지
class DetailView(View):
    def get(self, request):
        pass