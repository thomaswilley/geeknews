"""
URLconf for registration and activation, using django-registration's
default backend as the starting point.

"""

from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from django.views.generic.base import TemplateView

from registration_custombackend.forms import RegistrationFormUniqueEmailTermsOfService
from registration_custombackend.views import RegistrationView

from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse_lazy

urlpatterns = patterns('',
        url(r'^register/$',
            RegistrationView.as_view(form_class=RegistrationFormUniqueEmailTermsOfService),
            name='registration_register'),
        url(r'^register/closed/$',
            TemplateView.as_view(template_name='registration/registration_closed.html'),
            name='registration_disallowed'),
        (r'', include('registration.auth_urls')),
        )
