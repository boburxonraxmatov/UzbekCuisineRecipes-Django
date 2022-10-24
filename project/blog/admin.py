from django.contrib import admin
from .models import Category, Article, Comment, Profile

# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
   list_display = ('pk', 'title', 'category', 'views', 'created_at', 'updated_at', 'publish') # pk - PRIMARY KEY
   list_editable = ('publish', )


class CommentAdmin(admin.ModelAdmin):
   list_display = ('pk', 'user', 'created_at')
   readonly_fields = ('text', )


admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
