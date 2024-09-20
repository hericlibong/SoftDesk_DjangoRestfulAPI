from django.db import models
from django.conf import settings
import uuid

from django.forms import ValidationError



class Project(models.Model):
    TYPE_CHOICES = [
        ('backend', 'Back-end'),
        ('frontend', 'Front-end'),
        ('ios', 'iOS'),
        ('android', 'Android'),
         
    ]

    title = models.CharField(max_length=100, help_text="Project title")
    description = models.TextField(help_text="Project description")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, help_text="Project type")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="Project author")  
    created_time = models.DateTimeField(auto_now_add=True, help_text="Project creation date")
    contributors = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Contributor', 
                                          related_name='projects', help_text="Project contributors")

    def __str__(self):
        return self.title  
    
    def save(self, *args, **kwargs):
        # l'auteur du projet est automatiquement ajouté aux contributeurs
        super().save(*args, **kwargs)
        self.contributors.add(self.author)
    

class Contributor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="User")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, help_text="Project")
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'project'], name='unique_contributor')
        ]

    def __str__(self):
        return f"{self.user.username} - {self.project.title} "
    

class Issue(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('finished', 'Finished'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    TAG_CHOICES = [
        ('bug', 'Bug'),
        ('feature', 'Feature'),
        ('task', 'Task'),
    ]

    title = models.CharField(max_length=100, help_text="Issue title")
    description = models.TextField(help_text="Issue description")
    project = models.ForeignKey(Project, related_name='issues', on_delete=models.CASCADE, help_text="Project to which the issue belongs")
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='assigned_issues', on_delete=models.CASCADE, help_text="User to whom the issue is assigned")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, help_text="Status of the issue")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, help_text="Priority of the issue")
    tag = models.CharField(max_length=20, choices=TAG_CHOICES, help_text="Tag of the issue")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='authored_issues', on_delete=models.CASCADE, help_text="Author of the issue")
    created_time = models.DateTimeField(auto_now_add=True, help_text="Issue creation date")

    def clean(self):
       if not self.project.contributors.filter(id=self.assigned_to.id).exists():
            raise ValidationError("The author of the issue must be a contributor to the project")
    
    

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(help_text="Description of the comment")
    issue = models.ForeignKey(Issue, related_name='comments', on_delete=models.CASCADE, help_text="Issue to which the comment belongs")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="Author of the comment")
    created_time = models.DateTimeField(auto_now_add=True, help_text="Comment creation date")
