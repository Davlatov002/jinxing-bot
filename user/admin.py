from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('username','first_name','last_name', 'phone_number', 'telegram_username', 'created_at')

admin.site.register(User, UserAdmin)
