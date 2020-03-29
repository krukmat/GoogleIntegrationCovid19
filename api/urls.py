from rest_framework.routers import DefaultRouter
from django.conf.urls import url, include
from api.views import (
	PingView, ScrapeView
)

# This two if you want to enable the Django Admin: (recommended)
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
	url(r'^', include(router.urls)),
	url(r'ping/$', PingView.as_view(), name='ping'),
	url(r'scrape/$', ScrapeView.as_view(), name='scrape'),
	url(r'^auth/', include('rest_framework.urls', namespace='rest_framework'))
]