# LinkTest

链路监控 agent 客户端，结构为C/S结构。
- agent server(web Server): 通过第三方厂家API接口获取HTTP代理地址池，通过POST方式分发任务
- agent client(web Server): 接受任务后，添加定制化的headers，通过HTTP代理，访问测试站点。
