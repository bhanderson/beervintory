from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'floors', views.floors, name='floors'),
        url(r'floor/(?P<id>[0-9]+)/$', views.floor, name='floor'),
        url(r'kegerators', views.kegerators, name='kegerators'),
        url(r'kegerator/(?P<id>[0-9]+)/$', views.kegerator, name='kegerator'),
        url(r'styles', views.styles, name='styles'),
        url(r'style/(?P<id>[0-9]+)/$', views.style, name='style'),
        url(r'brewers', views.brewers, name='brewers'),
        url(r'brewer/(?P<id>[0-9]+)/$', views.brewer, name='brewer'),
        url(r'beers', views.beers, name='beers'),
        url(r'beer/(?P<id>[0-9]+)/$', views.beer, name='beer'),
        ]