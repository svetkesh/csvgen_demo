# Generated by Django 3.1.4 on 2020-12-07 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='columnnames',
            name='integer_from',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='columnnames',
            name='integer_to',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]