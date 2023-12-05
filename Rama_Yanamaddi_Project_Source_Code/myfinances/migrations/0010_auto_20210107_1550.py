# Generated by Django 3.1.5 on 2021-01-07 15:50

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myfinances', '0009_auto_20190204_1925'),
    ]

    operations = [
        migrations.AddField(
            model_name='importfile',
            name='account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='myfinances.account'),
        ),
        migrations.AddField(
            model_name='importfile',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='importfile',
            name='importer',
            field=models.PositiveIntegerField(null=True),
        ),
    ]