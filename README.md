# Salesforce: Google searcher integration

This is a django rest framework api to allow Salesforce do searches in google based on tokens to search. The intention is to do searches of data based on scientific profiles from emails and fullnames to search expanded information  

# Live demo here:

soon

# To deploy to heroku

```bash
$ heroku create mydashboard
$ git push heroku master
$ heroku config:set DJANGO_SETTINGS_MODULE=coronaapi.settings
$ heroku run python manage.py migrate
$ heroku run python manage.py createsuperuser
$ heroku ps:scale web=1
```



