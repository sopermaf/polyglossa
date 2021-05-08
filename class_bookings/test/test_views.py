# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring, no-self-use, unused-wildcard-import, wildcard-import
import json
from uuid import uuid4
from datetime import timedelta, datetime

import pytest
from django.urls import reverse
from django.utils import timezone

from class_bookings.const import *
from class_bookings.models import *
from class_bookings.views import _HomePageDateSerializer
from payments.models import Order
from . import util as t_util


# Seminar Signup

POST_SEMINAR_URL = reverse('signup-seminar')
UPCOMING_DT_FORMAT = _HomePageDateSerializer.DT_FORMAT

@pytest.mark.django_db
def test_seminar_signup_success(client):
    seminar = t_util.create_activity(activity_type=Activity.SEMINAR, order=1)
    slot = t_util.create_seminar_slot(seminar, timezone.now() + timedelta(days=2))

    params = create_seminar_params(slot.pk, 'foo', 'foo@example.com')
    response = client.post(POST_SEMINAR_URL, data=params)


    assert response.status_code == RESOURCE_CREATED_CODE    # resource created code
    assert slot.students.count() == 0                       # student not in slot

    assert len(Student.objects.all()) == 1
    student = Student.objects.first()
    assert student.name == 'foo'
    assert student.email == 'foo@example.com'

    assert len(Order.objects.all()) == 1
    order = Order.objects.first()
    exp_purchased_detail = 'Polyglossa Seminar\n("{}" @ {} UTC)'.format(
        seminar.title, slot.start_datetime.strftime('%d-%b-%Y %H:%M')
    )
    assert order.customer == student
    assert order.payment_status == Order.PaymentStatus.AWAITING
    assert order.purchased_detail == exp_purchased_detail


@pytest.mark.django_db
def test_seminar_signup_success_with_cancel_order(client):
    seminar = t_util.create_activity(activity_type=Activity.SEMINAR, order=1)
    slot = t_util.create_seminar_slot(seminar, timezone.now() + timedelta(days=2))

    params = create_seminar_params(slot.pk, 'foo', 'foo@example.com')
    for _ in range(2):
        response = client.post(POST_SEMINAR_URL, data=params)
        assert response.status_code == RESOURCE_CREATED_CODE

    # original order cancelled on ordering the same thing
    orders = Order.objects.all()
    assert len(orders) == 2
    assert orders[0].payment_status == Order.PaymentStatus.CANCELLED
    assert orders[1].payment_status == Order.PaymentStatus.AWAITING


@pytest.mark.django_db
def test_seminar_signup_error_past_slot(client):
    seminar = t_util.create_activity(activity_type=Activity.SEMINAR)
    slot = t_util.create_seminar_slot(seminar, timezone.now() - timedelta(days=2))

    response = client.post(POST_SEMINAR_URL, data=create_seminar_params(slot.pk))

    assert response.status_code == 400          # resource created code
    assert slot.students.count() == 0           # student not in slot
    assert len(Order.objects.all()) == 0        # Order not created
    assert len(Student.objects.all()) == 1      # Student created


@pytest.mark.django_db
def test_seminar_signup_error_missing_data(client):
    seminar = t_util.create_activity(activity_type=Activity.SEMINAR)
    slot = t_util.create_seminar_slot(seminar, timezone.now() - timedelta(days=2))

    for arg_to_pop in ('student_name', 'student_email', 'slot_id'):
        params = create_seminar_params(slot.pk)
        params.pop(arg_to_pop)

        response = client.post(POST_SEMINAR_URL, data=create_seminar_params(slot.pk))

        assert response.status_code == 400          # resource created code
        assert slot.students.count() == 0           # student not in slot
        assert len(Order.objects.all()) == 0        # Order not created
        assert len(Student.objects.all()) == 1      # Student created


