from asgiref.sync import iscoroutinefunction, markcoroutinefunction
from django.utils.decorators import (
    sync_only_middleware,
    async_only_middleware,
    sync_and_async_middleware
)


# @sync_and_async_middleware
@async_only_middleware
# @sync_only_middleware
def simple_middleware(get_response):
    if iscoroutinefunction(get_response):
        async def middleware(request):
            print("视图执行之前 async simple middleware")
            response = await get_response(request)
            print('视图执行之后 async simple middleware')
            return response
    else:
        def middleware(request):
            print("视图执行之前 sync simple middleware")
            response = get_response(request)
            print('视图执行之后 sync simple middleware')
            return response
    return middleware


class AsyncMiddleware:
    # 支持异步
    async_capable = True
    sync_capable = False

    def __init__(self, get_response):
        self.get_response = get_response
        if iscoroutinefunction(self.get_response):
            markcoroutinefunction(self)

    async def __call__(self, request):
        # 执行视图函数之前的代码
        print('异步中间件 执行视图之前')
        response = await self.get_response(request)
        # 执行视图函数之后的代码
        print('异步中间件 执行视图之后')
        return response
