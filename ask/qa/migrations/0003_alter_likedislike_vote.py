# Generated by Django 4.0.6 on 2022-11-28 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0002_likedislike'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likedislike',
            name='vote',
            field=models.SmallIntegerField(choices=[(1, 'Нравится'), (-1, 'Не нравится')]),
        ),
    ]
