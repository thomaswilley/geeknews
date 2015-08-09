from registration import signals
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from registration_custombackend.views import RegistrationView

from django.conf import settings

@receiver(signals.user_registered, sender=RegistrationView)
def send_welcome_email(sender, **kwargs):
    user = kwargs['user']
    assert user is not None
    context = {
            "user": user,
            }
    subject = render_to_string("registration/signup/welcome_email_subject.txt", context)
    subject = subject.replace('\n', '') # just in case

    body = render_to_string("registration/signup/welcome_email.html", context)
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
