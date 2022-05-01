# Generated by Django 3.2.11 on 2022-05-01 04:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_alter_comment_report_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment_report',
            name='report',
            field=models.CharField(choices=[('ip', 'inappropriate')], default='ip', max_length=200),
        ),
    ]
