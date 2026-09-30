from django.urls import path
from django.utils.translation import gettext_lazy as _
from oscar.core.application import OscarDashboardConfig
from oscar.core.loading import get_class


class SimpleFilesDashboardConfig(OscarDashboardConfig):
    label = "simplefiles_dashboard"
    name = "oscar_simplefiles.dashboard"
    verbose_name = _("Simple files dashboard")

    default_permissions = [
        "is_staff",
    ]

    def configure_permissions(self):
        DashboardPermission = get_class("dashboard.permissions", "DashboardPermission")

        self.permissions_map = {
            "simplefiles-list": DashboardPermission.get("simplefiles", "view_simplefile"),
            "simplefiles-create": DashboardPermission.get(
                "simplefiles", "view_simplefile", "add_simplefile"
            ),
            "simplefiles-delete": DashboardPermission.get(
                "simplefiles", "view_simplefile", "delete_simplefile"
            ),
            "simplefiles-list-json": DashboardPermission.get("simplefiles", "view_simplefile"),
        }

    # pylint: disable=attribute-defined-outside-init
    def ready(self):
        self.list_view = get_class("oscar_simplefiles.dashboard.views", "SimpleFileListView")
        self.create_view = get_class("oscar_simplefiles.dashboard.views", "SimpleFileCreateView")
        self.delete_view = get_class("oscar_simplefiles.dashboard.views", "SimpleFileDeleteView")
        self.json_list_view = get_class(
            "oscar_simplefiles.dashboard.views", "SimpleFileJSONListView"
        )
        self.configure_permissions()

    def get_urls(self):
        urls = [
            path("", self.list_view.as_view(), name="simplefiles-list"),
            path("create/", self.create_view.as_view(), name="simplefiles-create"),
            path("delete/<int:pk>/", self.delete_view.as_view(), name="simplefiles-delete"),
            path("list.json", self.json_list_view.as_view(), name="simplefiles-list-json"),
        ]
        return self.post_process_urls(urls)
