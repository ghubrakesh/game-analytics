# Generated by Django 5.0.6 on 2024-07-03 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GameData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_id', models.IntegerField()),
                ('name', models.CharField(max_length=255)),
                ('release_date', models.DateField()),
                ('required_age', models.IntegerField()),
                ('price', models.FloatField()),
                ('dlc_count', models.IntegerField()),
                ('about_the_game', models.TextField(blank=True, null=True)),
                ('supported_languages', models.CharField(max_length=255)),
                ('windows', models.BooleanField()),
                ('mac', models.BooleanField()),
                ('linux', models.BooleanField()),
                ('positive', models.IntegerField()),
                ('negative', models.IntegerField()),
                ('score_rank', models.IntegerField(blank=True, null=True)),
                ('developers', models.CharField(blank=True, max_length=255, null=True)),
                ('publishers', models.CharField(blank=True, max_length=255, null=True)),
                ('categories', models.TextField(blank=True, null=True)),
                ('genres', models.CharField(blank=True, max_length=255, null=True)),
                ('tags', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
