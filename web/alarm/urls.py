from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^mail$', views.mail, name='mail'),
    url(r'^sms$', views.sms, name='sms'),
]
