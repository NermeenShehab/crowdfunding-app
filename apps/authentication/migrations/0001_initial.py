# Generated by Django 3.2.11 on 2022-05-02 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Register',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=11, null=True, unique=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('profile_img', models.ImageField(default='default.jpg', upload_to='user/images/', verbose_name='photo')),
                ('birthdate', models.DateField(null=True)),
                ('facebook_profile', models.URLField(null=True)),
                ('country', models.CharField(max_length=30, null=True)),
                ('last_login', models.DateTimeField(null=True)),
            ],
        ),
    ]
