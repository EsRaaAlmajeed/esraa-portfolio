from django.contrib import admin
from .models import Project , Category, Certification

# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug":("title",)
    }
    list_display =('title', 'slug', 'technologies') 
    list_filter= ('technologies',)
    search_fields=('title', 'technologies')
    
    
    
admin.site.register(Project, ProjectAdmin)
admin.site.register(Category)
admin.site.register(Certification)
    