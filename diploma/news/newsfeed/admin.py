from django.contrib import admin
from newsfeed.models import Article

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'published_at']
    list_filter = ['author', 'topics', 'published_at']
    search_fields = ['title', 'text']
    fields = ['title', 'author', 'description', 'published_at', 'edited_at']
    readonly_fields = ['published_at', 'edited_at']

admin.site.register(Article, ArticleAdmin)
