from django.contrib.syndication.views import Feed
from .models import Post


class AllPostsRssFeed(Feed):
    title = "Testtitle"   # 显示在聚合阅读器上的标题
    link = "/"   # 跳转地址
    description = "Testdescription"   # 描述

    def items(self):
        return Post.objects.all()   # 内容条目

    def item_title(self, item):
        return '[%s] %s' % (item.category, item.title)   # 显示内容条目的标题

    def item_description(self, item):
        return item.body   # 内容条目的描述

