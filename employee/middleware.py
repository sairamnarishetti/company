from django.http import JsonResponse


class MyMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
        print("hi im middle ware")
        
    def __call__(self,req):
        print('berfore  all')
        response = self.get_response(req) 
        print('after view')
        return response  
