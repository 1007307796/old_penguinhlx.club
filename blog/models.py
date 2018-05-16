from django.db import models
from django.contrib.auth.models import User   # 引入处理用户交互的流程（登陆，注册等）
from django.urls import reverse   # 用于生成post必要的包
import markdown   # 引入makedown语法包
from django.utils.html import strip_tags   # 引入makedown转html包

# 更改模型后须迁移数据库
# Create your models here.
# coding: utf-8
# 两个花括号{{}}表示替换变量,数据由后端提供，一个花括号{}表示替换路由地址或标签，不经由后端数据库
# 实现博客文章，分类及标签功能


class Category(models.Model):   # Category(分类)是继承models.Model的标准类
    name = models.CharField(max_length=100)   # 创建分类数据库表格

    def __str__(self):
        return self.name   # 增加在shell里返回当前数据库字段的内容的函数


class Tag(models.Model):
    name = models.CharField(max_length=100)   # 创建标签数据库表格

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=70)   # 文章标题
    body = models.TextField()   # 文章正文
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()   # 文章创建时间和最后一次修改时间
    excerpt = models.CharField(max_length=200, blank=True)   # 文章摘要 设置CharField允许空值
    category = models.ForeignKey(Category, on_delete=models.CASCADE)   # 将分类设置为一对多关系
    tags = models.ManyToManyField(Tag, blank=True)   # 将标签设置为多对多关系
    author = models.ForeignKey(User, on_delete=models.CASCADE)   # 将作者设置为一对多关系
    # 指定外键方式on_delete=models.CASCADE
    views = models.PositiveIntegerField(default=0)   # 设置评论数量模型

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})   # 生成当前Post的url地址

    def increase_views(self):   # 每当调用此函数，评论数+1，并存至数据库中
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        if not self.excerpt:
            md = markdown.Markdown(extensions=['markdown.extensions.extra',
                                               'markdown.extensions.codehilite',
            ])   # 实例化markdown类，用于渲染body文本，这里为什么
            self.excerpt = strip_tags(md.convert(self.body))[:54]
            # 转换makedown为html-->去html标签-->复制给摘录对象
        super(Post, self).save(*args, **kwargs)   # 调用父类，保存文章数据库

    class Meta:   # 通过models的内部类规定这个类的共有特性
        ordering = ['-created_time', 'title']

