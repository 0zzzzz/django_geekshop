# Generated by Django 3.2.4 on 2021-11-16 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0004_auto_20211116_1711'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopuser',
            name='nickname',
            field=models.CharField(blank=True, max_length=60, verbose_name='Ник'),
        ),
    ]
