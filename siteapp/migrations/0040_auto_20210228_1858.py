# Generated by Django 3.1.7 on 2021-02-28 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siteapp', '0039_auto_20210120_1739'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(help_text='Label for tag', max_length=100, unique=True)),
                ('system_created', models.BooleanField(default=True)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]