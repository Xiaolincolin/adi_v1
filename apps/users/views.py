import csv
import random
import string

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View

from .forms import LoginForm
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from .models import UserProfile
from django.urls import reverse

# Create your views here.

# 登录逻辑
class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")

            user = authenticate(username=user_name, password=pass_word)
            print(user)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('media/')
            else:
                return render(request, 'login.html', {"msg": "用户名或密码错误！"})
        else:
            return render(request, 'login.html', {"msg": "用户名或密码错误！"})

class TmpView(View):
    def get(self,request):
        return HttpResponseRedirect(reverse("login"))

# 退出登录
class LogoutView(View):

    def get(self, request):
        logout(request)
        import time
        time.sleep(4)
        return HttpResponseRedirect(reverse("login"))
