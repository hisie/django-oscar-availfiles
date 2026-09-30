from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views import generic
from oscar.core.loading import get_classes
from simplefiles.models import SimpleFile

SimpleFileSearchForm, SimpleFileUploadForm = get_classes(
    "oscar_simplefiles.dashboard.forms", ("SimpleFileSearchForm", "SimpleFileUploadForm")
)


def _label_or_filename(term):
    return Q(label__icontains=term) | Q(original_filename__icontains=term)


class SimpleFileListView(generic.ListView):
    template_name = "oscar/dashboard/simplefiles/index.html"
    model = SimpleFile
    form_class = SimpleFileSearchForm
    paginate_by = settings.OSCAR_DASHBOARD_ITEMS_PER_PAGE
    desc_template = "%(main_filter)s%(label_filter)s"

    def get_queryset(self):
        # pylint: disable=attribute-defined-outside-init
        self.desc_ctx = {"main_filter": _("All files"), "label_filter": ""}
        queryset = self.model.objects.all()

        # pylint: disable=attribute-defined-outside-init
        self.form = self.form_class(self.request.GET)
        if not self.form.is_valid():
            return queryset

        label = self.form.cleaned_data["label"]
        if label:
            queryset = queryset.filter(_label_or_filename(label))
            self.desc_ctx["label_filter"] = _(" matching '%s'") % label

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form
        context["queryset_description"] = self.desc_template % self.desc_ctx
        return context


class SimpleFileCreateView(generic.CreateView):
    template_name = "oscar/dashboard/simplefiles/update.html"
    model = SimpleFile
    form_class = SimpleFileUploadForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        if self.request.user.is_authenticated:
            obj.uploaded_by = self.request.user
        obj.save()
        self.object = obj
        messages.success(self.request, _("File '%s' uploaded") % obj.display_name)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("dashboard:simplefiles-list")


class SimpleFileDeleteView(generic.DeleteView):
    template_name = "oscar/dashboard/simplefiles/delete.html"
    model = SimpleFile

    def get_success_url(self):
        messages.success(self.request, _("Deleted file '%s'") % self.object.display_name)
        return reverse("dashboard:simplefiles-list")


class SimpleFileJSONListView(generic.View):
    """Feeds the TinyMCE file_picker_callback wired in the host project's
    own dashboard layout override (see this package's README) — a plain
    JSON listing, most recent first, optionally filtered by ?q=<term>
    against label/filename. Staff-only, same as every other view here."""

    def get(self, request, *args, **kwargs):
        queryset = SimpleFile.objects.all()
        term = request.GET.get("q")
        if term:
            queryset = queryset.filter(_label_or_filename(term))

        files = [
            {"id": obj.pk, "url": obj.file.url, "display_name": obj.display_name}
            for obj in queryset[:50]
        ]
        return JsonResponse({"files": files})
