# Generated by Django 5.1.4 on 2025-01-07 08:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamapp', '0006_remove_article_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='fav',
            field=models.CharField(max_length=255, verbose_name='好きなもの、こと'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='hobby',
            field=models.CharField(max_length=255, verbose_name='趣味、特技'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='mbti',
            field=models.CharField(max_length=4, validators=[django.core.validators.RegexValidator(message='MBTIは有効な4文字の組み合わせである必要があります', regex='^[IE][NS][TF][JP]$')], verbose_name='MBTI'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='self_info',
            field=models.TextField(verbose_name='自己紹介'),
        ),
    ]
