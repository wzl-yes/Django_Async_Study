from django.urls import path
from . import views

app_name = 'front'

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.AboutView.as_view(), name='about'),
    path('baidu', views.BaiduView.as_view(), name='baidu'),
    path('sync', views.sync_view, name='sync_view'),
    path('async', views.async_view, name='async_view'),

]
