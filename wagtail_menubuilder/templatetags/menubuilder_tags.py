from django import template
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.template.loader import select_template

from wagtail_menubuilder.models import Menu, MenuItem

register = template.Library()

CACHE_TIMEOUT = 600  # 10 minutes
CACHE_KEY_PREFIX = "wagtail_menubuilder_menu_"


def _cache_key(slug):
    return f"{CACHE_KEY_PREFIX}{slug}"


def _build_menu_context(menu):
    """Fetch and process top-level items for a menu object."""
    navigation_items = menu.menu_items.filter(parent=None).prefetch_related(
        "children",
        "children__internal_link",
        "internal_link",
    )

    visible_items = []
    for item in navigation_items:
        processed = process_menu_item(item)
        if processed:
            visible_items.append(processed)

    return visible_items


@register.inclusion_tag("wagtail_menubuilder/default.html", takes_context=True)
def render_menu(context, menu_slug):
    """
    Render a menu by slug.

    Usage::

        {% load menubuilder_tags %}
        {% render_menu "main-nav" %}

    The tag looks for a template named ``wagtail_menubuilder/<slug>.html``
    and falls back to ``wagtail_menubuilder/menu-default.html`` if none exists.
    Results are cached for 10 minutes (CACHE_TIMEOUT). The cache is
    automatically cleared whenever a Menu or MenuItem is saved or deleted.
    """
    request = context.get("request")

    cache_key = _cache_key(menu_slug)
    cached = cache.get(cache_key)

    if cached is not None:
        cached["request"] = request
        return cached

    try:
        menu = Menu.objects.get(slug=menu_slug)
    except Menu.DoesNotExist:
        return {
            "menu": None,
            "visible_items": [],
            "template": None,
            "request": request,
        }

    visible_items = _build_menu_context(menu)

    # Resolve template: slug-specific first, generic fallback second
    resolved_template = select_template([
        f"wagtail_menubuilder/{menu_slug}.html",
        "wagtail_menubuilder/menu-default.html",
    ])
    # Note: to override for a specific menu slug, create:
    # <your_app>/templates/wagtail_menubuilder/<slug>.html

    result = {
        "menu": menu,
        "visible_items": visible_items,
        "template": resolved_template.template.name,
    }

    cache.set(cache_key, result, CACHE_TIMEOUT)

    result["request"] = request
    return result


def process_menu_item(item):
    """
    Recursively process a menu item and its children.
    Returns None if the item should be hidden (links to an unpublished page).
    Attaches ``visible_children`` to each item for use in templates.
    """
    if item.internal_link and not item.internal_link.live:
        return None

    visible_children = []
    for child in item.children.all():
        processed = process_menu_item(child)
        if processed:
            visible_children.append(processed)

    item.visible_children = visible_children
    return item


# ---------------------------------------------------------------------------
# Cache invalidation
# ---------------------------------------------------------------------------

@receiver(post_save, sender=Menu)
@receiver(post_delete, sender=Menu)
def invalidate_menu_cache_on_menu_change(sender, instance, **kwargs):
    cache.delete(_cache_key(instance.slug))


@receiver(post_save, sender=MenuItem)
@receiver(post_delete, sender=MenuItem)
def invalidate_menu_cache_on_item_change(sender, instance, **kwargs):
    cache.delete(_cache_key(instance.menu.slug))
