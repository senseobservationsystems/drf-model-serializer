# Generated by Django 2.2.4 on 2019-11-18 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe_id', models.UUIDField()),
                ('name', models.CharField(max_length=25)),
            ],
        ),
    ]