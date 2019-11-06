from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

def validate_content(value):
    content = value
    if content == "":
        raise ValidationError("Content Cannot be blank")
    return value

class Tweet(models.Model):
    # Tweets must be associated to a user
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=140, validators=[validate_content])
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.content)

    # def clean(self, *args, **kwargs):
    #     content = self.content
    #     if content == "abc":
    #         raise ValidationError("Content Cannot be ABC")
    #     return super(Tweet, self).clean(*args,**kwargs)
