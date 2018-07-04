from django.db import models

# Create your models here.


class HttpProxyInfo(models.Model):
    IP = models.GenericIPAddressField(verbose_name='HTTP代理地址')
    ISP = models.CharField(max_length=32, verbose_name='ISP')
    ExpireTime = models.CharField(max_length=32, verbose_name='过期时间')
    IpAddress = models.CharField(max_length=32, verbose_name='归属地')
    Used = models.IntegerField(default=0)


class AgentInfo(models.Model):
    AgentName = models.CharField(max_length=16, verbose_name='客户端名称')
    AgentIP = models.GenericIPAddressField(max_length=16, verbose_name='客户端地址')
    AgentPort = models.IntegerField(max_length=16, verbose_name='端口', default=0)
    Api = models.CharField(max_length=16, verbose_name='客户端API接口')
    Key = models.CharField(max_length=32, verbose_name='认证key信息')
    Used = models.IntegerField(default=0)


class UrlInfo(models.Model):
    UrlName = models.CharField(max_length=16, verbose_name='Url名称')
    UrlAddress = models.CharField(max_length=128, verbose_name='Url地址')
    Used = models.IntegerField(default=0)
    Checked = models.IntegerField(default=0)


class UserLogin(models.Model):
    UserName = models.CharField(max_length=16, verbose_name='用户名')
    Password = models.CharField(max_length=16, verbose_name='密码')
    Status = models.IntegerField(verbose_name='账号状态')