@pytest.mark.django_db
def test_seminar_signup_error_slot_not_found(client):
    response = client.post(POST_SEMINAR_URL, data=create_seminar_params(1))

    assert response.status_code == 400          # resource created code
    assert len(Order.objects.all()) == 0        # Order not created
    assert len(Student.objects.all()) == 1      # Student created


@pytest.mark.django_db
def test_seminar_signup_error_student_already_present(client):
    seminar = t_util.create_activity(activity_type=Activity.SEMINAR, order=1)
    slot = t_util.create_seminar_slot(seminar, timezone.now() + timedelta(days=2))
    student = Student.objects.create(name='foo', email='foo@email.com')

    slot.students.add(student)
    slot.save()

    params = create_seminar_params(slot.pk, student.name, student.email)
    response = client.post(POST_SEMINAR_URL, data=params)

    assert response.status_code == 400
    assert len(Order.objects.all()) == 0


# Seminars Data Access Tests

@pytest.mark.django_db
def test_get_future_seminar_slots_future_only(client):
    seminar = t_util.create_activity(activity_type=Activity.SEMINAR, order=1)

    created_slot_pair = t_util.create_seminar_slot_pair(seminar)

    response = client.get(
        reverse(
            'sem-slots',
            kwargs={'seminar_id': seminar.id}
        )
    )

    assert response.status_code == 200
    ret = json.loads(response.content)['slots']

    assert len(ret) == 1
    assert ret[0]['id'] == created_slot_pair['future'].id


@pytest.mark.django_db
def test_get_future_seminar_slots_sorted(client):
    seminar = t_util.create_activity(activity_type=Activity.SEMINAR, order=1)

    t_util.create_seminar_slot(
        seminar,
        *(timezone.now() + timedelta(days=i) for i in range(5, 1))
    )

    response = client.get(reverse('sem-slots', kwargs={'seminar_id': seminar.id}))

    ret = [slot['id'] for slot in json.loads(response.content)['slots']]
    assert ret == [slot.id for slot in SeminarSlot.objects.order_by('start_datetime')]


@pytest.mark.django_db
def test_get_activities(client):
    t_util.create_activity(activity_type=Activity.SEMINAR, order=2)
    t_util.create_activity(activity_type=Activity.SEMINAR, order=1)
    t_util.create_activity(activity_type=Activity.INDIVIDUAL)

    test_cases = [
        (Activity.SEMINAR, 2),
        (Activity.INDIVIDUAL, 1),
        ('NOT REAL', 0),
    ]

    for activity_type, exp_num, in test_cases:
        response = client.get(reverse(
            'get-activities', kwargs={'activity_type': activity_type}
        ))

        # successful request
        assert response.status_code == 200

        # assert data is of expected length and type
        activities = json.loads(response.content)['activities']
        assert len(activities) == exp_num

        # assert ordered and type
        for i, activity in enumerate(activities):
            if i > 0:
                assert activities[i-1]['order_shown'] < activity['order_shown']
            assert activity['activity_type'] == activity_type


@pytest.mark.django_db
def test_get_upcoming_seminars_success(client):
    sem_foo = t_util.create_activity(activity_type=Activity.SEMINAR, title='foo')
    sem_bar = t_util.create_activity(activity_type=Activity.SEMINAR, title='bar')

    tmw = timezone.now() + timedelta(days=1, minutes=10)
    t_util.create_seminar_slot(sem_foo, tmw)
    t_util.create_seminar_slot(sem_bar, tmw)

    response = client.get(reverse('get-upcoming-seminars'))
    assert response.status_code == 200

    ret = json.loads(response.content)
    exp = [
        {
            'date': tmw.strftime(UPCOMING_DT_FORMAT),
            'seminars': [   # sorted
                'bar',
                'foo',
            ]
        }
    ]

    assert ret == exp


