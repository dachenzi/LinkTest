from django.shortcuts import render,HttpResponse,redirect
import requests
import configparser
# Create your views here.


def get_ip_address(request):

    if request.method == 'GET':
        cp = configparser.ConfigParser()
        cp.read('../../conf/api.properties')
        print(cp.sections())
        # api_address = cp.get('Default', 'api_address')
        # print(api_address)
