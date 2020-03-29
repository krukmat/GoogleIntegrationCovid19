from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import permissions

from .mixins import JSONResponseMixin
from api.models import Organization, Team, Kpi, KpiValue
from api.serializers import (
	UserSerializer, OrganizationSerializer, 
	TeamSerializer, KpiSerializer, KpiValueSerializer,
)
from googlesearch import search 
import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud, STOPWORDS

@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'organizations': reverse('organization-list', request=request, format=format),
		'teams': reverse('team-list', request=request, format=format),
    })

class PingView(APIView):

	def get(self, request):
		"""
		Just responds with Pong
		"""
		data = {'ping': 'pong'}

		return JSONResponseMixin(data)
	
class ScrapeView(APIView):
	def get(self, request):
		email = request.query_params.get('email')
		firstname = request.query_params.get('firstname')
		lastname = request.query_params.get('lastname')
		name = request.query_params.get('name')
		query = email + ' OR '+name
		result = []
		#filtering
		blacklistTokens = [
			'[document]',
			'noscript',
			'header',
			'html',
			'meta',
			'head', 
			'input',
			'script',
			'\n'
			'style'
		]
		output = ''
		for j in search(query, tld="com", num=10, stop=10, pause=2): 
			url = j 
			res = requests.get(url)
			html_page = res.content
			soup = BeautifulSoup(html_page, 'html.parser')
			text = soup.find_all(text=True)
			blacklistWords = []
			blacklistWords.append(string.lower(firstname))
			blacklistWords.append(string.lower(lastname))
			blacklistWords.append(string.lower(firstname) + ' ' + string.lowe(lastname))
			blacklistWords.append(string.lower(lastname) + ' ' + string.lower(firstname))
			blacklistWords.append('twitter')
			blacklistWords.append('facebook')
			blacklistWords.append('instagram')
			blacklistWords.append('tweet')
			blacklistWords.append('like')
			blacklistWords.append('follow')
			blacklistWords.append(string.lower(email))
			for t in text:				
				if t.parent.name not in blacklistTokens and not any([any(string.lower(str) in string.lower(s) for s in blacklistWords) for str in t.split()]) :
					output += '{} '.format(t)
		#word cloud
		wordcloud = WordCloud().process_text(output)
		wordcloud = {k: v for k, v in sorted(wordcloud.items(), key=lambda item: item[1], reverse=True)}
		return JSONResponseMixin(wordcloud)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer

class OrganizationViewSet(viewsets.ModelViewSet):
	queryset = Organization.objects.all()
	serializer_class = OrganizationSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

	def perform_create(self, serializer):
		serializer.save(owner=self.request.user)		

class TeamViewSet(viewsets.ModelViewSet):
	queryset = Team.objects.all()
	serializer_class = TeamSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)	


#TODO: The views below could be transformed into viewsets later

class KpiList(generics.ListCreateAPIView):
	queryset = Kpi.objects.all()
	serializer_class = KpiSerializer

class KpiDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Kpi.objects.all()
	serializer_class = KpiSerializer

class KpiValueList(generics.ListCreateAPIView):
	queryset = KpiValue.objects.all()
	serializer_class = KpiValueSerializer

class KpiValueDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = KpiValue.objects.all()
	serializer_class = KpiValueSerializer