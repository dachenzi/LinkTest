import random
import requests
import time
import json


def auto_task(url_file, available_proxy, agent_list, url_address):
    while True:
        with open(url_file, encoding='utf-8') as f:
            flag = f.read().split('\n')[0]
        if flag == 'start':
            agent_ip, agent_port, agent_api = random.choice(agent_list)
            proxy_ip, proxy_address = random.choice(available_proxy)
            agent_url = 'http://{}:{}{}'.format(agent_ip, agent_port, agent_api)
            data = {'proxy_ip': proxy_ip, 'proxy_address': proxy_address, 'url_address': url_address}
            response = requests.post(agent_url, data=json.dumps(data))
            print(agent_url, data)
            time.sleep(3)
        else:
            break


