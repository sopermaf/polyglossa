# pylint: disable=missing-module-docstring,missing-class-docstring

from django.http import JsonResponse

from .models import LearningMaterial


def get_all_materials(request):
    '''
    Return all learning materials according to category.

    Expected format:
    ---
    [
        {
            'level': 'A1',
            'content': {
                'Exercises': [
                    {'title': 'foobar', 'link': 'http://foobar.com'},
                ],
                'Videos': [
                    {'title': 'foobar', 'link': 'http://foobar.com'},
                ],
                'Readings': [
                    {'title': 'foobar', 'link': 'http://foobar.com'},
                ],
            }
        }
    ]
    '''
    # NOTE: number of materials should be small < 200
    transform = lambda lm: {'title': lm.display_name, 'link': lm.link}
    all_materials = LearningMaterial.objects.order_by('level', 'ordering')

    organised_materials = [
        {
            'level': str(level),
            'content': {
                str(m_type): [
                    transform(lm) for lm in all_materials.filter(level=level, material_type=m_type)
                ]
                for m_type in LearningMaterial.MaterialType
            }
        }
        for level in LearningMaterial.CERFLevel
    ]

    return JsonResponse(organised_materials, safe=False)
