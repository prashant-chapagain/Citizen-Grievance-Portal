from django.contrib import admin
from .models import Department, GrievanceCategory, Grievance, GrievanceResponse, UserProfile

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(GrievanceCategory)
class GrievanceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'department')
    list_filter = ('department',)
    search_fields = ('name',)

@admin.register(Grievance)
class GrievanceAdmin(admin.ModelAdmin):
    list_display = ('reference_id', 'title', 'user', 'category', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('reference_id', 'title', 'description', 'user__username', 'user__first_name', 'user__last_name')
    readonly_fields = ('reference_id', 'created_at', 'updated_at')

@admin.register(GrievanceResponse)
class GrievanceResponseAdmin(admin.ModelAdmin):
    list_display = ('grievance', 'responder', 'created_at')
    list_filter = ('created_at', 'responder')
    search_fields = ('grievance__reference_id', 'grievance__title', 'response')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone')