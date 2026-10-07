from django.utils.translation import gettext_lazy as _
from oscar.core.application import OscarConfig


class OscarAvailFilesConfig(OscarConfig):
    name = "oscar_availfiles"
    label = "oscar_availfiles"
    verbose_name = _("Avail files (Oscar integration)")
    default_auto_field = "django.db.models.BigAutoField"
