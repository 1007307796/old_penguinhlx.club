from haystack import indexes
from .models import Post


# haystack规定必须创建一个[数据模型+Index]的类，并继承SearchIndex和Indexable
class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)   # 设置关键字

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
