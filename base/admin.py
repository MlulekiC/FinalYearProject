from django.contrib import admin
from django.conf import settings
User = settings.AUTH_USER_MODEL
from . import models

class postAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'title']
    ordering = ['id']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author__municipality=request.user.municipality)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            kwargs["queryset"] = User.objects.filter(username=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(models.Post, postAdmin)
admin.site.register(models.PersonalRequest)
admin.site.register(models.CommunityRequestPost)
admin.site.register(models.Notification)