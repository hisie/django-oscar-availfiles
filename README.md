# django-oscar-simplefiles

Wires [django-simplefiles](https://github.com/hisie/django-simplefiles)
into [django-oscar](https://github.com/django-oscar/django-oscar): an
Oscar dashboard section to upload/browse files, plus the pieces needed to
let editors link to them from a TinyMCE "Insert Link" dialog in any
dashboard wysiwyg field (a blog post body, a product description, ...).

## What this package does, and doesn't, do

- An Oscar dashboard section under `/dashboard/simplefiles/`: list/
  upload/delete. Uploads are rejected if their content-type starts with
  `image/` by default (configurable via
  `OSCAR_SIMPLEFILES_REJECTED_CONTENT_TYPES`) — images already have their
  own drag-and-drop-into-the-editor upload flow in a typical Oscar
  dashboard TinyMCE setup; this library is for everything else (PDFs,
  spec sheets, downloadable docs).
- A JSON listing endpoint (`dashboard:simplefiles-list-json`, optionally
  filtered by `?q=<term>` against label/filename) — read-only, meant to
  feed a TinyMCE `file_picker_callback`, not a general API.
- It does **not** upload new files from inside the TinyMCE dialog itself
  — the flow is: upload once via the dashboard, then link to it from
  anywhere via the picker. It also doesn't touch the image-upload flow at
  all; that's a separate, pre-existing concern in whatever project this
  is installed into.

## Installation

```
uv add django-oscar-simplefiles
```

```python
INSTALLED_APPS = [
    ...,
    "simplefiles",
    "oscar_simplefiles.apps.OscarSimpleFilesConfig",
    "oscar_simplefiles.dashboard.apps.SimpleFilesDashboardConfig",
]
```

Run `manage.py migrate` — `simplefiles` ships the actual model migration;
this package has none of its own.

## Wiring the dashboard in

Same fork every dashboard extension in this family needs (Oscar's
`DashboardConfig.get_urls()` is a hardcoded list) — see this package's own
`tests/dashboard.py` for a worked example:

```python
from django.apps import apps
from django.urls import include, path
from oscar.apps.dashboard.apps import DashboardConfig as OscarDashboardConfig


class DashboardConfig(OscarDashboardConfig):
    def ready(self):
        super().ready()
        self.simplefiles_app = apps.get_app_config("simplefiles_dashboard")

    def get_urls(self):
        urls = super().get_urls()
        urls.append(path("simplefiles/", include(self.simplefiles_app.urls[0])))
        return urls
```

## Wiring the TinyMCE file picker in

This has to live in the host project's own dashboard layout override
(`templates/oscar/dashboard/layout.html`'s `onbodyload` block, where
`oscar.dashboard.init(options)` is called) — the same place an image
upload handler would be wired, if one exists. Add a `file_picker_callback`
to `tinyConfig` that opens a small popup fed by the JSON endpoint above:

```javascript
function simplefilesPickerCallback(callback, value, meta) {
    if (meta.filetype !== 'file') {
        return;  // only handling the plain "link" picker, not image/media
    }
    fetch('{% url "dashboard:simplefiles-list-json" %}')
        .then(function (response) { return response.json(); })
        .then(function (data) {
            var win = tinymce.activeEditor.windowManager.open({
                title: 'Choose a file',
                body: {
                    type: 'panel',
                    items: data.files.map(function (f) {
                        return { type: 'button', text: f.display_name, name: 'file_' + f.id };
                    })
                },
                buttons: [{ type: 'cancel', text: 'Close' }],
                onAction: function (dialogApi, details) {
                    var id = parseInt(details.name.replace('file_', ''), 10);
                    var chosen = data.files.find(function (f) { return f.id === id; });
                    if (chosen) {
                        callback(chosen.url, { text: chosen.display_name });
                        dialogApi.close();
                    }
                }
            });
        });
}

options.tinyConfig.file_picker_callback = simplefilesPickerCallback;
options.tinyConfig.file_picker_types = 'file';
```

(`file_picker_types = 'file'` restricts the picker to the plain-link case
— TinyMCE also offers `image`/`media` pickers, which this package doesn't
handle; leave those to whatever already handles image uploads.)

## Development

```
uv sync
uv run pytest
```

Requires `django-simplefiles`, wired in `pyproject.toml`'s
`[tool.uv.sources]` as a local path dependency until it's published.
