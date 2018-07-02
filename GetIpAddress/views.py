from django.shortcuts import render,HttpResponse,redirect
import requests
import json
import configparser
from django.conf import settings
from GetIpAddress import models
from django.forms import Form
from django.forms import fields
from django.forms import widgets
# Create your views here.


class AgentAdd(Form):
    AgentName = fields.CharField(
        max_length=16,
        error_messages={'required': '主机名不能为空',
                        'max_length': '主机名不能超过16位'},
        widget=widgets.TextInput(attrs={'class': 'form-control', 'id': 'AgentName', 'placeholder': "Name",
                                        })
    )
    AgentIP = fields.GenericIPAddressField(
        protocol='ipv4',
        error_messages={'required': 'IP地址不能为空',
                        'invalid': '地址格式不正确'},
        widget=widgets.TextInput(attrs={'class': 'form-control', 'id': 'AgentIP', 'placeholder': " 0.0.0.0",
                                        })
    )
    AgentPort = fields.IntegerField(
        max_value=65535,
        error_messages={'required': '端口不能为空',
                        'invalid': '端口范围错误',
                        'max_value': '最大端口范围为65535'},
        widget=widgets.TextInput(attrs={'class': 'form-control', 'id': 'AgentPort', 'placeholder': " 0",
                                        })
    )
    Key = fields.CharField(
        max_length=16,
        error_messages={'required': 'Key不能为空',
                        'max_length': 'Key不能超过16位'},
        widget=widgets.TextInput(attrs={'class': 'form-control', 'id': 'Key', 'placeholder': "Key",
                                        })
    )


class UrlAdd(Form):
    UrlName = fields.CharField(
        max_length=16,
        error_messages={'required': 'Url名称不能为空',
                        'max_length': 'Url名称不能超过16位'},
        widget=widgets.TextInput(attrs={'class': 'form-control', 'id': 'UrlName', 'placeholder': "名称",
                                        })
    )
    UrlAddress = fields.URLField(
        max_length=128,
        error_messages={'required': 'Url地址不能为空',
                        'max_length': 'Url地址不能超过128位'},
        widget=widgets.TextInput(attrs={'class': 'form-control', 'id': 'UrlAddress', 'placeholder': "http://",
                                         })
    )


def update_http_proxy():
    cp = configparser.ConfigParser()
    cp.read(settings.API_FILE)
    api_address = cp.get('api', 'api_address')
    try:
        response = requests.get(api_address)
        http_proxy_list = json.loads(response.text)['data']
        for http_proxy in http_proxy_list:
            models.HttpProxyInfo.objects.create(**http_proxy)
    except Exception as e:
        pass


def index(request):

    if request.method == 'GET':
        available_proxy = models.HttpProxyInfo.objects.filter(Used=0)
        available_agent = models.AgentInfo.objects.filter(Used=0)
        available_url = models.UrlInfo.objects.filter(Used=0)
        return render(request, 'index.html', {'available_proxy': available_proxy, 'available_agent': available_agent,
                                              'available_url': available_url})


def proxy_index(request):

    if request.method == 'GET':
        available_proxy = models.HttpProxyInfo.objects.filter(Used=0)
        return render(request, 'proxy_info.html', {'available_proxy': available_proxy})


def agent_index(request):

    if request.method == 'GET':
        available_agent = models.AgentInfo.objects.filter(Used=0)
        return render(request, 'agent_info.html', {'available_agent': available_agent})


def add_agent(request):
    ret_code = {'status': True, 'err_msg': {}}

    if request.method == 'GET':
        agent_add = AgentAdd()
        return render(request, 'add_agent.html', locals())

    if request.method == 'POST':
        agent_add = AgentAdd(request.POST)
        if agent_add.is_valid():
            agent_obj = models.AgentInfo.objects.filter(AgentIP=agent_add.cleaned_data['AgentIP'],
                                                        AgentPort=agent_add.cleaned_data['AgentPort'])
            if agent_obj:
                ret_code['status'] = False
                ret_code['err_msg'] = {}
                ret_code['err_msg'] = {'AgentIP': 'IP:Port已存在!'}
            else:
                ret_code['status'] = True
                agent_url = 'http://{}:{}/auth'.format(agent_add.cleaned_data['AgentIP'],
                                                       agent_add.cleaned_data['AgentPort'])
                # retry = 0
                # print(agent_url)
                # while retry <= 3:
                #     try:
                #         response = requests.post(agent_url, data={'key': agent_add.cleaned_data['Key']}, timeout=1)
                #         print(response.text())
                #         if response.text():
                #             break
                #         retry += 1
                #     except Exception as e:
                #         retry += 1
                #         continue
                # else:
                #     ret_code['status'] = False
                #     ret_code['err_msg'] = {}
                #     ret_code['err_msg'] = {'invalid': 'Agent 无响应，请确认Agent地址'}
                #     return HttpResponse(json.dumps(ret_code))
                models.AgentInfo.objects.create(**agent_add.cleaned_data)

        else:
            ret_code['status'] = False
            ret_code['err_msg'] = {}
            ret_code['err_msg'] = agent_add.errors

        return HttpResponse(json.dumps(ret_code))


def delete_agent(request):
    ret_code = {'status': True, 'err_msg': {}}
    if request.method == 'POST':
        agent_id = request.POST.get('id', None)
        if agent_id:
            models.AgentInfo.objects.filter(id=agent_id).delete()
    return HttpResponse(json.dumps(ret_code))


def url_index(request):

    if request.method == 'GET':
        available_url = models.UrlInfo.objects.filter(Used=0)
        return render(request, 'url_info.html', {'available_url': available_url})


def add_url(request):
    ret_code = {'status': True, 'err_msg': {}}

    if request.method == 'GET':
        url_add = UrlAdd()
        return render(request, 'add_url.html', locals())

    if request.method == 'POST':
        print('begin')
        url_add = UrlAdd(request.POST)
        if url_add.is_valid():
            url_obj = models.UrlInfo.objects.filter(UrlAddress=url_add.cleaned_data['UrlName'])
            if url_obj:
                ret_code['status'] = False
                ret_code['err_msg'] = {}
                ret_code['err_msg'] = {'UrlName': 'Url已存在!'}
            else:
                ret_code['status'] = True
                models.UrlInfo.objects.create(**url_add.cleaned_data)
        else:
            ret_code['status'] = False
            ret_code['err_msg'] = {}
            ret_code['err_msg'] = url_add.errors

        return HttpResponse(json.dumps(ret_code))


def delete_url(request):
    ret_code = {'status': True, 'err_msg': {}}
    if request.method == 'POST':
        url_id = request.POST.get('id', None)
        if url_id:
            models.UrlInfo.objects.filter(id=url_id).delete()
    return HttpResponse(json.dumps(ret_code))


def update(request):

    if request.method == 'GET':
        update_http_proxy()
        return HttpResponse('ok')