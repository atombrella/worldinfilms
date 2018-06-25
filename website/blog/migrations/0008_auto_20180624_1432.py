# Generated by Django 2.0 on 2018-06-24 14:32

import blog.models
from django.db import migrations, models
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20180620_1421'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpage',
            name='subtitle',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='blogpage',
            name='body',
            field=wagtail.core.fields.StreamField((('main', wagtail.core.blocks.RichTextBlock(classname='full')), ('quote', blog.models.QuoteChooserBlock(target_model=blog.models.Quote)), ('related', wagtail.core.blocks.PageChooserBlock(target_model=['blog.BlogPage'])), ('embedded_video', wagtail.embeds.blocks.EmbedBlock(icon='media')))),
        ),
    ]
