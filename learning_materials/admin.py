"""
Admin interface for learning material
management.
"""
# pylint: disable=missing-class-docstring
from django.contrib import admin

from . import models


@admin.register(models.LearningMaterial)
class LearningMaterialsAdmin(admin.ModelAdmin):
    list_display = ('level', 'ordering', 'material_type', 'display_name')
    fields = ('level', 'ordering', 'material_type', 'display_name', 'link')
    list_filter = ('level', 'material_type')
    search_fields = ('display_name', 'link')
