from django.db import models
from db.models import BaseModel


# 订单详情
class OrderInfo(BaseModel):
    PAY_METHOD = (
        (0, '微信'),
        (1, '支付宝'),
        (2, '银联'),
    )
    ORDER_STATUS = (
        (0, '待支付'),
        (1, '待发货'),
        (2, '待收货'),
        (3, '待评价'),
        (4, '完成'),
    )

    order_id = models.CharField(max_length=128, primary_key=True, verbose_name='订单id')
    # 外键
    user = models.ForeignKey('user.User', on_delete=models.CASCADE,verbose_name='用户')
    addr = models.ForeignKey('user.Address',on_delete=models.CASCADE, verbose_name='地址')

    pay_method = models.SmallIntegerField(choices=PAY_METHOD, default=0, verbose_name='支付方式')
    total_count = models.IntegerField(default=1, verbose_name='商品数量')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='订单总价')
    transit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='运费')
    order_status = models.SmallIntegerField(choices=ORDER_STATUS, default=0, verbose_name='订单状态')
    pay_num = models.CharField(max_length=100, verbose_name='支付编号')

    class Meta:
        db_table = 'OrderInfo'
        verbose_name = '订单信息'
        verbose_name_plural = verbose_name


# 订单模型类
class OrderGoods(BaseModel):
    order = models.ForeignKey('OrderInfo',on_delete=models.CASCADE, verbose_name='订单')
    sku = models.ForeignKey('goods.GoodsSKU', on_delete=models.CASCADE,verbose_name='sku')
    count = models.IntegerField(default=1, verbose_name='订单数量')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='订单价格')
    coment = models.CharField(max_length=256, verbose_name='评论')

    class Meta:
        db_table = 'OrderGoods'
        verbose_name = '订单模型'
        verbose_name_plural = verbose_name
