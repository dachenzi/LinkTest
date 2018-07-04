from django.utils.deprecation import MiddlewareMixin         # 引入MiddlewareMixin类
from django.shortcuts import redirect


class Auth(MiddlewareMixin):

    def process_request(self, request):
        if request.path_info == '/login.html':
            return None
        if not request.session.get('user', None):
            return redirect('/login.html')
