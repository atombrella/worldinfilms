from django.db import migrations
from wagtail.core.rich_text import RichText


def convert_to_streamfield(apps, schema_editor):
    BlogPage = apps.get_model("blog", "BlogPage")
    for page in BlogPage.objects.all():
        if page.body.raw_text and not page.body:
            page.body = [('main', RichText(page.body.raw_text))]
            page.save()


def convert_to_richtext(apps, schema_editor):
    BlogPage = apps.get_model("blog", "BlogPage")
    for page in BlogPage.objects.all():
        if page.body.raw_text is None:
            raw_text = ''.join([
                child.value.source for child in page.body
                if child.block_type == 'rich_text'
            ])
            page.body = raw_text
            page.save()


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20180620_1314'),
    ]

    operations = [
        migrations.RunPython(
            convert_to_streamfield,
            convert_to_richtext,
        ),
    ]
