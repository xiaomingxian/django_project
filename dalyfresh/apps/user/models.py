from django.db import models
from django.contrib.auth.models import AbstractUser
from db.models import BaseModel


# Create your models here.

# 自定义模型管理器类   对象.object返回的是模型管理器类  models.Manager
class AddressModelManager(models.Manager):
    # 应用场景
    # 1.改变原有结果集  eg:过滤
    # 2.封装新方法
    # 自定义显示默认地址
    def show_address_default(self, user):
        # self.model当前对象对应的模型类----简写为self
        try:
            address = self.get(userId=user, isDefault=1)
        except Exception as e:
            address = None

        return address


class User(AbstractUser, BaseModel):
    LIVE_FLAG = (
        (0, '未激活'),
        (1, '激活'),
    )
    AUTHORITY_FLAG = (
        (0, '无权限'),
        (1, '有权限'),
    )
    user_name = models.CharField(max_length=30, verbose_name='用户名')
    password = models.CharField(max_length=80, verbose_name='密码')
    mail = models.CharField(max_length=50, verbose_name='邮箱')
    alive = models.SmallIntegerField(choices=LIVE_FLAG, default=0, verbose_name='激活标志')
    authority = models.SmallIntegerField(choices=AUTHORITY_FLAG, default=0, verbose_name='权限')

    class Meta:
        db_table = 'user'
        verbose_name = '用户'  # 管理页面显示
        verbose_name_plural = verbose_name  # 复数形式


# 地址表
class Address(BaseModel):
    IS_DEFAULT = ((0, '否'), (1, '是'))
    name = models.CharField(max_length=100, verbose_name='收件人姓名')
    address = models.CharField(max_length=200, verbose_name='收件人地址')
    zipCode = models.CharField(max_length=50, null=True, verbose_name='邮编')
    telNumber = models.CharField(max_length=11, verbose_name='联系方式')
    isDefault = models.SmallIntegerField(choices=IS_DEFAULT, default=0, verbose_name='是否默认')  # 也可以写称boolean类型
    userId = models.ForeignKey('User', on_delete=models.CASCADE)

    objects = AddressModelManager()

    class Meta:
        db_table = 'Address'
        verbose_name = '用户地址'  # 管理页面显示
        verbose_name_plural = verbose_name  # 复数形式
