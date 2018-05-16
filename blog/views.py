import markdown
from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from comments.forms import CommentForm   # 更新文章详情页的视图函数
from django.http import HttpResponse

# Create your views here.


def index(request):   # request为封装好的HTTP请求
    post_list = Post.objects.all()   # .order_by('-created_time')all()返回QuerSet(类似列表的数据结构)
    # -即倒序排列
    return render(request, 'blog/index.html', context={'post_list': post_list})   # 封装HTTP响应，渲染为Response
    # {}模板变量，在最终渲染视图里替换views传过来的值


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)   # 判断传入的pk的是否在数据库存在，如果存在，返回对应的post,反之返回404错误
    post.increase_views()
    post.body = markdown.markdown(post.body,
                                  extensions=[   # extensions为markdown的参数
                                    'markdown.extensions.extra',
                                    'markdown.extensions.codehilite',   # 语法高亮拓展
                                    'markdown.extensions.toc',   # 自动生成目录
                                  ])
    form = CommentForm()
    comment_list = post.comment_set.all()   # 获取这篇post下的全部评论数据
    context = {'post': post, 'form': form, 'comment_list': comment_list}
    return render(request, 'blog/detail.html', context=context)


def archives(request, year, month):   # 筛选出created_time的year和month的文章,由于是参数列表，用__代替.
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    )   # .order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)    # 这里为分类的id
    post_list = Post.objects.filter(category=cate)   # .order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})