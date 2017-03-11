import re

import tweepy


class TwitterBotException(Exception):
    pass


def escape_sms_commands(text):
    """
    Twitter allow 'special commands' to be sent via a tweet:
     https://support.twitter.com/articles/14020
    Since any tweet starting with these commands will try to run the command
     rather than actually updating our status, we need to turn off this behavior
     by adding a fancy zero-width whitespace character in front of our text.
    See: http://stackoverflow.com/questions/19969275
    """
    pattern = re.compile(
        r'^(ON|OFF|FOLLOW|F|UNFOLLOW|LEAVE|L|STOP|QUIT|END|CANCEL|'
        r'UNSBSCRIBE|ARRET|D|M|RETWEET|RT|SET|WHOIS|W|GET|G|FAV|FAVE|'
        r'FAVORITE|FAVORITE|\*|STATS|SUGGEST|SUG|S|WTF|HELP|INFO|AIDE|'
        r'BLOCK|BLK|REPORT|REP)(\W)(.*)', re.I)
    text = re.sub(pattern, '\\1\u200B\\2\\3', text)
    return text


class TwitterAPI(object):
    """
    Handler for the Twitter API. Useful to make tweets for an account.

    The following environment variables must be set to use:

        TWITTER_CONSUMER_KEY
        TWITTER_CONSUMER_SECRET
        TWITTER_ACCESS_KEY
        TWITTER_ACCESS_SECRET

    For more information on obtaining keys, see:

        https://dev.twitter.com/oauth/overview/application-owner-access-tokens

    Usage:

        `api = TwitterAPI()`
        `api.tweet('My First Tweet!')`
    """

    def __init__(self, consumer_key=None, consumer_secret=None,
                 access_key=None, access_secret=None):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_key = access_key
        self.access_secret = access_secret

        if any(i is None for i in (self.consumer_key, self.consumer_secret,
                                   self.access_key, self.access_secret)):
            raise TwitterBotException('Following values must be set to use:\n'
                                      '\tconsumer_key\n'
                                      '\tconsumer_secret\n'
                                      '\taccess_key\n'
                                      '\taccess_secret')

        self.api = self.get_api()

    def get_auth(self):
        auth = tweepy.OAuthHandler(
            self.consumer_key,
            self.consumer_secret,
        )
        auth.set_access_token(
            self.access_key,
            self.access_secret,
        )
        return auth

    def get_api(self):
        auth = self.get_auth()
        return tweepy.API(auth)

    @staticmethod
    def clean_text(text):
        """
        Prepares a string to be tweeted:

        - Validate input
        - Escape SMS commands (https://support.twitter.com/articles/14020)
        - Truncate to 140 characters
        """
        # Make sure we have a string
        if not isinstance(text, str):
            raise TwitterBotException('Can only tweet strings.')

        # Text should have content
        text = text.strip()
        if not text:
            raise TwitterBotException('Text has no content.')

        # Escape SMS commands
        text = escape_sms_commands(text)

        # Truncate to 140 characters
        text = text[:140]
        return text

    def tweet(self, text):
        # Prepare our text for tweeting (truncate to 140 chars, etc.)
        text = self.clean_text(text)

        # Send our tweet
        api = self.get_api()
        api.update_status(status=text)
