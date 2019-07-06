from django.conf.urls import url, include
import goods.views as g
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # 装饰器做法
    # url('^index$', login_required(g.index.as_view()), name='index'),
    url('^index$', g.index.as_view(), name='index'),

]

app_name = 'goods'
