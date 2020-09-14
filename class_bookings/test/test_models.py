# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring, no-self-use, unused-wildcard-import, wildcard-import

from datetime import datetime, timedelta

import pytest

from .. import errors as err
from .. import models as mods
from .  import util


@pytest.mark.django_db
def test_validate_signup_error_slot_not_found():
    student = mods.Student(name='foo', email='bar@foo.com')

    # no seminars exist
    with pytest.raises(err.NoMatchingSeminarError):
        mods.SeminarSlot.validate_signup(1, student)

    # no future seminars exist
    slot = util.create_seminar_slot(
        util.create_activity(mods.Activity.SEMINAR),
        datetime.now() - timedelta(days=1)
    )
    with pytest.raises(err.NoMatchingSeminarError):
        mods.SeminarSlot.validate_signup(slot.id, student)


@pytest.mark.django_db
def test_validate_signup_error_student_present():
    # setup slot with student
    student = mods.Student.objects.create(name='foo', email='bar@foo.com')

    slot = util.create_seminar_slot(
        util.create_activity(mods.Activity.SEMINAR),
        datetime.now() + timedelta(days=1)
    )
    slot.students.add(student)
    slot.save()

    with pytest.raises(err.StudentAlreadyPresentError):
        mods.SeminarSlot.validate_signup(slot.id, student)
