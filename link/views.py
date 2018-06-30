from django.shortcuts import render,HttpResponse,redirect

# Create your views here.


def index(request):
    if request.method == 'GET':
        return render(request,'login.html')