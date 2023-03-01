from django.contrib import admin
from .models import Category, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status',
                    'PostCategories')
    list_filter = ('status', 'created', 'publish', 'author__username')
    search_fields = ('title', 'body', 'autor__username', 'categories__name')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', '-publish')

    def PostCategories(self, obj):
        return ', '.join(
            [c.name for c in obj.categories.all().order_by('name')])

    PostCategories.short_description = 'Categorías'
