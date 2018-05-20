import markdown
from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from comments.forms import CommentForm   # 更新文章详情页的视图函数
from django.views.generic import ListView, DetailView   # 引入类列表（多条）视图包和类数据（某一条）视图包
from django.http import HttpResponse

# Create your views here.

'''   # 将视图函数改写为类视图 
def index(request):   # request为封装好的HTTP请求
    post_list = Post.objects.all()   # .order_by('-created_time')all()返回QuerSet(类似列表的数据结构)
    # -即倒序排列
    return render(request, 'blog/index.html', context={'post_list': post_list})   # 封装HTTP响应，渲染为Response
    # {}模板变量，在最终渲染视图里替换views传过来的值
'''


class IndexView(ListView):   # 类视图
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'   # 指定获取的模型列表数据保存的变量名,将传递给模板


'''转换函数视图
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
'''


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        # 调用get方法后，才能有self.object属性，其值为post文章
        self.object.increase_views()   # 调用阅读量增加1的函数
        return response   # 视图必须返回一个httprespnse对象

    def get_object(self, queryset=None):   # 对post的body值进行渲染
        post = super(PostDetailView, self).get_object(queryset=None)
        post.body = markdown.markdown(post.body,
                                      extensions=[  # extensions为markdown的参数
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',  # 语法高亮拓展
                                          'markdown.extensions.toc',  # 自动生成目录
                                      ])
        return post

    def get_context_data(self, **kwargs):   # 将post下评论传递给模板
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context   # 返回模板变量字典httpResponse，传递给模板


'''
def archives(request, year, month):   # 筛选出created_time的year和month的文章,由于是参数列表，用__代替.
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    )   # .order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

'''


class ArchivesView(IndexView):

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(created_time__year=year, created_time__month=month)


'''函数视图
def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)    # 这里为分类的id
    post_list = Post.objects.filter(category=cate)   # .order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})
'''


class CategoryView(IndexView):   # 继承IndexView，简约代码

    def get_queryset(self):    # 覆写get_queryset()方法，改获取全部列表数据为获取指定分类下的文章。
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        # *args表示任何多个无名参数,**kwargs表示关键字参数，它是一个dict
        return super(CategoryView, self).get_queryset().filter(category=cate)