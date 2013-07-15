from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

# Create your models here.

class LinkPost(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    dateCreated = models.DateTimeField()
    dateAccessed = models.DateTimeField(null=True, blank=True)
    note = models.TextField(blank=True)
    user = models.ForeignKey(User)
    preview = models.ImageField(null=True, upload_to='linklist')

    class Meta:
        verbose_name_plural = "LinkPosts"

    def __str__(self):
        return self.title


class Keyword(models.Model):
    keyword = models.CharField(max_length=30)
    linkpost = models.ForeignKey('LinkPost')

    class Meta:
        verbose_name_plural = "Keywords"

    def __str__(self):
        return self.keyword

