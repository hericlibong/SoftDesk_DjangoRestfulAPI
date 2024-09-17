from django.contrib import admin
from .models import Project, Contributor

# Inline for Contributor model
class ContributorInline(admin.TabularInline):
    model = Contributor
    extra = 1  # Display 1 blank form by default

# ProjectAdmin without the ManyToMany field directly in fieldsets
class ProjectAdmin(admin.ModelAdmin):
    # Define only the fields that are editable
    fieldsets = [
        (None, {'fields': ['title', 'description', 'type', 'author']}),
    ]
    inlines = [ContributorInline]
    
    # Exclude the 'created_time' field from the form as it is non-editable
    exclude = ['created_time']

admin.site.register(Project, ProjectAdmin)




    

