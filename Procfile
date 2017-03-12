web: gunicorn config.wsgi:application
worker: celery beat --app=tweeter.taskapp --loglevel=info -S django
