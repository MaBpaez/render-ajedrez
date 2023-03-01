from django.shortcuts import render, get_object_or_404
from .models import Page


# Vista para Page
def page(request, page_id, page_title):
    page_name = get_object_or_404(Page, id=page_id)
    _page_title = page_title

    return render(request, 'page/sample.html', {'page': page_name})
