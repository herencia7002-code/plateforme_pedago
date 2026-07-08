from django.contrib import admin
from .models import User, Course, Enrollment


# Customize admin site headers
admin.site.site_header = 'Plateforme pédagogique — Administration'
admin.site.site_title = 'Admin Plateforme pédagogique'
admin.site.index_title = 'Gestion'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = ('username', 'email', 'school', 'role', 'is_staff', 'is_active')
	list_filter = ('role', 'is_staff', 'is_active')
	search_fields = ('username', 'email', 'school')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
	list_display = ('title', 'teacher', 'created_at')
	search_fields = ('title', 'description')
	list_filter = ('created_at',)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
	list_display = ('student', 'course', 'enrolled_at')
	search_fields = ('student__username', 'course__title')

