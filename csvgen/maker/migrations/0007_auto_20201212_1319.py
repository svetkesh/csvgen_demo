# Generated by Django 3.1.4 on 2020-12-12 13:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maker', '0006_auto_20201207_1953'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='column',
            index_together={('schema', 'order')},
        ),
    ]
