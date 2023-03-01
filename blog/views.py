from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.conf import settings
from django.db.models import Q
from .models import Post, Category
from .forms import SearchForm
from taggit.models import Tag


def post_list(request, tag_slug=None, category_id=None, category_name=None):
    object_list = Post.published.all()
    tag_list = Tag.objects.all().order_by("name")
    tag = None
    category = None
    canonical = True
    _category_name = category_name
    form_search = SearchForm()

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
        canonical = False

    if category_id:
        category = get_object_or_404(Category, id=category_id)
        # todos los posts de la categoria utilizando el related_name
        object_list = category.get_posts.all()
        canonical = False

    paginator = Paginator(object_list, 10)  # posts(objects) in each page
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)  # todos los objetos de una página

    except PageNotAnInteger:
        # if page is not an integer deliver the first page
        posts = paginator.page(1)

    except EmptyPage:
        # if pages is out of range deliver las page of results
        posts = paginator.page(paginator.num_pages)

    return render(
        request,
        "blog/list.html",
        {
            "category": category,
            "page": page,
            "posts": posts,
            "tag": tag,
            "tag_list": tag_list,
            "CANONICAL": canonical,
            "form": form_search,
        },
    )


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        slug=post,
        status="published",
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )

    return render(request, "blog/detail.html", {"post": post})


def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            # Búsqueda
            results = set(
                Post.objects.filter(
                    Q(title__icontains=query)
                    | Q(search_date__icontains=query)
                    | Q(body__icontains=query)
                    | Q(tags__name__icontains=query)
                )
            )
            print(results)

    return render(
        request,
        "blog/search.html",
        {"query": query, "form": form, "results": results},
    )
