# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-24 20:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('discussion', '0002_discussion_organization'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(help_text='The attached file.', upload_to='discussion/attachments')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('extra', jsonfield.fields.JSONField(blank=True, help_text='Additional information stored with this object.')),
                ('comment', models.ForeignKey(blank=True, help_text='The Comment that this Attachment is attached to. Null when the file has been uploaded before the Comment has been saved.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='discussion.Comment')),
            ],
        ),
        migrations.AlterField(
            model_name='discussion',
            name='guests',
            field=models.ManyToManyField(blank=True, help_text="Additional Users who are participating in this chat, besides those that are implicit discussion members via the Discussion's attached_to object.", to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='attachment',
            name='discussion',
            field=models.ForeignKey(help_text='The Discussion that this Attachment is attached to.', on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='discussion.Discussion'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='user',
            field=models.ForeignKey(help_text='The user uploading this attachment.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
