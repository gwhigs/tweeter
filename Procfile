web: gunicorn config.wsgi:application
worker: celery worker --app=tweeter.taskapp --loglevel=info
