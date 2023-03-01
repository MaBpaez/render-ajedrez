from django import template
from blog.models import Category

register = template.Library()


@register.inclusion_tag('blog/latest_categories.html')
def show_latest_categories(count=10):
    latest_categories = Category.objects.all().order_by('name')[:count]
    return {'latest_categories': latest_categories}
