from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Tweet
from django.urls import reverse

User = get_user_model()
class TweetModelTestCase(TestCase):
    # METHOD 1
    def setUp(self):
        some_random_user = User.objects.create(username = 'chrispsk33333')
    # METHOD 2
    def test_tweet_item(self):
        obj = Tweet.objects.create(
            user = User.objects.first(),
            content = 'Some random content'
        )
        self.assertTrue(obj.content=='Some random content')
        self.assertTrue(obj.id==1)
        self.assertEqual(obj.id,1)
        absolute_url = reverse("detail", kwargs={"pk":1})
        self.assertEqual("/tweet/1",absolute_url)

    def test_tweet_url(self):
        obj = Tweet.objects.create(
            user = User.objects.first(),
            content = 'Some random content'
        )
        absolute_url = reverse("detail", kwargs={"pk":obj.pk})
        self.assertEqual("/tweet/1",absolute_url)
