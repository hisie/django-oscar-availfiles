import pytest
from availfiles.models import AvailFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

pytestmark = pytest.mark.django_db


@pytest.fixture
def staff_client(client, django_user_model):
    staff = django_user_model.objects.create_superuser(
        username="staff", email="staff@example.com", password="pw"
    )
    client.force_login(staff)
    return client


def make_pdf(name="care-sheet.pdf"):
    return SimpleUploadedFile(name, b"%PDF-1.4 fake", content_type="application/pdf")


def make_png(name="photo.png"):
    return SimpleUploadedFile(name, b"\x89PNG fake", content_type="image/png")


def test_anonymous_is_redirected_to_login(client):
    response = client.get(reverse("dashboard:availfiles-list"))
    assert response.status_code == 302


def test_staff_can_list_files(staff_client):
    AvailFile.objects.create(file=make_pdf())

    response = staff_client.get(reverse("dashboard:availfiles-list"))

    assert response.status_code == 200
    assert response.context["availfile_list"].count() == 1


def test_staff_can_upload_a_pdf_and_is_set_as_uploader(staff_client, django_user_model):
    response = staff_client.post(
        reverse("dashboard:availfiles-create"),
        {"file": make_pdf(), "label": "Care sheet"},
    )

    assert response.status_code == 302
    obj = AvailFile.objects.get(label="Care sheet")
    assert obj.uploaded_by.username == "staff"
    assert obj.original_filename == "care-sheet.pdf"


def test_uploading_an_image_is_rejected(staff_client):
    response = staff_client.post(
        reverse("dashboard:availfiles-create"),
        {"file": make_png(), "label": ""},
    )

    assert response.status_code == 200
    assert not AvailFile.objects.exists()
    assert "file" in response.context["form"].errors


def test_staff_can_delete_a_file(staff_client):
    obj = AvailFile.objects.create(file=make_pdf())

    response = staff_client.post(reverse("dashboard:availfiles-delete", kwargs={"pk": obj.pk}))

    assert response.status_code == 302
    assert not AvailFile.objects.filter(pk=obj.pk).exists()


def test_json_list_view_returns_url_and_display_name(staff_client):
    obj = AvailFile.objects.create(file=make_pdf(), label="Care sheet")

    response = staff_client.get(reverse("dashboard:availfiles-list-json"))

    assert response.status_code == 200
    data = response.json()
    assert data["files"] == [{"id": obj.pk, "url": obj.file.url, "display_name": "Care sheet"}]


def test_json_list_view_filters_by_query(staff_client):
    AvailFile.objects.create(file=make_pdf("care-sheet.pdf"), label="Care sheet")
    AvailFile.objects.create(file=make_pdf("warranty.pdf"), label="Warranty")

    response = staff_client.get(reverse("dashboard:availfiles-list-json"), {"q": "warranty"})

    data = response.json()
    assert [f["display_name"] for f in data["files"]] == ["Warranty"]


def test_json_list_view_requires_staff(client):
    response = client.get(reverse("dashboard:availfiles-list-json"))
    assert response.status_code == 302
