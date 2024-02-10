from django.contrib import admin

# Register your models here.
from import_export.admin import ImportExportModelAdmin


from guest.models import Guest,Feedback


@admin.register(Guest)
class GuestAdmin(ImportExportModelAdmin):
    list_display =  ['first_name', 'last_name', 'email', 'phone', 'address', 'company', 'head_about_us']
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'address', 'company',)
    list_filter = ['head_about_us',]



@admin.register(Feedback)
class CommentAdmin(ImportExportModelAdmin):
    list_display = ['comment', 'excellent', 'good', 'fair', 'poor',]    
    list_filter = ['excellent', 'good', 'fair', 'poor',]
    list_editable = ['excellent', 'good', 'fair', 'poor']