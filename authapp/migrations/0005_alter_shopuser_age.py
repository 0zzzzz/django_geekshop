# Generated by Django 3.2.4 on 2021-11-20 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0004_auto_20211116_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='age',
            field=models.PositiveSmallIntegerField(default=18, verbose_name='Возраст'),
        ),
    ]
