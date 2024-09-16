from django.db import models
from django.conf import settings


def validate_role(value):

    valid_roles = ['Developer', 'Tester', 'Manager', 'Reviewer']
    if value not in valid_roles:
        raise ValueError(f"{value} is not a valid role. Valid roles are {valid_roles}")
        

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
    # Voir s'il est possible d'avoir le même related_name pour plusieurs champs 
    created_time = models.DateTimeField(auto_now_add=True, help_text="Project creation date")
    contributors = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Contributor', related_name='projects', help_text="Project contributors")

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # l'auteur du projet est automatiquement ajouté aux contributeurs
        super().save(*args, **kwargs)
        self.contributors.add(self.author)
        self.save()

    
class Contributor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="User")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, help_text="Project")
    role = models.CharField(max_length=20, validators=[validate_role], help_text="User role in the project")
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'project'], name='unique_contributor')
        ]

    def __str__(self):
        return f"{self.user.username} - {self.project.title} - {self.role}"