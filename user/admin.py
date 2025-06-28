from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('username','first_name','last_name', 'phone_number', 'telegram_username', 'created_at')
    search_fields = ('username', 'first_name', 'last_name', 'phone_number', 'telegram_username')

admin.site.register(User, UserAdmin)
