# Generated by Django 5.1.6 on 2025-05-19 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recomender', '0014_review_star'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='star',
        ),
        migrations.AddField(
            model_name='review',
            name='rating',
            field=models.IntegerField(default=5),
        ),
    ]
