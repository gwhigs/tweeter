from django.core.management import call_command

from celery import shared_task


@shared_task()
def tweet_next_task():
    call_command('tweet_next', verbose=True, interactive=False)
