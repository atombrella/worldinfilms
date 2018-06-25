from django.shortcuts import render
from wagtail.search.models import Query
from .models import BlogPage


def search(request):
    search_query = request.GET.get('query', None)
    if search_query:
        search_results = BlogPage.objects.live().search(search_query)

        # Log the query so Wagtail can suggest promoted results
        Query.get(search_query).add_hit()
    else:
        search_results = BlogPage.objects.none()

    # Render template
    return render(request, 'blog/search_results.html', {
        'search_query': search_query,
        'search_results': search_results,
    })
