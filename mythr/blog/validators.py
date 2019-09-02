from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
import re
import datetime


def password_match_validator(password1, password2):
    if password1 != password2:
        raise ValidationError(
            _("Password and Confirm Password do not match")
        )
