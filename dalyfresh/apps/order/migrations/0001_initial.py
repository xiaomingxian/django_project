# Generated by Django 2.0 on 2018-11-05 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrderGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('isDelete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('count', models.IntegerField(default=1, verbose_name='订单数量')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='订单价格')),
                ('coment', models.CharField(max_length=256, verbose_name='评论')),
            ],
            options={
                'verbose_name': '订单模型',
                'verbose_name_plural': '订单模型',
                'db_table': 'OrderGoods',
            },
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('isDelete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('order_id', models.CharField(max_length=128, primary_key=True, serialize=False, verbose_name='订单id')),
                ('pay_method', models.SmallIntegerField(choices=[(0, '微信'), (1, '支付宝'), (2, '银联')], default=0, verbose_name='支付方式')),
                ('total_count', models.IntegerField(default=1, verbose_name='商品数量')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='订单总价')),
                ('transit_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='运费')),
                ('order_status', models.SmallIntegerField(choices=[(0, '待支付'), (1, '待发货'), (2, '待收货'), (3, '待评价'), (4, '完成')], default=0, verbose_name='订单状态')),
                ('pay_num', models.CharField(max_length=100, verbose_name='支付编号')),
            ],
            options={
                'verbose_name': '订单信息',
                'verbose_name_plural': '订单信息',
                'db_table': 'OrderInfo',
            },
        ),
    ]
