from django.db import models

# Create your models here.


# 1.创建评论数据库模型--> 2.迁移数据库
class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    url = models.URLField(blank=True)
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('blog.post', on_delete=models.CASCADE)   # 设置文章与评论的关系为一对多,不要忘记创建外键

    def __str__(self):
        return self.text[:20]
