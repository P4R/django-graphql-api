# Generated by Django 3.2.6 on 2021-08-20 10:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_idea_pub_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userfollowing',
            old_name='following_user_id',
            new_name='following_user',
        ),
        migrations.RenameField(
            model_name='userfollowing',
            old_name='user_id',
            new_name='user',
        ),
    ]
