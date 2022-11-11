from django.db import models


class CreationBase(models.Model):
    """Abstract model to store the time of creation"""

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class AuditBase(CreationBase):
    """Abstract model to store the time of creation and last update"""

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
