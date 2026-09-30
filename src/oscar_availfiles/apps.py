from oscar.core.application import OscarConfig


class OscarAvailFilesConfig(OscarConfig):
    name = "oscar_availfiles"
    label = "oscar_availfiles"
    verbose_name = "Avail files (Oscar integration)"
    default_auto_field = "django.db.models.BigAutoField"
