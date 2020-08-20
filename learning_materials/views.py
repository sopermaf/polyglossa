# pylint: disable=missing-module-docstring,missing-class-docstring

from django.http import JsonResponse

from .models import LearningMaterial


def get_all_materials(request):
    '''
    Return all learning materials according to category.

    Expected format:
    ---
    [
        # sorted by `title`
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
    # get all materials
    materials = [
        {
            'level': lm.level,
            'type': lm.material_type,
            'link': lm.link,
            'title': lm.display_name
        }
        for lm in LearningMaterial.objects.order_by('ordering')
    ]

    # group by level
    materials_by_level = []
    for level in LearningMaterial.CERFLevel:
        materials_by_level.append([mat for mat in materials if mat['level'] == str(level)])

    fully_sorted = []
    for level_materials, level in zip(materials_by_level, LearningMaterial.CERFLevel):
        if not level_materials:
            continue

        level_content = {}
        for section in LearningMaterial.MaterialType:
            level_content[section] = [lm for lm in level_materials if lm['type'] == str(section)]
        fully_sorted.append({'content': level_content, 'level': str(level)})

    print(f"final content:\n{json.dumps(fully_sorted, indent=4)}\n")
    
    return JsonResponse(fully_sorted, safe=False)
