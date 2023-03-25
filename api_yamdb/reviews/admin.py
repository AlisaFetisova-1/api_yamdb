from django.contrib import admin

from .models import User, Comment, Review


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'role',
        'bio',
        'first_name',
        'last_name',
        'confirmation_code',
    )
    search_fields = ('username', 'role',)
    list_filter = ('username',)
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
admin.site.register(Comment)
admin.site.register(Review)

