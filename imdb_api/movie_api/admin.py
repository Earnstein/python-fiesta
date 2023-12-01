from django.contrib import admin
from .models import Movie
# Register your models here.
class MovieAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'active')
    list_display_links = ('name', 'description')
    ordering = ('name',)


admin.site.register(Movie, MovieAdmin)