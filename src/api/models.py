from django.db import models
from django.conf import settings



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
