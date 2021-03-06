# Generated by Django 2.0 on 2018-07-09 13:35

from django.db import migrations
import django.db.models.deletion
import modelcluster.fields
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20180624_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogcategoryblogpage',
            name='page',
            field=modelcluster.fields.ParentalKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='blog.BlogPage'),
        ),
        migrations.AlterField(
            model_name='blogpage',
            name='blog_categories',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, through='blog.BlogCategoryBlogPage', to='blog.BlogCategory'),
        ),
        migrations.AlterField(
            model_name='blogpage',
            name='intro',
            field=wagtail.core.fields.RichTextField(),
        ),
    ]
