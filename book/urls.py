from django.urls import path
from . import views

app_name = 'book'

urlpatterns = [
    path('add', views.add_book, name='add_book'),
    path('detail/<int:pk>', views.book_detail, name='book_detail'),
    path('list', views.BookListView.as_view(), name='book_list')
]
