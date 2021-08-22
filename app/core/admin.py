from django.contrib import admin
from core.models.idea import Idea
from core.models.user_following import UserFollowing

# Register your models here.
admin.site.register(Idea)
admin.site.register(UserFollowing)
