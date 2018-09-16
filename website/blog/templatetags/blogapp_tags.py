from django import template

register = template.Library()


@register.inclusion_tag('blog/components/tags_list.html', takes_context=True)
def tags_list(context, blog_page):
    tags = blog_page.tags.all()
    return {
        'blog_page': blog_page,
        'request': context['request'],
        'tags': tags,
    }


@register.inclusion_tag('blog/components/categories_list.html', takes_context=True)
def categories_list(context, blog_page):
    categories = blog_page.categories.all()
    return {
        'blog_page': blog_page,
        'request': context['request'],
        'categories': categories,
    }
