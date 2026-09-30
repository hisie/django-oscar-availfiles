from oscar.core.application import OscarConfig


class OscarSimpleFilesConfig(OscarConfig):
    name = "oscar_simplefiles"
    label = "oscar_simplefiles"
    verbose_name = "Simple files (Oscar integration)"
    default_auto_field = "django.db.models.BigAutoField"
