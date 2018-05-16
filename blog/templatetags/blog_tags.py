# 自定义模板标签 version>1.9
from ..models import Post, Category #分类模板标签和文章模板标签需要用到Category和Post类
from django import template


register = template.Library()


@register.simple_tag   # 定义装饰器，此将函数传递给register.simple_tag，注册为模板标签
def get_recent_posts(num=5):   # 获取最新5篇文章
    return Post.objects.all()[:num]   # .order_by('-created_time')


@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')
    # 按照降序返回Post中created_time对象到月份的值


@register.simple_tag
def get_categories():
    return Category.objects.all()
