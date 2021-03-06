# Generated by Django 2.0 on 2018-07-09 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_genericpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('url', models.URLField()),
                ('description', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': '',
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
            },
        ),
    ]
