from django import template
from django.shortcuts import get_object_or_404
from page.models import Page

register = template.Library()


@register.simple_tag
def get_page_list():
    pages = Page.objects.all()

    return pages


@register.simple_tag
def get_page_privacy():
    page_privacy = get_object_or_404(Page, id=2)

    return page_privacy
