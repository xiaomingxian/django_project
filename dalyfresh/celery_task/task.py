from celery import Celery
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as JiaMi
from django.core.mail import send_mail as d_sendmial

#
# # worker进行项目和django初始化
import os
import django

# 初始化配置文件
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dalyfresh.settings")
# 在任务处理者一方加这块代码
django.setup()

# 创建Celery实例   ,,,,第一个参数不是固定的,,,broker是中间件
app = Celery('celery_task.task', broker="redis://localhost:6379/5", backend='redis://localhost:6379/5')


# 定义任务函数
@app.task
def send_mail(id, email):
    print('------------ ： 发邮件')
    mi = JiaMi(settings.SECRET_KEY, 3600)
    data = mi.dumps({"id": id})
    x = data.decode('utf8')

    msg = '<a href="http://127.0.0.1:8000/user/active/%s" target="_blank">点击激活</a>' % x
    d_sendmial('标题', '内容', settings.EMAIL_FROM, [email], html_message=msg)


@app.task
def test():
    print('-----异步任务执行-----')
