"""Test-only fork of Oscar's DashboardConfig that mounts
availfiles_dashboard — the same fork a host project needs to make, same
pattern as django-oscar-blog's/django-oscar-freeletter's own
tests/dashboard.py, which this package's README points to."""

from __future__ import annotations

from django.apps import apps
from django.urls import include, path
from oscar.apps.dashboard.apps import DashboardConfig as OscarDashboardConfig


class DashboardConfig(OscarDashboardConfig):
    def ready(self):
        super().ready()
        self.availfiles_app = apps.get_app_config("availfiles_dashboard")

    def get_urls(self):
        urls = super().get_urls()
        urls.append(path("availfiles/", include(self.availfiles_app.urls[0])))
        return urls
