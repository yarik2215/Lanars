from django.db.models import DateTimeField, Model
from django.utils.translation import gettext_lazy as _


class TimestampModelMixin(Model):
    created_at = DateTimeField(_("created at"), auto_now_add=True)
    updated_at = DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        abstract = True