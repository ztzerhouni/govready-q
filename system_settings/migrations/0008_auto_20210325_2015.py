# Generated by Django 3.1.7 on 2021-03-25 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system_settings', '0007_auto_20210324_2310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classification',
            name='status',
            field=models.CharField(choices=[('UNCLASSIFIED', 'unclassified'), ('CONFIDENTIAL', 'confidential'), ('SECRET', 'secret'), ('TOPSECRET', 'top secret')], default='UNCLASSIFIED', max_length=32),
        ),
    ]