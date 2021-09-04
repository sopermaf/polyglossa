# Generated by Django 3.1.8 on 2021-08-19 17:18

from django.db import migrations


DEFAULT_SUBJECTS = [
    'Other',
    'General Question/Enquiry',
    'Problem',
]


def create_default_subjects(apps, schema_editor):
    """populates the subject table"""
    FeedbackType = apps.get_model('feedback', 'FeedbackType')
    for subject in DEFAULT_SUBJECTS:
        FeedbackType.objects.create(name=subject.title())


class Migration(migrations.Migration):
    dependencies = [
        ('feedback', '0001_initial')
    ]

    operations = [
        migrations.RunPython(create_default_subjects)
    ]
