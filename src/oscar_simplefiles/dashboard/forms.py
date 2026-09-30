from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from simplefiles.models import SimpleFile

# Images already have their own upload flow (drag-and-drop straight into
# a wysiwyg field, urbanplants/dashboard/views.py's EditorImageUploadView)
# — this library is deliberately for everything else, so images are
# rejected here by default rather than giving editors two different ways
# to do the same thing. A host project that genuinely wants images here
# too can override the setting.
DEFAULT_REJECTED_PREFIXES = ("image/",)


class SimpleFileSearchForm(forms.Form):
    label = forms.CharField(required=False, label=_("Label or filename"))


class SimpleFileUploadForm(forms.ModelForm):
    class Meta:
        model = SimpleFile
        fields = ("file", "label")

    def clean_file(self):
        upload = self.cleaned_data["file"]
        rejected_prefixes = getattr(
            settings, "OSCAR_SIMPLEFILES_REJECTED_CONTENT_TYPES", DEFAULT_REJECTED_PREFIXES
        )
        content_type = getattr(upload, "content_type", "") or ""
        if any(content_type.startswith(prefix) for prefix in rejected_prefixes):
            raise forms.ValidationError(
                _(
                    "This file type isn't accepted here — use the image upload in the editor instead."
                )
            )
        return upload
