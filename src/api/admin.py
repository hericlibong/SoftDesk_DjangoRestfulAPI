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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        project_id = request.resolver_match.kwargs.get('object_id')
        if project_id:
            project = Project.objects.get(pk=project_id)
            
            # Limiter les utilisateurs assignables (assigned_to) aux contributeurs du projet
            if db_field.name == 'assigned_to':
                kwargs['queryset'] = project.contributors.all()
            
            # Limiter les auteurs (author) aux contributeurs du projet
            if db_field.name == 'author':
                kwargs['queryset'] = project.contributors.all()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

   
# ProjectAdmin with Issue and Contributor inlines
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'type', 'author']
    fieldsets = [
        (None, {'fields': ['title', 'description', 'type', 'author']}),
    ]
    inlines = [ContributorInline, IssueInline]
    exclude = ['created_time']

# IssueAdmin
class IssueAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'assigned_to', 'author']
    fieldsets = [
        (None, {'fields': ['title', 'description', 'project', 'assigned_to', 'status', 'priority', 'tag', 'author']}),
    ]
    inlines = [CommentInline]
    exclude = ['created_time']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Récupère l'instance de l'issue si on modifie une issue existante
        issue_id = request.resolver_match.kwargs.get('object_id')
        if issue_id:
            issue = Issue.objects.get(pk=issue_id)
            project = issue.project
        else:
            # Si l'on crée une nouvelle issue, on utilise la valeur du champ 'project'
            project = kwargs.get('initial', {}).get('project', None)
        
        if project:
            # Limiter les utilisateurs assignables (assigned_to) aux contributeurs du projet
            if db_field.name == 'assigned_to':
                kwargs['queryset'] = project.contributors.all()

            # Limiter les auteurs (author) aux contributeurs du projet
            if db_field.name == 'author':
                kwargs['queryset'] = project.contributors.all()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
# CommentAdmin
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'issue', 'created_time']
    exclude = ['created_time']

admin.site.register(Project, ProjectAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment, CommentAdmin)
