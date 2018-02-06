# url_check
url监控
    
## agent  
pycurl+msgpackrpc client获取url状态     
    
## web    
django+msgpackrpc server将client数据保存到beanstalk队列中，同时提供url列表
    
## alarm    
将beanstalk中的信息，添加到influxdb中，同时提供报警功能    
    
## 后台展现功能    
使用grafana来读到数据库，展示图表信息    
![image](https://github.com/akin520/url_check/blob/master/image/grafna.png?raw=true)