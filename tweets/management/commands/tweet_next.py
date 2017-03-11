from __future__ import print_function

from django.core.management import BaseCommand
from django.conf import settings

from tweets.twitter_api import TwitterAPI
from tweets.models import Tweet


class Command(BaseCommand):
    """
    Tweets the least most recently created Tweet object that hasn't already been tweeted.
    """
    help = ("Tweets the least most recently created Tweet object that hasn't"
            " already been tweeted.")

    def add_arguments(self, parser):
        parser.add_argument(
            '--verbose',
            action='store_true',
            dest='verbose',
            default=False,
            help='Verbose output',
        )

    def handle(self, *args, **options):
        api = TwitterAPI(
            consumer_key=settings.TWITTER_CONSUMER_KEY,
            consumer_secret=settings.TWITTER_CONSUMER_SECRET,
            access_key=settings.TWITTER_ACCESS_KEY,
            access_secret=settings.TWITTER_ACCESS_SECRET,
        )

        tweet = Tweet.objects.filter(tweeted=False).order_by('created').first()
        if not tweet:
            if options['verbose']:
                print('DONE: Nothing to tweet.')
            return

        text = tweet.text
        api.tweet(text)
        tweet.tweeted = True
        tweet.save()
        if options['verbose']:
            print('DONE: Tweeted:\n{}'.format(text))
