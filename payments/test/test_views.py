'''
Tests for payments.views
'''
# pylint: disable=missing-function-docstring
import json
import datetime

import pytest
from django.urls import reverse
from django.utils import timezone

from class_bookings.test import util as t_util
from class_bookings.models import Activity, Student
from class_bookings import const as cb_const
from tasks.models import EmailTask
from ..models import Order


ORDER_PAGE = reverse('order-page')
CANCEL_ORDER = reverse('cancel-awaiting')


@pytest.mark.django_db
def test_cancel_order_success(client):
    # setup cookie from `payments.views.paypal_button`
    _setup_session_order(client.session)

    response = client.post(CANCEL_ORDER)
    order = Order.objects.first()

    assert response.status_code == cb_const.SUCCESS_CODE
    assert order.payment_status == Order.PaymentStatus.CANCELLED


def test_cancel_order_error_not_found(client):
    response = client.post(reverse('cancel-awaiting'))
    assert response.status_code == 404


@pytest.mark.django_db
def test_payment_page_success_payment_not_required(client):
    seminar = t_util.create_activity(price=0)
    slot = t_util.create_seminar_slot(seminar, timezone.now() + datetime.timedelta(days=2))
    order = _setup_seminar_order(seminar=seminar, slot=slot)
    _setup_session_order(client.session, order=order)

    response = client.get(ORDER_PAGE)

    assert response.status_code == 200
    assert 'data' in response.context
    page_data = json.loads(response.context['data'])
    assert 'order' in page_data
    assert page_data['button'] is None

    # order completion done immediately
    slot.refresh_from_db()
    order.refresh_from_db()
    assert order.payment_status == Order.PaymentStatus.COMPLETED
    assert slot.students.count() == 1
    assert EmailTask.objects.all().count() == 1


@pytest.mark.django_db
def test_payment_page_success_payment_required(client):
    _setup_session_order(client.session)

    response = client.get(ORDER_PAGE)

    assert response.status_code == 200
    assert 'data' in response.context

    page_data = json.loads(response.context['data'])
    assert 'order' in page_data
    assert 'button' in page_data
    assert all(key in page_data['button'] for key in ('url', 'encrypted_inputs'))

    order = Order.objects.first()
    assert order.payment_status == Order.PaymentStatus.AWAITING


def test_payment_page_error_no_order(client):
    response = client.get(ORDER_PAGE)

    assert response.status_code == 404


# UTIL FUNCTIONS

def _setup_session_order(session, order=None):
    """Add order to session"""
    if not order:
        order = _setup_seminar_order()

    session['order_id'] = order.pk
    session.save()


def _setup_seminar_order(customer=None, seminar=None, slot=None):
    """Create an order for a seminar"""
    if not customer:
        customer = Student.objects.create(name='foo', email='foo@bar.com')
    if not seminar:
        seminar = t_util.create_activity(
            activity_type=Activity.SEMINAR,
            bookable=True,
        )
    if not slot:
        slot = t_util.create_seminar_slot(seminar, timezone.now() + datetime.timedelta(days=1))


    order_details = {
        cb_const.KEY_CHOICE: slot.pk,
        cb_const.KEY_NAME: customer.name,
        cb_const.KEY_EMAIL: customer.email,
    }

    return Order.objects.create(
        customer=customer,
        payment_status=Order.PaymentStatus.AWAITING,
        processor=Order.ProcessorEnums.SEMINAR,
        order_details=json.dumps(order_details),
        amount=slot.seminar.price,
    )
