from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):   # 利用django自带的表格类
    class Meta:   # 定义包含表单信息的类
        model = Comment
        fields = ['name', 'email', 'url', 'text']