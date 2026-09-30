from django.urls import path
from django.utils.translation import gettext_lazy as _
from oscar.core.application import OscarDashboardConfig
from oscar.core.loading import get_class


class AvailFilesDashboardConfig(OscarDashboardConfig):
    label = "availfiles_dashboard"
    name = "oscar_availfiles.dashboard"
    verbose_name = _("Avail files dashboard")

    default_permissions = [
        "is_staff",
    ]

    def configure_permissions(self):
        DashboardPermission = get_class("dashboard.permissions", "DashboardPermission")

        self.permissions_map = {
            "availfiles-list": DashboardPermission.get("availfiles", "view_availfile"),
            "availfiles-create": DashboardPermission.get(
                "availfiles", "view_availfile", "add_availfile"
            ),
            "availfiles-delete": DashboardPermission.get(
                "availfiles", "view_availfile", "delete_availfile"
            ),
            "availfiles-list-json": DashboardPermission.get("availfiles", "view_availfile"),
        }

    # pylint: disable=attribute-defined-outside-init
    def ready(self):
        self.list_view = get_class("oscar_availfiles.dashboard.views", "AvailFileListView")
        self.create_view = get_class("oscar_availfiles.dashboard.views", "AvailFileCreateView")
        self.delete_view = get_class("oscar_availfiles.dashboard.views", "AvailFileDeleteView")
        self.json_list_view = get_class("oscar_availfiles.dashboard.views", "AvailFileJSONListView")
        self.configure_permissions()

    def get_urls(self):
        urls = [
            path("", self.list_view.as_view(), name="availfiles-list"),
            path("create/", self.create_view.as_view(), name="availfiles-create"),
            path("delete/<int:pk>/", self.delete_view.as_view(), name="availfiles-delete"),
            path("list.json", self.json_list_view.as_view(), name="availfiles-list-json"),
        ]
        return self.post_process_urls(urls)
