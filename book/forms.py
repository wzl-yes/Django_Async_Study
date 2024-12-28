from django import forms
from pyexpat.errors import messages

from .models import Book


# 如果表单中，要查找数据库（要做同步的I/O操作），那么有两种解决方法
# 1. 把查找数据库的操作，移到视图函数中。
# 2. 在表单中写同步I/O操作代码，到时候在异步视图中，再使用sync_to_async，将表单验证的操作转换成异步的
class AddBookForm(forms.Form):
    name = forms.CharField(min_length=1, max_length=100)
    author = forms.CharField(min_length=1, max_length=80, error_messages={'required': '请输入作者！'})
    price = forms.FloatField(error_messages={'required': "请输入价格！"})

    def clean_name(self):
        name = self.cleaned_data.get('name')
        # 同步的I/O操作
        if Book.objects.filter(name=name).exists():
            raise forms.ValidationError('图书已存在')
        return name
