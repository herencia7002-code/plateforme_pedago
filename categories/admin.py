from django.contrib import admin
from .models import Category, Subject


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'created_at')
	search_fields = ('name', 'description')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
	list_display = ('name', 'category', 'created_at')
	search_fields = ('name', 'description')
	list_filter = ('category',)
