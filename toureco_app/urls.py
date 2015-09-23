from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^/?$', views.index, name='index'),
    url(r'^tour/?$', views.welcome, name='welcome'),
    url(r'^tour/step/(?P<next_count>[0-9]+)$', views.choice, name='choice')
]
