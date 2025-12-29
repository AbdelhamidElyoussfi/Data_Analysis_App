from django.contrib import admin
from .models import UploadedFile

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'file', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['file']
    readonly_fields = ['uploaded_at']
    
    def has_add_permission(self, request):
        # Prevent adding files through admin (use upload page instead)
        return False

