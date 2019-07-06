from django.db import models
from tinymce.models import HTMLField
from db.models import BaseModel


class GoodsType(BaseModel):
    name = models.CharField(max_length=20, verbose_name='种类名称')
    logo = models.CharField(max_length=20,
                            verbose_name='log')  # logo值是定位的部分 CSS雪碧 即CSS Sprite，是一种CSS图像合并技术，该方法是将小图标和背景图像合并到一张图片上，然后利用css的背景定位来显示需要显示的图片部分
    image = models.ImageField(upload_to='type')

    class Meta:
        db_table = 'TypeInfo'
        verbose_name = '商品类型'
        verbose_name_plural = verbose_name


# 商品--SPU
# spu是款  ---  sku是件
class GoodsSPU(BaseModel):
    """SPU"""
    name = models.CharField(max_length=20, verbose_name='商品SPU名称')
    detail = HTMLField(blank=True, verbose_name='商品详情')

    class Meta:
        db_table = 'GoodsSPU'
        verbose_name = '商品SPU'
        verbose_name_plural = verbose_name


# 商品SKU
class GoodsSKU(BaseModel):
    STATUS_CHOICES = (
        (0, '下架'),
        (1, '上架'),
    )
    # 外键
    type = models.ForeignKey('GoodsType', on_delete=models.CASCADE, verbose_name='商品种类')
    goods = models.ForeignKey('GoodsSPU', on_delete=models.CASCADE, verbose_name='商品SPU')

    name = models.CharField(max_length=20, verbose_name='商品名称')
    desc = models.CharField(max_length=256, verbose_name='商品简介')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    unit = models.CharField(max_length=20, verbose_name='商品单位')
    image = models.ImageField(upload_to='sku')
    stock = models.IntegerField(default=1, verbose_name='sku库存')
    sales = models.IntegerField(default=0, choices=STATUS_CHOICES, verbose_name='商品销量')

    class Meta:
        db_table = 'GoodsSKU'
        verbose_name = '商品SKU'
        verbose_name_plural = verbose_name


# 商品图片
class GoodsImage(BaseModel):
    sku = models.ForeignKey('GoodsSKU', on_delete=models.CASCADE,verbose_name='sku图')
    pic = models.ImageField(upload_to='sku')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')

    class Meta:
        db_table = 'GoodsImage'
        verbose_name = 'sku图'
        verbose_name_plural = verbose_name


# 展示类型
class IndexTypeBanner(BaseModel):
    DISPLAY_TYPE = ((0, '图片'), (1, '标题'))

    type = models.ForeignKey('GoodsType',on_delete=models.CASCADE, verbose_name='商品类型')
    sku = models.ForeignKey('GoodsSKU', on_delete=models.CASCADE,verbose_name='商品sku')
    display_type = models.SmallIntegerField(choices=DISPLAY_TYPE, default=0, verbose_name='展示类型')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')

    class Meta:
        db_table = 'IndexTypeBanner'
        verbose_name = '展示类型'
        verbose_name_plural = verbose_name


# 首页轮播
class IndexGoodsBanner(BaseModel):
    sku = models.ForeignKey('GoodsSKU',on_delete=models.CASCADE, verbose_name='图片所属sku名称 ')
    pic = models.ImageField(upload_to='sku')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')

    class Meta:
        db_table = 'IndexGoodsBanner'
        verbose_name = '首页轮播'
        verbose_name_plural = verbose_name


# 首页促销
class IndexPromotionBanner(BaseModel):
    sku = models.ForeignKey('GoodsSKU',on_delete=models.CASCADE, verbose_name='活动名称')
    url = models.URLField(verbose_name='活动链接')
    pic = models.ImageField(upload_to='sku')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')

    class Meta:
        db_table = 'IndexPromotionBanner'
        verbose_name = '首页促销'
        verbose_name_plural = verbose_name
