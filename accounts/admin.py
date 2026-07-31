from django.contrib import admin
from .models import User


admin.site.site_header = 'Plateforme pédagogique — Administration'
admin.site.site_title = 'Admin Plateforme pédagogique'
admin.site.index_title = 'Gestion'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = ('username', 'email', 'school', 'role', 'is_staff', 'is_active')
	list_filter = ('role', 'is_staff', 'is_active')
	search_fields = ('username', 'email', 'school')

  