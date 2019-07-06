from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.


# 顺序不能颠倒-----原理:在LoginRequiredMixin中对as_view进行了封装  ：使用login_required对View进行了装饰
class index(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'goods/index.html')




