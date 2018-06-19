from django.db import models
from wagtail.admin.edit_handlers import PageChooserPanel, FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel

from blog.models import BlogPage, BlogIndexPage


class HomePage(Page):
    body = RichTextField(blank=True, null=True)
    featured = models.ForeignKey(BlogPage, null=True, blank=True, on_delete=models.SET_NULL)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
        PageChooserPanel('featured'),
        ImageChooserPanel('image'),
    ]

    @classmethod
    def allowed_subpage_models(cls):
        return [BlogIndexPage]

    def __str__(self):
        return self.title
