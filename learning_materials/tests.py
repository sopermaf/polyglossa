# pylint: disable=missing-module-docstring,missing-class-docstring, missing-function-docstring
import uuid
import json
import random

import pytest
from django.urls import reverse

from .models import LearningMaterial


URL_GET_ALL = reverse('get-all-materials')


@pytest.mark.django_db
def test_get_materials_exists(client):
    response = client.get(URL_GET_ALL)
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_materials_ordered_by_level(client):
    # shuffle list randomly out of order by level
    levels = [str(level) for level in LearningMaterial.CERFLevel]
    random.shuffle(levels)
    for level in levels:
        add_material_to_db(1, level, 'Readings') 

    response = client.get(URL_GET_ALL)
    materials = json.loads(response.content)

    assert materials == sorted(materials, key=lambda item: item['level'])


@pytest.mark.django_db
def test_get_materials_level_format(client):
    sections = ('Readings', 'Exercises', 'Videos')
    for section in sections:
        add_material_to_db(1, 'A1', section)

    response = client.get(URL_GET_ALL)
    a1_materials = json.loads(response.content)[0]['content']

    for section in sections:
        assert section in a1_materials
        assert len(a1_materials[section]) == 1


@pytest.mark.django_db
def test_get_materials_ordered_within_section(client):
    add_material_to_db(2, 'A1', 'Readings')
    add_material_to_db(1, 'A1', 'Readings')

    response = client.get(URL_GET_ALL)
    a1_content = json.loads(response.content)[0]['content']['Readings']

    # only title used as names should be unique
    exp_order = [m.display_name for m in LearningMaterial.objects.order_by('ordering')]
    assert [lm['title'] for lm in a1_content] == exp_order


# helper functions


def add_material_to_db(order, level, m_type):
    assert level in LearningMaterial.CERFLevel
    assert m_type in LearningMaterial.MaterialType

    LearningMaterial.objects.create(
        display_name=str(uuid.uuid4()),
        link='http://link.com',
        level=level,
        material_type=m_type,
        ordering=order,
    )
