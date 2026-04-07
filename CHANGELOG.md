# Changelog

All notable changes to this project will be documented in this file.

---

## [0.4.0] - 2026-04-07

### Added

- **`SnippetViewSet`** (`wagtail_hooks.py`): Replaces the bare `@register_snippet`
  decorator. The admin list now shows title, slug, and last-updated columns, supports
  full-text search across title and slug, paginates at 20 per page, and enables the
  built-in "Copy" action. Requires Wagtail 5.0+ (stable in 6/7).
- **`prepopulate_from="title"` on the slug field**: The slug is now auto-filled as the
  editor types the menu title — no more manual slug entry.
- **`search_fields` on `Menu`**: Enables search in the snippet chooser and list view via
  Wagtail's `index.Indexed` mixin.
- **Generic fallback template** (`wagtail_menubuilder/menu-default.html`): The tag now
  uses `select_template` to try `wagtail_menubuilder/<slug>.html` first, then falls back
  to this built-in template. Previously a missing slug-specific template caused a hard
  `TemplateDoesNotExist` 500 error. The fallback template is fully accessible
  (ARIA roles, keyboard navigation, Escape key closes dropdowns) and mobile-responsive.
- **Menu caching in `render_menu`**: Results are cached per slug for 10 minutes
  (`CACHE_TIMEOUT = 600`). The cache is automatically cleared via Django signals whenever
  a `Menu` or `MenuItem` is saved or deleted, so editors always see fresh content
  immediately after saving.
- **`MenuItem.clean()` validation**:
  - Prevents an item from being set as its own parent.
  - Prevents assigning a parent that belongs to a different menu.
  - Detects and blocks circular reference chains (e.g. A → B → A).

### Fixed

- **Migration 0003 now preserves ordering data.** A `RunPython` step copies the old
  `order` field value into `sort_order` before dropping the column, so existing menu
  item ordering is not lost on upgrade.
- **`default.html` no longer renders a red error div** when a menu slug is not found.
  It now renders nothing (silent failure), which is the correct production behaviour.

### Changed

- **`@register_snippet` removed from `models.py`** — registration is now handled
  entirely by `MenuViewSet` in `wagtail_hooks.py`.
- **`default.html` wrapper simplified** — the error div removed; the template is now
  two meaningful lines.

---

## [0.3.0] - 2026-04-07

### Fixed

- **Drag-and-drop ordering was silently broken.** `MenuItem` inherited `sort_order` from
  `Orderable` (used by Wagtail's inline drag-and-drop) but also declared its own `order`
  field whose `Meta.ordering` override meant items always rendered in `order` sequence
  regardless of drag-and-drop changes. The custom `order` field has been removed; ordering
  now correctly uses `Orderable.sort_order`.
- **Stale `is_dropdown` database column.** The field was removed from the model in an
  earlier release without a migration, leaving the column orphaned in the database.
  Migration `0003` drops both `is_dropdown` and the removed `order` column.
- **`Orderable` was imported from `modelcluster.models`** instead of the correct
  `wagtail.models`. Both resolve at runtime, but the wagtail import is the documented
  and supported path from Wagtail 6 onwards.
- **Missing `templatetags/__init__.py`.** Django requires this file for template tag
  discovery; its absence could cause `{% load menubuilder_tags %}` to fail in some
  environments.
- **`context["request"]` raised `KeyError`** when the
  `django.template.context_processors.request` processor was not active. Changed to
  `context.get("request")`.
- **N+1 queries for nested menu items.** The prefetch did not cover
  `children__internal_link`, causing an extra query per child item to load its linked page.

### Changed

- `verbose_name` / `verbose_name_plural` on `Menu` changed from `"Menubuilder"` /
  `"Menubuilder"` to `"Menu"` / `"Menus"`.
- Python minimum version raised to 3.9 to align with Wagtail 7's dropped support
  for Python 3.8.

### Upgrade notes

After running `python manage.py migrate wagtail_menubuilder`, existing menu items will
have their ordering preserved via the `sort_order` copy step in migration 0003.

---

## [0.2.1] - 2025-01-17

- Bumped version and finalised package structure for PyPI.

## [0.2.0] - 2025-01-17

- Removed `is_dropdown` field; dropdown detection now relies on whether an item has
  visible children.
- Added `parent` field to `MenuItem` to support hierarchical/nested menus.
- Switched to `PageChooserPanel` for the `internal_link` field.
- Renamed context variable to `visible_items`.

## [0.1.8] - 2025-01-17

- Package structure fixes.

## [0.1.7] - 2025-01-17

- Initial public release.
