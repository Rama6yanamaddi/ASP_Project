# Generated by Django 2.1 on 2018-09-29 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myfinances', '0004_auto_20180203_2257'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='importconfiguration',
            name='default_account',
        ),
        migrations.AddField(
            model_name='account',
            name='iban',
            field=models.CharField(blank=True, max_length=34, null=True),
        ),
        migrations.DeleteModel(
            name='ImportConfiguration',
        ),
    ]
