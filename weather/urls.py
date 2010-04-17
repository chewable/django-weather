from django.conf.urls.defaults import *

urlpatterns = patterns('',
	(r'^/?$', 'bpaulson.weather.views.index', {}, 'index'),
)