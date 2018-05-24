# 自定义模板标签 version>1.9
from ..models import Post, Category, Tag   # 分类模板标签和文章模板标签需要用到Category和Post类
from django import template
from django.db.models.aggregates import Count


register = template.Library()


@register.simple_tag   # 定义装饰器，此将函数传递给register.simple_tag，注册为模板标签
def get_recent_posts(num=5):   # 获取最新5篇文章
    return Post.objects.all()[:num]   # .order_by('-created_time')


@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')
    # 按照降序返回Post中created_time对象到月份的值


@register.simple_tag
def get_categories():   # 为每个分类添加一个计数的方法属性
    # return Category.objects.all()
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    # 通过annotate获取当前分类下的全部post,用count方法自动计数，filter筛选掉没有任何文章的分类
    # object__gt=x表示集合中大于x的数


@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
