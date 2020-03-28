# Salesforce: Google searcher integration

This is a django rest framework api to allow Salesforce do searches in google based on tokens to search 

# Live demo here:

soon

# To deploy to heroku

```bash
$ heroku create mydashboard
$ git push heroku master
$ heroku config:set DJANGO_SETTINGS_MODULE=agileteamskpisapi.settings
$ heroku run python manage.py migrate
$ heroku run python manage.py createsuperuser
$ heroku ps:scale web=1
```



