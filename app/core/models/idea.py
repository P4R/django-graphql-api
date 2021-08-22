from django.db import models
from django.contrib.auth.models import User

VISIBILITY_CHOICES = [
    ('pub', 'Public'),
    ('pro', 'Protected'),
    ('pri', 'Private'),
]


class Idea(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, blank=False, null=False)
    visibility = models.CharField(max_length=3, choices=VISIBILITY_CHOICES)
    pub_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        to=User,
        related_name="idea",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title
