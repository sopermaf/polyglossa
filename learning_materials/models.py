"""
Learning material models. Provide download
links with category tags
"""
from django.db import models


class LearningMaterial(models.Model):
    """
    A download link of a particular type

    Categorised by level and type, and can
    be ordered by display
    """
    class CERFLevel(models.TextChoices):
        """Language proficiency level"""
        A1 = 'A1'
        A2 = 'A2'
        B1 = 'B1'
        B2 = 'B2'
        C1 = 'C1'

    class MaterialType(models.TextChoices):
        """Learning Material Content Type"""
        VIDEOS = "Videos"
        EXERCISES = "Exercises"
        READINGS = "Readings"

    display_name = models.CharField(max_length=50, unique=True)
    link = models.URLField()
    level = models.CharField(max_length=2, choices=CERFLevel.choices)
    material_type = models.CharField(max_length=20, choices=MaterialType.choices)
    # used for ordering within cateogry
    ordering = models.PositiveIntegerField()
