import requests
from flask import Flask
from flask import request
import json
import time
app = Flask(__name__)


local_ip = '127.0.0.1'
local_port = 8080
key = '12345678'


@app.route('/auth/', methods=['GET'])
def auth():
    ret_code = {'status': True}
    agent_key = request.args.get('key')
    if agent_key != key:
        ret_code['status'] = False
    return json.dumps(ret_code)


@app.route('/api/', methods=['POST'])
def auto_task():

    # 接受服务器端发送的测试数据
    data = json.loads(request.data, encoding='UTF-8')
    proxy_ip = data.get('proxy_ip')
    proxy_address = data.get('proxy_address')
    url_address = data.get('url_address')

    # 完成测试请求
    client_time = str(time.time())
    headers = {'client-ip': local_ip, 'client-time': client_time, 'proxy-address': json.dumps(proxy_address)}
    proxies = {'http': 'http://{}'.format(proxy_ip)}
    try:

        response = requests.get(url_address, headers=headers, proxies=proxies)
        print(response.text)
    except Exception as e:
        print(e)
    return 'Hello world'


if __name__ == '__main__':
    app.run(host=local_ip, port=local_port)
