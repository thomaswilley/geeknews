from django import forms
from registration.forms import RegistrationFormUniqueEmail
from django.utils.translation import ugettext_lazy as _

class RegistrationFormUniqueEmailTermsOfService(RegistrationFormUniqueEmail):
    """
    Subclass of ``RegistrationFormUniqueEmail`` which adds a required checkbox
    for agreeing to a site's Terms of Service.
    """
    next = forms.CharField(widget=forms.HiddenInput),
    tos = forms.BooleanField(widget=forms.CheckboxInput,
            error_messages={'required': _("You must agree to the terms of serivce to sign up")})


