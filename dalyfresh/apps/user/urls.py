from django.conf.urls import url, include
import user.views as u
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url('^register', u.register.as_view()),
    url('^active/(?P<data>.*)', u.active.as_view()),
    url('^login', u.login_df.as_view(), name='login'),
    # url('^active/(?P<data>.*)', u.active),
    url('^user_center_info$', login_required(u.user_center_info.as_view()), name='user'),
    url('^logout$', u.logout_df.as_view(), name='logout'),
    url('^user_center_site$', u.user_center_site.as_view(), name='site'),
]

app_name = 'user'
