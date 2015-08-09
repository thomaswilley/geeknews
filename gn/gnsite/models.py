from django.db import models
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse
from urllib.parse import urlparse
from django.utils import timezone

class Post(models.Model):
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_modified = models.DateTimeField(auto_now=True)
    op = models.ForeignKey(User, related_name="posts")
    title = models.CharField(max_length=200)
    desc = models.TextField(max_length=1000, blank=True)
    link = models.URLField(max_length=1000, blank=True)
    votes = models.ManyToManyField(User, related_name='votes')
    parent = models.ForeignKey("self", related_name="comments", blank=True, null=True)

    def __str__(self):
        return self.title

    def total_num_comments(self):
        num_comments = len(self.comments.all())
        for c in self.comments.all():
            num_comments += c.total_num_comments()
        return num_comments

    def get_domain_only(self):
        parsed_uri = urlparse(self.link)
        domain = '{uri.netloc}'.format(uri=parsed_uri)
        return domain

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.pk})

    def get_score(self):
        votes = self.votes.all().count()
        item_hour_age = (timezone.now() - self.dt_created).seconds / 60 / 60
        gravity = 1.8
        score = (votes - 1) / pow((item_hour_age + 2), gravity)
        return score
