web: gunicorn config.wsgi:application
worker: celery worker -B --app=tweeter.taskapp --loglevel=info
