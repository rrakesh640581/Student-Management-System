from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'email',
        'age',
        'course',
        'phone'
    )

    search_fields = ('name', 'email', 'course')

    list_filter = ('course',)

    ordering = ('id',)