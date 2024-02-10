from django.contrib import admin
from outlets.models import Outlet,Comment
from import_export.admin import ImportExportModelAdmin

# Register your models here.

@admin.register(Outlet)
class OutletAdmin(ImportExportModelAdmin):
    list_display = ['name', 'description']


@admin.register(Comment)
class CommentAdmin(ImportExportModelAdmin):
    list_display = ['name', 'description']
