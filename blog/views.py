import markdown
from django.shortcuts import render, get_object_or_404
from blog.models import Post, Category, Tag
from comments.forms import CommentForm   # 更新文章详情页的视图函数
from django.views.generic import ListView, DetailView   # 引入类列表（多条）视图包和类数据（某一条）视图包
from django.utils.text import slugify   # 引入自动生成目录支持中文的包
from markdown.extensions.toc import TocExtension
from django.db.models import Q   # 用于包装查询表达式，提供复杂的查询逻辑
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
    paginate_by = 3   # 开启分页功能

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # 获取父类生成的字典
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        # 父类中已有上述三个变量
        pagination_data = self.pagination_data(paginator, page, is_paginated)
        # 利用下面的pagination_data方法获取所需数据
        context.update(pagination_data)  # 将函数返回的字典更新到页面中
        return context  # 将更新后的页面返回，以便ListView去渲染变量

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}  # 如果没有分页，则无需显示导航条
        left = []
        right = []
        left_has_more = False
        right_has_more = False  # 是否需要省略号展示更多
        first = False
        last = False  # 是否需要单独显示首页和尾页
        page_number = page.number  # 当前网页
        total_pages = paginator.num_pages  # 分页后的总数
        page_range = paginator.page_range  # 分类后的数组列表[1.2.3.4....]
        # 初始化各个变量
        if page_number == 1:  # 当当前为第一页时
            right = page_range[page_number:page_number + 2]  # 获取右边页码数组
            if right[-1] < total_pages - 1:  # 是否显示右侧省略号
                right_has_more = True
            if right[-1] < total_pages:  # 是否需要单独显示页尾
                last = True
        elif page_number == total_pages:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            # 当用户请求最后一页时，显示左边数据状态
            if left[0] > 2:
                left_has_more = True  # 是否显示右侧省略号
            if left[0] > 1:
                first = True  # 是否需要单独显示页首
        else:  # 用户请求的既不是首页也不是尾页
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }
        return data


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

    def get_object(self, queryset=None):   # 对post的body值进行渲染,queryset:查询设置
        """   覆写get_object()方法，改成对body值进行渲染
        post.body = markdown.markdown(post.body,
                                      extensions=[  # extensions为markdown的参数
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',  # 语法高亮拓展
                                          'markdown.extensions.toc',  # 自动生成目录
                                      ])
        return post
        """
        post = super(PostDetailView, self).get_object(queryset=None)
        md = markdown.Markdown(extensions=[  # extensions为markdown的参数
                            'markdown.extensions.extra',
                            'markdown.extensions.codehilite',  # 语法高亮拓展
                            # 'markdown.extensions.toc',  # 自动生成目录
                            TocExtension(slugify=slugify),
                            # 将toc拓展为一个实例，参数接受一个函数，处理标题的中文锚点值
        ])
        post.body = md.convert(post.body)   # 用convert将makedown文本渲染为html文本
        post.toc = md.toc   # 动态为post添加toc属性
        return post

    def get_context_data(self, **kwargs):   # 将post下评论传递给模板
        # 函数视图中，传递模板变量通过render实现，而在类视图中，通过get_context_data来实现
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context  # 返回模板变量字典httpResponse，传递给模板


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


class TagView(ListView):
    model = Post
    template_name = 'blog/index.html'   # 复用index.html的模板
    context_object_name = 'post_list'

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)


def search(request):
    q = request.GET.get('q')   # get方法提交的数据保存在request.GET的字典中
    error_msg = ''
    if not q:
        error_msg = '请输入关键词'
        return render(request, 'blog/index.html', {'error_msg': error_msg})
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    # icontains为查询表达式，用法：模型属性后面跟两个下划线
    return render(request, 'blog/index.html', {'error_msg': error_msg,
                                               'post_list': post_list})
