# Generated by Django 3.1.4 on 2020-12-07 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maker', '0005_auto_20201207_1857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='column',
            name='type',
            field=models.CharField(choices=[('Full name', 'Full name'), ('Integer', 'Integer'), ('Company', 'Company'), ('Job', 'Job'), ('Domain', 'Domain')], max_length=40),
        ),
    ]
