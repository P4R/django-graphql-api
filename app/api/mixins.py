from smtplib import SMTPException

from app.settings import DOMAIN_URL
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from graphql_auth.bases import Output
from graphql_auth.constants import Messages


class SendPasswordResetEmailMixin(Output):

    @classmethod
    def resolve_mutation(cls, root, info, **kwargs):
        try:
            email = kwargs.get("email")
            if User.objects.filter(email=email).exists():
                form = PasswordResetForm({'email': email})
                if form.is_valid():
                    form.save(
                        domain_override=DOMAIN_URL)
                    return cls(success=True)
                return cls(success=False, errors=form.errors.get_json_data())
            else:
                return cls(success=False, errors=["User email not found"])
        except ObjectDoesNotExist:
            return cls(success=True)
        except SMTPException:
            return cls(success=False, errors=Messages.EMAIL_FAIL)
