from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


class User(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True, help_text="User's age")
    can_be_contacted = models.BooleanField(default=False, help_text="User can be contacted or not")
    can_be_data_shared = models.BooleanField(default=False, help_text="User can share data or not")
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='api_users_groups', blank=True,
        help_text="The groups this user belongs to."
        )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='api_users_user_permissions', blank=True,
        help_text="Specific permissions for this user."
    )

    def clean(self):
        if self.age is not None and self.age < 15:
            raise ValidationError("l'utilisateur doit avoir au moins 15 ans pour s'inscrire")

    def can_collect_data(self):
        return self.age >= 15 and self.can_be_data_shared
