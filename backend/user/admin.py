from django.contrib import admin
from user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = (
        'id',
        'phone_number',
    )
    list_filter = ('is_active', 'is_staff', 'created_at')
    list_display = (
        'id',
        'phone_number',
        'is_active',
    )
    list_editable = ('is_active',)
    ordering = ('-created_at',)
    exclude = ('groups', 'user_permissions')
    readonly_fields = ('last_login',)
    list_per_page = 10
