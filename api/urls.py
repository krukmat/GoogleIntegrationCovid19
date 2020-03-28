from rest_framework.routers import DefaultRouter
from django.conf.urls import url, include
from api.views import (
	PingView, ScrapeView, UserViewSet, OrganizationViewSet, TeamViewSet,
	KpiList, KpiDetail, KpiValueList, KpiValueDetail,
)

# This two if you want to enable the Django Admin: (recommended)
from django.contrib import admin
admin.autodiscover()

user_list = UserViewSet.as_view({
    'get': 'list'
})

user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})

organization_list = OrganizationViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

organization_detail = OrganizationViewSet.as_view({
	'get': 'retrieve',
	'put': 'update',
	'patch': 'partial_update',
	'delete': 'destroy'
})

team_list = TeamViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

team_detail = TeamViewSet.as_view({
	'get': 'retrieve',
	'put': 'update',
	'patch': 'partial_update',
	'delete': 'destroy'
})

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'organizations', OrganizationViewSet)
router.register(r'teams', TeamViewSet)

urlpatterns = [
	url(r'^', include(router.urls)),
	url(r'ping/$', PingView.as_view(), name='ping'),
	url(r'scrape/$', ScrapeView.as_view(), name='scrape'),
	url(r'^auth/', include('rest_framework.urls', namespace='rest_framework'))
]