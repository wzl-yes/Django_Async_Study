from django.shortcuts import render
from django.views import View
import requests
from asgiref.sync import sync_to_async, async_to_sync
from django.http.response import HttpResponse
import threading
import asyncio
from django.views.decorators.http import require_GET

# Create your views here.


async def index(request):
    return render(request, 'index.html')


class AboutView(View):
    async def get(self, request):
        return render(request, 'about.html')


class BaiduView(View):
    async def ado_something(self):
        await asyncio.sleep(1)
        print('ado_something')
        return "done"

    def get_baidu_page(self):
        print("子线程名称：", threading.current_thread().name)
        # requests：pip install requests
        resp = requests.get("https://www.baidu.com")
        do_something = async_to_sync(self.ado_something)
        result = do_something()
        print("result:", result)
        return resp.text

    async def get(self, request):
        # get函数是在主线程中
        print("主线程名称：", threading.current_thread().name)
        # 先将同步函数转换为异步
        aget_baidu_page = sync_to_async(self.get_baidu_page)
        html = await aget_baidu_page()
        return HttpResponse(html)


def sync_view(request):
    print('同步视图')
    return HttpResponse("同步视图")


async def async_view(request):
    print('异步视图')
    return HttpResponse("异步视图")
