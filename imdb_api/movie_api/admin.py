from django.contrib import admin
from .models import Watchlist, StreamPlatform


class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'storyline', 'active')
    list_display_links = ('title', 'storyline', )
    ordering = ('title',)


class StreamAdmin(admin.ModelAdmin):
    list_display = ('name', 'about', 'website', 'created')
    list_display_links = ('name', 'about', )
    ordering = ('name',)

admin.site.register(Watchlist, MovieAdmin)
admin.site.register(StreamPlatform, StreamAdmin)