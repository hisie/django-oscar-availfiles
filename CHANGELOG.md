# Changelog

All notable changes to this project are documented in this file.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

## [0.2.1] - 2026-10-02

### Changed

- Widened the `django-availfiles` dependency constraint from
  `>=0.2.0,<0.3` to `>=0.2.0,<1.0` — matches this project's wider
  version-pinning policy (patch/minor releases across this package
  family shouldn't need a dependency-constraint edit downstream).
- Removed the now-stale `[tool.uv.sources]` local-path override for
  `django-availfiles` — it's genuinely published now, no longer needs a
  path dependency for local development.

## [0.2.0] - 2026-09-30

First real release. Published as `django-oscar-simplefiles` initially;
renamed to follow `django-availfiles`'s own rename (PyPI rejected that
name as too similar to the existing `django-simple-files`) — 0.1.0 was
built under the old name but never actually published.

### Added

- An Oscar dashboard section under `/dashboard/availfiles/` (list/
  upload/delete) for `django-availfiles`' `AvailFile` model, images
  rejected by default (configurable), and a JSON listing endpoint
  feeding a TinyMCE `file_picker_callback` — so an editor can link to an
  already-uploaded file from any wysiwyg field's "Insert Link" dialog.
- 8 tests, 97% coverage.

[Unreleased]: https://github.com/hisie/django-oscar-availfiles/compare/0.2.1...HEAD
[0.2.1]: https://github.com/hisie/django-oscar-availfiles/compare/0.2.0...0.2.1
[0.2.0]: https://github.com/hisie/django-oscar-availfiles/releases/tag/0.2.0
