from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.models import User
from taggit.models import Tag
from movies.models import Movie, Review


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'release_date', 'country', 'genres_list', 'image_tag'
    ]
    list_filter = ['title', 'country', 'release_date', 'genres']
    search_fields = ['title', 'country']
    readonly_fields = ['image_tag']

    def get_queryset(self, request):
        return super().get_queryset(request).\
            prefetch_related('genres')

    def genres_list(self, obj):
        return u", ".join(o.name for o in obj.genres.all())

    def image_tag(self, obj):
        return format_html(f'<img src="{obj.poster.url}" width="60" height="100">')
    image_tag.short_description = 'Poster'


admin.site.unregister(User)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'username', 'email', 'date_joined',
        'is_superuser', 'is_active', 'is_staff'
    ]
    search_fields = ['username']
    list_filter = ['username', 'date_joined']
