from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.post_list, name="post-list"),
    path("search/", views.post_search, name="post_search"),
    path("tag/<slug:tag_slug>/", views.post_list, name="post_list_by_tag"),
    path(
        "categorias/<int:category_id>/<slug:category_name>/",
        views.post_list,
        name="category",
    ),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>/",
        views.post_detail,
        name="post-detail",
    ),
]
