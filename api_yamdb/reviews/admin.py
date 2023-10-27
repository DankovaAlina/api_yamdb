from django.contrib import admin

from .models import Comment, Review, Title


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'author', 'score', 'pub_date')
    search_fields = ('text',)
    list_editable = ('text', 'author', 'score')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'review', 'author', 'text', 'pub_date')
    search_fields = ('text',)


admin.site.register(Comment, CommentAdmin)
admin.site.register(Review, ReviewAdmin)
