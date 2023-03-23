from django.core.mail import send_mail
from django.conf import settings


def send_email(subject, email_address, content):
    """ Send customized email to given email address """
    return send_mail(subject=subject, from_email=settings.FROM_EMAIL_ADDRESS,
                    html_message=content, message='', recipient_list=[email_address])


def send_mail_otp(email_address, otp):
    """ Send otp code to given email address """
    subject = "Devonetwork Account Activation"
    message = f"""Hello dear {email_address}, welcome to devonetwork :)
    Here is your activation code:
    <b>{otp}</b>
    
    Thank you for registration.
    """
    return send_mail(subject=subject, message='', html_message=message,
                from_email=settings.FROM_EMAIL_ADDRESS, recipient_list=[email_address])
