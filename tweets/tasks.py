from datetime import timedelta

from django.conf import settings
from django.core.management import call_command

from celery.task import periodic_task


@periodic_task(run_every=timedelta(minutes=settings.TWEET_INTERVAL_MINUTES))
def tweet_next_task():
    call_command('tweet_next', verbose=True, interactive=False)
