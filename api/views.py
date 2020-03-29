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
from nltk.corpus import stopwords
import nltk
from textblob import TextBlob

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
			'style',
			'header'
		]
		output = ''
		returnlist = []
		for j in search(query, tld="com", num=10, stop=10, pause=2): 
			url = j 
			res = requests.get(url)
			html_page = res.content
			soup = BeautifulSoup(html_page, 'html.parser')
			text = soup.find_all(text=True)
			whitelist = ['covid', 'hiv', 'epidemiology', 'infection', 'disease', 'microbiology', 'protein', 'molecul', 'bioengineering', 'malaria', 'measles', 'neumonia']
			blacklistWords = []
			blacklistWords.append(firstname.lower())
			blacklistWords.append(lastname.lower())
			blacklistWords.append(firstname.lower() + ' ' + lastname.lower())
			blacklistWords.append(lastname.lower() + ' ' + firstname.lower())
			blacklistWords.append('twitter')
			blacklistWords.append('facebook')
			blacklistWords.append('instagram')
			blacklistWords.append('tweet')
			blacklistWords.append('like')
			blacklistWords.append('retweet')
			blacklistWords.append('follow')
			blacklistWords.append(email.lower())
			output = ''
			#
			for t in text:				
				if t.parent.name not in blacklistTokens and any([any(str.lower() in s for s in whitelist) for str in t.split()]) and not any([any(str.lower() in s for s in blacklistWords) for str in t.split()]) and  not any([str in stopwords.words('english') for str in t.split()]):
					output += '{} '.format(t)

			#noun extraction
			blob = TextBlob(output)
			output = ' '.join(blob.noun_phrases) 
			#word cloud
			wordcloud = WordCloud().process_text(output)
			wordcloud = {k: v for k, v in sorted(wordcloud.items(), key=lambda item: item[1], reverse=True)}
			if wordcloud:
				returnlist.append(dict(cloud=wordcloud, url=url))
		return JSONResponseMixin(returnlist)