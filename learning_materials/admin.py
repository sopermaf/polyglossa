"""
Admin interface for learning material
management.
"""
# pylint: disable=missing-class-docstring
from django.contrib import admin

from . import models


class LearningMaterialsAdmin(admin.ModelAdmin):
    list_display = ('level', 'ordering', 'material_type', 'display_name')
    fields = ('level', 'ordering', 'material_type', 'display_name', 'link')


admin.site.register(models.LearningMaterial, LearningMaterialsAdmin)
