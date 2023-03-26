from celery import shared_task
from .email import send_email, send_mail_otp, reset_password_email


@shared_task
def email_sender_otp(*args, **kwargs):
    """ Function for otp sending emails with celery """
    return send_mail_otp(*args, **kwargs)


@shared_task
def email_sender(*args, **kwargs):
    """ Function for sending emails with celery """
    return send_email(*args, **kwargs)


@shared_task
def email_reset_password_sender(*args, **kwargs):
    """ Function for sending reset password emails """
    return reset_password_email(*args, **kwargs)
