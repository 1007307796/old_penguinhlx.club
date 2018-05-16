from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
from .models import Comment
from .forms import CommentForm


# Create your views here.


def post_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)  # 获取文章pk
    if request.method == 'POST':
        form = CommentForm(request.POST)  # 用户提交的数据存在request.POST类字典对象中
        if form.is_valid():
            comment = form.save(commit=False)  # 利用表单数据生成Comment实例
            comment.post = post  # 将评论和文章关联起来
            comment.save()  # 将评论保存进数据库
            return redirect(post)  # redirect函数接收到一个实例时，会调用这个实例的get_absolute_url方法
            # 然后重定向该方法返回的url
        else:   # 检查数据不合法时，返回渲染表单的错误
            comment_list = post.comment_set.all()   # object_set.all()反向获取该文章下的全部评论
            context = {'post': post,
                       'form': form,
                       'comment_list': comment_list
                       }
            return render(request, 'blog/detail.html', context=context)
    return redirect(post)
