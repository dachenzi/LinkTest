from django.shortcuts import render,HttpResponse,redirect
import requests
import json
import configparser
from django.conf import settings
from GetIpAddress import models
# Create your views here.


def update_http_proxy():
    cp = configparser.ConfigParser()
    cp.read(settings.API_FILE)
    api_address = cp.get('api', 'api_address')
    response = requests.get(api_address)
    http_proxy_list = json.loads(response.text)['data']
    for http_proxy in http_proxy_list:
        models.HttpProxyInfo.objects.create(**http_proxy)


def index(request):

    if request.method == 'GET':
        available_proxy = len(models.HttpProxyInfo.objects.filter(Used=0))
        print(available_proxy)
        return render(request, 'main_page.html', {'data': None})

