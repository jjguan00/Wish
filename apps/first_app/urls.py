from django.conf.urls import url
from . import views

urlpatterns=[
	url(r'^$', views.index),
	url(r'^signups$', views.signups),
	url(r'^logins$', views.logins),
	url(r'^logOut$', views.logOut),
	url(r'^new$', views.new),
	url(r'^wishes$', views.wishes),
	url(r'^makeWish$', views.makeWish),
	url(r'^remove/(?P<number>\d+)$', views.remove),
	url(r'^edit/(?P<number>\d+)$', views.edit),
	url(r'^editWish/(?P<number>\d+)$', views.editWish),
	url(r'^grant/(?P<number>\d+)$', views.grantWish),
	url(r'^stats$', views.stats),
	url(r'^like/(?P<number>\d+)$', views.like)
]