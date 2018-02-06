# url_check
url监控
    
##agent    
pycurl+msgpackrpc client获取url状态   
    
##web    
django+msgpackrpc server将client数据保存到beanstalk队列中
    
##alarm    
将beangstalk中的信息，添加到influxdb中，同时提供报警功能    
    
##后台展现功能    
使用granfa来读到数据库