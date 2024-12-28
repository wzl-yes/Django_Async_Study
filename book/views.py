from .forms import AddBookForm
from asgiref.sync import sync_to_async
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from .models import Book
from django.views import View


async def add_book(request):
    if request.method == 'GET':
        return render(request, 'add_book.html')
    else:
        # 写一个表单验证数据
        form = AddBookForm(request.POST)
        # 因为在AddBookForm中，我们验证name的时候，用了同步的I/O操作方法
        # 所以这里，不能直接调用is_valid()方法，否则里面的同步I/O操作方法就会阻塞事件循环
        # 解决方法，就是用使用sync_to_async函数，来将同步代码转换成异步代码
        ais_valid = sync_to_async(form.is_valid)
        if await ais_valid():
            name = form.cleaned_data.get('name')
            author = form.cleaned_data.get('author')
            price = form.cleaned_data.get('price')
            # print(name, author, price)
            # return HttpResponse("表单验证成功！")
            # 1. 先创建对象，再保存
            # book = Book(name=name, author=author, price=price)
            # await book.asave()
            # 2. 直接创建并保存
            book = await Book.objects.acreate(name=name, author=author, price=price)
            return redirect(reverse('book:book_detail', kwargs={"pk": book.id}))

        else:
            print(form.errors)
            return HttpResponse("表单验证失败！")


async def book_detail(request, pk):
    try:
        book = await Book.objects.aget(pk=pk)
        return render(request, 'book_detail.html', context={"book": book})
    except Exception as e:
        print(e)
        return HttpResponse("图书id不存在！")


class BookListView(View):
    async def get(self, request):
        queryset = Book.objects.all()
        # 针对这种QuerySet对象，只有通过异步迭代，async for来异步查找数据
        books = []
        async for book in queryset:
            books.append(book)
        return render(request, 'book_list.html', context={"books": books})
