from django.contrib import admin
from .models import CustomUser, AboutUrl

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'gender', 'date_joined', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'first_name', 'last_name', 'gender')
    ordering = ('-id',)

@admin.register(AboutUrl)
class AboutUrlAdmin(admin.ModelAdmin):
    list_display = ('title', 'original_url', 'user')#this shows the model fields in the admin panel
    search_fields = ('title', 'original_url', 'user')#gives chance to search for the given fields
    list_filter = ('choices',)#it filters choices(we give choicefield for this object)
    autocomplete_fields = ('user',)#we can give foreign key , manytomany fields for this object
    ordering = ('-id',)