@pytest.mark.django_db
def test_get_upcoming_seminars_count(client):
    seminar = t_util.create_activity(activity_type=Activity.SEMINAR, title='foo')
    dts = [timezone.now() + timedelta(days=i, minutes=1) for i in range(1, 365, 100)]
    t_util.create_seminar_slot(seminar, *dts)


    response = client.get(reverse('get-upcoming-seminars'))
    upcoming = json.loads(response.content)

    assert len(upcoming) == 3   # only the next 3 days
    for i, day in enumerate(upcoming):
        assert day['date'] == dts[i].strftime(UPCOMING_DT_FORMAT)


@pytest.mark.django_db
def test_get_upcoming_seminars_future_only(client):
    now = timezone.now()
    seminar = t_util.create_activity(activity_type=Activity.SEMINAR, title='foo')
    dts = (now + timedelta(days=i) for i in range(5, -2, -1))
    t_util.create_seminar_slot(seminar, *dts)


    response = client.get(reverse('get-upcoming-seminars'))
    upcoming_seminars = json.loads(response.content)

    for day in upcoming_seminars:
        upcoming_dt = datetime.datetime.strptime(day['date'], UPCOMING_DT_FORMAT)
        upcoming_dt = now.replace(month=upcoming_dt.month, day=upcoming_dt.day)
        assert  upcoming_dt > now


@pytest.mark.django_db
def test_get_upcoming_seminars_unique(client):
    seminar = t_util.create_activity(activity_type=Activity.SEMINAR, title='foo')

    # add 2 slots on same day
    now = timezone.now()
    t_util.create_seminar_slot(seminar, (now + timedelta(days=1)))
    t_util.create_seminar_slot(seminar, (now + timedelta(days=1)))

    response = client.get(reverse('get-upcoming-seminars'))
    ret = json.loads(response.content)

    assert len(ret) == 1    # single day
    assert ret[0]['seminars'] == ['foo']


# VIDEO PAGES

video_request = lambda slot_id: reverse('video-view', kwargs={'slot_id': slot_id})


@pytest.mark.django_db
def test_seminar_video_page_success(client):
    # setup a slot and seminar
    seminar = t_util.create_activity(activity_type=Activity.SEMINAR, title='foo')
    slot = t_util.create_seminar_slot(
        seminar,
        timezone.now() - timedelta(hours=1),
        video_id='FOOBAR'
    )

    response = client.get(video_request(slot.external_id))

    assert response.status_code == 200

    # assert correct info included
    assert 'data' in response.context

    video_data = json.loads(response.context['data'])
    assert video_data['video_id'] == 'FOOBAR'
    assert video_data['title'] == seminar.title
    assert not video_data['error']


@pytest.mark.django_db
def test_seminar_video_page_not_found(client):
    response = client.get(video_request(uuid4()))

    assert response.status_code == 404


@pytest.mark.django_db
def test_seminar_video_page_too_early(client):
    seminar = t_util.create_activity(activity_type=Activity.SEMINAR, title='foo')
    slot = t_util.create_seminar_slot(seminar, timezone.now() + timedelta(hours=1))

    response = client.get(video_request(slot.external_id))
    assert response.status_code == 200

    video_data = json.loads(response.context['data'])
    assert video_data['video_id'] is None
    assert 'will be available' in video_data['error']


@pytest.mark.django_db
def test_seminar_video_page_too_late(client):
    seminar = t_util.create_activity(activity_type=Activity.SEMINAR, title='foo')
    slot = t_util.create_seminar_slot(seminar, timezone.now() - timedelta(hours=24, minutes=1))

    response = client.get(video_request(slot.external_id))
    assert response.status_code == 200

    video_data = json.loads(response.context['data'])
    assert video_data['video_id'] is None
    assert 'ended' in video_data['error']


# HELPER FUNCTIONS

def create_seminar_params(slot, name='name', email='email@email.com'):
    """Creates params for POST request"""
    return {
        KEY_CHOICE: slot,
        KEY_NAME: name,
        KEY_EMAIL: email,
    }
