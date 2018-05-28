from django.conf.urls import url
from . import views   # .为当前目录下

app_name = 'blog'   # 视图函数命名空间，区分以下函数只作用于blog项目
urlpatterns = [
    url('post/(?P<pk>[0-9]+)/', views.PostDetailView.as_view(), name='detail'),
    # 正则表达式匹配以post/开头，后跟一个至少一位数的数字，并且以/符号结尾
    # 正则式()里面为提取参数，传给视图detail函数
    url('archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/', views.ArchivesView.as_view(), name='archives'),
    url('category/(?P<pk>[0-9]+)/', views.CategoryView.as_view(), name='category'),
    url('tag/(?P<pk>[0-9]+)/', views.TagView.as_view(), name='tag'),
    url('', views.IndexView.as_view(), name='index'),   # as_views()将类转换为函数
    url(r'^search/$', views.search, name='search'),   # 将视图函数映射到url
    # url('', views.index, name='index'),
    # 网址参数（正则表达式）/处理函数/起个别名，便于操作
]