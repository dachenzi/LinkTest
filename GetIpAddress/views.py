import requests
import json
import configparser
import os
import time
from django.shortcuts import render, HttpResponse, redirect
from django.conf import settings
from GetIpAddress import models
from GetIpAddress import cron
from django.forms import Form
from django.forms import fields
from django.forms import widgets
from multiprocessing import Process
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
    Api = fields.CharField(
        max_length=32,
        error_messages={'required': 'Api接口不能为空',
                        'max_length': 'Api接口不能超过32位'},
        widget=widgets.TextInput(attrs={'class': 'form-control', 'id': 'Api', 'placeholder': "/api/index.html",
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


class LoginCheck(Form):   # 登陆时的form表单验证
    username = fields.CharField(
        error_messages={'required':'用户名不能为空'},
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '用户名'})
    )
    password = fields.CharField(
        error_messages={'required':'密码不能为空'},
        widget=widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': '密 码'})
    )


def update_http_proxy():
    ret_code = {'status': True, 'msg': ""}
    cp = configparser.ConfigParser()
    cp.read(settings.API_FILE)
    api_address = cp.get('api', 'api_address')
    try:
        response = requests.get(api_address)
        response = json.loads(response.text, encoding='UTF-8')
        # print(response)
        if response['success'] == 'true':
            http_proxy_list = response['data']
            for http_proxy in http_proxy_list:
                models.HttpProxyInfo.objects.create(**http_proxy)
                ret_code['status'] = True
        else:
            ret_code['status'] = False
            ret_code['msg'] = response['msg']
            # print(ret_code)
        return ret_code
    except Exception as e:
        ret_code['status'] = False
        return ret_code


def login(request):

    # 定义返回数据字典
    ret_code = {'status': True, 'error_msg': {}}

    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        lc = LoginCheck(data=request.POST)
        if lc.is_valid():
            user = lc.cleaned_data['username']
            pwd = lc.cleaned_data['password']
            user_obj = models.UserLogin.objects.filter(UserName=user, Password=pwd)
            if not user_obj:
                ret_code['status'] = False
                ret_code['error_msg'] = {}  # 初始化错误信息
                ret_code['error_msg']['username'] = '用户名或密码不正确！'
            else:
                request.session['user'] = user
                request.session['time_login'] = '本次登陆时间: {}'.format(time.strftime('%Y-%m-%d %H:%M:%S'))
                return redirect('/')
        else:
            ret_code['status'] = False
            ret_code['error_msg'] = lc.errors  # 返回错误信息

        return HttpResponse(json.dumps(ret_code))


def logout(request):

    if request.method == 'GET':
        request.session.clear()

        return redirect('/login.html')




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
        paginator = Paginator(available_proxy, 20)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
        return render(request, 'proxy_info.html', {'available_proxy': contacts})


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
                agent_url = 'http://{}:{}/auth/'.format(agent_add.cleaned_data['AgentIP'],
                                                       agent_add.cleaned_data['AgentPort'])

                # 添加agent时，发送key到agent进行验证(重试3次）
                retry = 0
                print(agent_url)
                while retry <= 3:
                    try:
                        response = requests.get(agent_url, params={'key': agent_add.cleaned_data['Key']}, timeout=3)
                        result = json.loads(response.text)['status']
                        if result:
                            break
                        retry += 1
                    except Exception as e:
                        retry += 1
                        continue
                else:
                    ret_code['status'] = False
                    ret_code['err_msg'] = {}
                    ret_code['err_msg'] = {'invalid': 'Agent 无响应，请确认Agent地址'}
                    return HttpResponse(json.dumps(ret_code))
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
        res = update_http_proxy()
        return HttpResponse(json.dumps(res))


def task_info(request):
    ret_code = {'status': True}

    if request.method == 'GET':
        available_url = models.UrlInfo.objects.filter(Used=0)
        return render(request, "task_info.html", {'available_url': available_url})

    if request.method == 'POST':
        res = request.POST.get('status', None)
        if res:
            url_id = request.POST.get('id')
            models.UrlInfo.objects.filter(id=url_id).update(Checked=int(res))
            url_address = models.UrlInfo.objects.filter(id=url_id).first().UrlAddress
            url_name = url_address.split('/')[2]
            url_file = "{}{}{}-{}".format(settings.HTTP_DATA, os.path.sep, url_id, url_name)
            with open(url_file, 'w') as f:
                if res == '0':
                    flag = 'stop'
                elif res == '1':
                    flag = 'start'
                f.write(flag)
            http_proxy_list = models.HttpProxyInfo.objects.filter(Used=0)
            agent_list = list(models.AgentInfo.objects.filter(Used=0).values_list('AgentIP', 'AgentPort', 'Api'))
            available_proxy = []
            for http_proxy in http_proxy_list:
                expire = time.mktime(time.strptime(http_proxy.ExpireTime, '%Y-%m-%d %H:%M:%S'))
                if expire < time.time():
                    models.HttpProxyInfo.objects.filter(id=http_proxy.id).update(Used=1)
                else:
                    available_proxy.append((http_proxy.IP, http_proxy.IpAddress))
            p = Process(target=cron.auto_task, args=(url_file, available_proxy, agent_list, url_address))
            p.start()
        return HttpResponse(json.dumps(ret_code))
