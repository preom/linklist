from django.contrib import admin
from linklist.models import LinkPost, Keyword

class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(LinkPost, AuthorAdmin)
admin.site.register(Keyword, AuthorAdmin)
