from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
import re


class CustomPasswordValidator(object):
    def validate(self, password, user=None):
        if password.islower():
            raise ValidationError(
                _("Password must contain uppercase letters.")
            )
        if password.isupper():
            raise ValidationError(
                _("Password must contain lowercase letters.")
            )
        if not bool(re.search(r'\d', password)):
            raise ValidationError(
                _("Password must contain digits.")
            )
        if not bool(re.search(r'[@#$]', password)):
            raise ValidationError(
                _("Password must contain '@', '#' or '$'.")
            )

    def get_help_text(self):
        return _(
            "Your password must contain both uppercase and lowercase "
            "letters, digits, and special characters."
        )
