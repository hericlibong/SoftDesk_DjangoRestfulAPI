from django.contrib import admin
from .models import Project, Contributor, Issue, Comment

# Inline for Contributor model
class ContributorInline(admin.TabularInline):
    model = Contributor
    extra = 1  # Display 1 blank form by default

# Inline for Comment model
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1  # Display 1 blank form by default

# Inline for Issue model
class IssueInline(admin.TabularInline):
    model = Issue
    extra = 1  # Display 1 blank form by default
    
# ProjectAdmin without the ManyToMany field directly in fieldsets
class ProjectAdmin(admin.ModelAdmin):
    # Define only the fields that are editable
    fieldsets = [
        (None, {'fields': ['title', 'description', 'type', 'author']}),
    ]
    inlines = [ContributorInline, IssueInline]
    # Exclude the 'created_time' field from the form as it is non-editable
    exclude = ['created_time']

# IssueAdmin
class IssueAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'description', 'project', 'assigned_to', 'status', 'priority', 'tag', 'author']}),
    ]
    inlines = [CommentInline]
    exclude = ['created_time']

# Separate CommentAdmin
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ['author', 'issue', 'created_time']
#     exclude = ['created_time']

admin.site.register(Project, ProjectAdmin)
admin.site.register(Issue, IssueAdmin)
# admin.site.register(Comment, CommentAdmin)





    

