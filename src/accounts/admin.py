from django.contrib import admin
from .models import User

# admin.site.register(User)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'age', 'can_be_contacted', 'can_be_data_shared']
    search_fields = ['username', 'email']
    list_filter = ['can_be_contacted', 'can_be_data_shared']
    fieldsets = (
        ('User Informations', {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('age', 'can_be_contacted', 'can_be_data_shared')}),
        ('Permissions', {'fields': ('groups', 'user_permissions')}),
    )
    filter_horizontal = ['groups', 'user_permissions']
    ordering = ['id']
    readonly_fields = ['id']
