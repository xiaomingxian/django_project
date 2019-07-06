from django.shortcuts import render

from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, redirect
from user.models import *
from django.contrib.auth import get_user_model

User = get_user_model()

from django.urls import reverse
# 激活邮件加密
from itsdangerous import TimedJSONWebSignatureSerializer as JiaMi
# 密码加密
import hashlib
from django.conf import settings
# 邮件发送
from django.core.mail import send_mail
# 导入发送邮件的celery_task
from celery_task.task import send_mail as t_send
# 用户认证环节
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin


class register(View):
    def get(self, request):
        # 访问注册页面
        return render(request, 'user/register.html')
        # return HttpResponse('注册页面')

    def post(self, request):
        # 提交表单
        allow = request.POST.get("allow")

        if allow == "on":

            try:
                user_name = request.POST.get("user_name")
                pwd = request.POST.get("pwd")
                email = request.POST.get("email")
                pwd = hashlib.sha1(pwd.encode("utf8")).hexdigest()
                print('----- : ', user_name, pwd, email)
                User.objects.create_user(user_name=user_name, password=pwd,
                                         username=user_name,
                                         mail=email,
                                         authority=0)
                # 异步发送激活邮件
                user = User.objects.get(user_name=user_name)
                # 将任务放入任务队列[中间件]----在经过@app.task装饰之后就有了delay属性
                t_send.delay(user.id, email)

                # 同步发送激活邮件
                # user = User.objects.get(user_name=user_name)
                # mi = JiaMi(settings.SECRET_KEY, 3600)
                # data = mi.dumps({"id": user.id})
                # x = data.decode('utf8')
                #
                # msg = '<a href="http://127.0.0.1:8000/user/active/%s" target="_blank">点击激活</a>' % x
                # send_mail('标题', '内容', settings.EMAIL_FROM,
                #           [email],
                #           html_message=msg)

            except Exception as e:
                print(e)

        else:
            return redirect('register')

        return redirect(reverse('goods:index'))


# 用户激活
class active(View):
    def get(self, request, data):
        # data = request.GET.get('data')
        print('data : ', data)
        # 获取用户id
        mi = JiaMi(settings.SECRET_KEY, 3600)
        code = mi.loads(data)
        user = User.objects.get(id=code['id'])
        if user:
            user.alive = 1
            user.save()
        return redirect(reverse('goods:index'))


# def active(request, data):
#     print('---------- 激活 -------------')
#     # 获取用户id
#     mi = JiaMi(settings.SECRET_KEY, 3600)
#     code = mi.loads(data)
#     user = User.objects.get(id=code['id'])
#     if user:
#         user.alive = 1
#         user.save()
#     else:
#         return HttpResponse("出现了错误")
#     return redirect(reverse('goods:index'))


class login_df(View):
    def get(self, request):
        # 获取用户名
        try:
            pass
            username = request.COOKIES.get('username')
            print('username : ', username)
            if username:
                # 传送数据，并勾选复选框
                return render(request, 'user/login.html', {'username': username, 'checked': 'checked'})

            return render(request, 'user/login.html', {'checked': ''})
        except Exception as e:
            print('---- 异常:', e)
        return render(request, 'user/login.html', {'checked': ''})

    def post(self, request):
        try:
            username = request.POST.get('username')
            pwd = request.POST.get('pwd')
            rember = request.POST.get('rember')
            pwd = hashlib.sha1(pwd.encode("utf8")).hexdigest()
            # 去数据库认证--返回一个经过认证的用户
            user = authenticate(username=username, password=pwd)
            print('------------- user : ', user, 'username : ', username, 'pss : ', pwd, 'rem: ', rember)
            if user:
                if user.alive == 1:
                    print(user, user.alive)
                    login(request, user)
                    # 将user放入session
                    request.session['user'] = user
                    # 判断是否是直接请求login---不是的话登录成功再次重定向到想请求的页面
                    try:
                        pass
                        dest = request.GET.get('next')
                        print('-------dest : ', dest)
                        # if dest:
                        #     response = redirect(dest)  # 返回的对象未HttpRedirect他是Httpresponse的子类
                        # else:
                        #     response = redirect(reverse('goods:index'))  # 返回的对象未HttpRedirect他是Httpresponse的子类
                        # 简易写法---前面值不存在时用第二个参数替换
                        response = redirect(dest, reverse('goods:index'))
                    except Exception as e:
                        print('-----e : ', e)
                        pass

                    # 判断是否记住用户名
                    if rember == 'on':
                        response.set_cookie('username', username, max_age=3600 * 24 * 7)
                    else:
                        response.delete_cookie('username')

                    return response

            return redirect(reverse('user:login'))
        except Exception as e:
            print('---- login e : ', e)


# 用户信息中心
class user_center_info(View):
    def get(self, request):
        print('----- user info ：', request.user, request.user.is_authenticated)
        loginOrNot = request.user.is_authenticated
        if loginOrNot:
            print('-----------已经登录...')


        else:
            print('-----------未登录 ...')
            pass

        return render(request, 'user/user_center_info.html')


class logout_df(View):
    def get(self, request):
        logout(request)
        return redirect(reverse("goods:index"))

    pass


class user_center_site(LoginRequiredMixin, View):
    def get(self, request):
        # 根据当前用户查询地址信息
        user = request.user
        #
        # try:
        #     address = Address.objects.get(userId=request.user, isDefault=1)
        # except Exception as e:
        #     print('e : ', e)
        #     address = None
        # print('aaaa : ', address)
        address = Address.objects.show_address_default(user)

        return render(request, 'user/user_center_site.html', {'Address': address})

    def post(self, request):
        # 添加地址信息
        name = request.POST.get('name')
        address = request.POST.get('address')
        zipCode = request.POST.get('zipCode')
        telNumber = request.POST.get('telNumber')
        # 查询用户是否有默认地址
        # try:
        #     adds = Address.objects.get(userId=request.user, isDefault=1)
        #
        #     isDefault = 0
        # except Exception as e:
        #     print('没有默认地址')
        #     isDefault = 1
        #     pass

        adds = Address.objects.show_address_default(request.user)
        if adds:
            isDefault = 0
        else:
            isDefault = 1

        Address.objects.create(name=name, address=address, zipCode=zipCode, telNumber=telNumber,
                               isDefault=isDefault, userId=request.user)
        return redirect(reverse('user:site'))


# redis原生连接方式
# from redis import StrictRedis
#
# st = StrictRedis(host='localhost', port='6379', db=7)


# django中的redis
from django_redis import get_redis_connection

# settings中的缓存配置
redis_con = get_redis_connection('default')

# 存储浏览信息到redis----数据结构hash history:userid:x,xx,x,x,x/list userid:[x,x,x,x]
class store_history(LoginRequiredMixin, View):
    def get(self):
        pass

    pass


class get_history(LoginRequiredMixin, View):
    def get(self):
        pass

    pass
