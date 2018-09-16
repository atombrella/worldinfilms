from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from taggit.models import TaggedItemBase, Tag as TaggitTag
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.blocks import PageChooserBlock, RichTextBlock
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Orderable, Page
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.snippets.models import register_snippet


@register_snippet
class Quote(models.Model):
    quote = models.CharField(max_length=1024)
    movie = models.CharField(max_length=255)
    actor = models.CharField(max_length=255)
    year = models.PositiveIntegerField(
        validators=[MinValueValidator(limit_value=1900), MaxValueValidator(limit_value=2050)],
    )
    imdb = models.URLField(blank=False, null=False)

    def __str__(self):
        return self.quote


class QuoteChooserBlock(SnippetChooserBlock):

    def __init__(self, target_model=Quote, **kwargs):
        super().__init__(target_model, **kwargs)

    class Meta:
        icon = "openquote"
        template = "blog/snippets/quote.html"


@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=80)
    description = models.CharField(max_length=500, blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        FieldPanel('description', classname='full'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class BlogCategoryBlogPage(models.Model):
    category = models.ForeignKey(
        BlogCategory, related_name="+", verbose_name='Category',
        on_delete=models.CASCADE,
    )
    page = ParentalKey('BlogPage', related_name='categories', null=True, blank=True)

    panels = [
        FieldPanel('category'),
    ]


class BlogIndexPage(RoutablePageMixin, Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    @classmethod
    def allowed_subpage_models(cls):
        return [BlogPage, BlogTagIndexPage]

    @route(r'^tag/(?P<tag>[- \w]+)/$')
    def post_by_tag(self, request, tag, *args, **kwargs):
        self.posts = self.get_posts().filter(tags__slug=tag)
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^category/(?P<category>[-\w]+)/$')
    def post_by_category(self, request, category, *args, **kwargs):
        self.posts = self.get_posts().filter(categories__slug=category)
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^search/$')
    def post_search(self, request, *args, **kwargs):
        search_query = request.GET.get('q', None)
        self.posts = self.get_posts()
        if search_query:
            self.posts = self.posts.filter(body__contains=search_query)
            self.search_term = search_query
            self.search_type = 'search'
        return Page.serve(self, request, *args, **kwargs)

    def get_posts(self):
        return BlogPage.objects.descendant_of(self).live()

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        if hasattr(self, 'posts'):
            context['posts'] = self.posts
        else:
            context['posts'] = self.get_descendants().type(
                BlogPage
            ).specific().live().order_by('-first_published_at')[:10]
        return context


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('BlogPage', related_name='tagged_items')


@register_snippet
class Tag(TaggitTag):
    class Meta:
        proxy = True


class BlogTagIndexPage(Page):

    def get_context(self, request, **kwargs):
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)

        context = super().get_context(request)
        context['blogpages'] = blogpages
        return context


class BlogPage(RoutablePageMixin, Page):
    subtitle = models.CharField(max_length=250, null=True, blank=True)
    date = models.DateField("Post date", null=False)
    intro = RichTextField(null=False, blank=False)
    body = StreamField([
        ('main', RichTextBlock(classname="full")),
        ('quote', QuoteChooserBlock(target_model=Quote)),
        ('related', PageChooserBlock(target_model="blog.BlogPage")),
        ('embedded_video', EmbedBlock(icon="media")),
    ], null=False, blank=False)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )
    blog_categories = ParentalManyToManyField(BlogCategory, through=BlogCategoryBlogPage, blank=True)

    @classmethod
    def allowed_subpage_models(cls):
        return []

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('date'),
        FieldPanel('intro'),
        ImageChooserPanel('image'),
        StreamFieldPanel('body'),
        FieldPanel('tags', classname="full"),
        FieldPanel('blog_categories', classname="full", widget=forms.CheckboxSelectMultiple),
        InlinePanel('gallery_images', label="Gallery images"),
    ]


class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]
