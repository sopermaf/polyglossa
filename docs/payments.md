Payments
===

Payments are made on the wesite using paypal and through the use of [django-paypal](https://django-paypal.readthedocs.io/en/stable/index.html)


Paypal
---
- Sandbox for simulating requests
- Uses IPN signals to confirm payment status after attempted payment


Process
---

1. Signup / Purchase Form

```mermaid
graph TD
    form(Class Booking Form)
    purchase-form(Course Purchase)
    paypal-button(PayPal Button Page)
    order-create(Order Details addd to DB)
    paypal-redirect(Redirected to PayPal for Payments)
    payment-made(Payment Finished)
    payment-cancelled(Payment Cancelled)

    form --> paypal-button
    purchase-form --> paypal-button
    paypal-button --> order-create
    order-create --> paypal-redirect
    paypal-redirect --> payment-made
    paypal-redirect --> payment-cancelled
```

2. Reacting to Paypal IPN Signals

```mermaid
graph TD
    ipn-signal(PayPal IPN Signal)
    valid-ipn(valid_ipn_received)
    order-complete(Order details retrieved by DB)
    seminar(Add Student to Seminar)
    individual(Confirm 1-to-1 lesson)
    purchase(Prepare Sending of Item)
    invalid-ipn(invalid_ipn_received)
    order-incomplete(Mark Order as Incomplete)
    email(Notify User of Booking Status)

    ipn-signal --> valid-ipn
    valid-ipn --> order-complete
    order-complete --> seminar
    order-complete --> individual
    order-complete --> purchase
    seminar --> email
    individual --> email
    purchase --> email

    invalid-ipn --> order-incomplete
    ipn-signal --> invalid-ipn
    order-incomplete --> email
```