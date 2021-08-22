from django.db import models
from django.contrib.auth.models import User

STATUS_CHOICES = [
    ('p', 'Pending'),
    ('a', 'Approved'),
    ('d', 'Denied'),
]


class UserFollowing(models.Model):

    user = models.ForeignKey(
        to=User,
        related_name="following",
        on_delete=models.CASCADE
    )
    following_user = models.ForeignKey(
        to=User,
        related_name="followers",
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following_user'], name='Unique follow')
        ]
