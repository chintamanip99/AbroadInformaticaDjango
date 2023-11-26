# Generated by Django 3.0.8 on 2020-07-13 05:45

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0002_auto_20200713_0545'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, null=True)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('image', models.FileField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Category2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, null=True)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('image', models.FileField(blank=True, null=True, upload_to='')),
                ('category1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='content.Category1')),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, null=True)),
                ('description', models.TextField(max_length=500, null=True)),
                ('image', models.FileField(blank=True, null=True, upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])),
                ('audio', models.FileField(blank=True, null=True, upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp3', 'wav', 'mp4', 'm4a', 'wma'])])),
                ('video', models.FileField(blank=True, null=True, upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4', 'm4a', 'm4v', 'f4v', 'f4a', 'm4b', 'm4r', 'f4b', 'mov'])])),
                ('text_content', models.FileField(blank=True, null=True, upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['txt', 'docx'])])),
                ('image_link', models.URLField(blank=True, null=True)),
                ('audio_link', models.URLField(blank=True, null=True)),
                ('video_link', models.URLField(blank=True, null=True)),
                ('text_content_link', models.URLField(blank=True, null=True)),
                ('no_of_likes', models.IntegerField(default=0)),
                ('no_of_shares', models.IntegerField(default=0)),
                ('no_of_comments', models.IntegerField(default=0)),
                ('no_of_reports', models.IntegerField(default=0)),
                ('record_created_date_time', models.DateTimeField(default=datetime.datetime(2020, 7, 13, 5, 45, 8, 956997), null=True)),
                ('category1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='content.Category1')),
                ('category2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='content.Category2')),
            ],
            options={
                'ordering': ['-record_created_date_time'],
            },
        ),
        migrations.CreateModel(
            name='RecordComments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=1000, null=True)),
                ('no_of_reports', models.IntegerField(default=0, null=True)),
                ('comment_created_date_time', models.DateTimeField(default=datetime.datetime(2020, 7, 13, 5, 45, 8, 958155), null=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.Profile')),
                ('record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.Record')),
            ],
            options={
                'ordering': ['-comment_created_date_time'],
            },
        ),
        migrations.CreateModel(
            name='RecordLikes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.Profile')),
                ('record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.Record')),
            ],
            options={
                'unique_together': {('profile', 'record')},
            },
        ),
    ]
