from django import template
from wagtail_menubuilder.models import Menu # Corrected import path

register = template.Library()


@register.inclusion_tag("wagtail_menubuilder/default.html", takes_context=True) # Corrected template path
def render_menu(context, menu_slug):
    """
    Renders a menu based on its slug, filtering out unpublished pages.
    """
    try:
        menu = Menu.objects.prefetch_related("menu_items__children").get(slug=menu_slug)

        # Get top-level items
        navigation_items = menu.menu_items.filter(parent=None).prefetch_related("children", "internal_link")

        # Process and filter items
        visible_items = []
        for item in navigation_items:
            processed_item = process_menu_item(item)
            if processed_item:
                visible_items.append(processed_item)

        # Determine the template to use, falling back to default if specific slug template doesn't exist
        # Note: Template existence check isn't done here, Django handles it during rendering.
        specific_template = f"wagtail_menubuilder/{menu_slug}.html"

        return {
            "menu": menu,
            "visible_items": visible_items, # Renamed context variable
            "template": specific_template, # Corrected template path prefix
            "request": context["request"],
        }
    except Menu.DoesNotExist:
        return {
            "menu": None,
            "visible_items": [], # Renamed context variable
            "template": None,
            "request": context["request"],
        }


def process_menu_item(item):
    """
    Recursively process menu items and their children.
    Returns None if the item should be hidden, otherwise returns the processed item.
    """
    # Skip items linking to unpublished pages
    if item.internal_link and not item.internal_link.live:
        return None

    # Process children if they exist
    if item.children.exists():
        visible_children = []
        for child in item.children.all():
            processed_child = process_menu_item(child)
            if processed_child:
                visible_children.append(processed_child)

        # If an item intended as a parent has no visible children, it might still be displayed
        # depending on template logic (e.g., as a non-clickable header or a direct link if it has one).
        # The check for `is_dropdown` is removed as the field is gone.
        # We now rely on the template to handle rendering based on `visible_children`.

        # Set the visible children on the item
        item.visible_children = visible_children
    else:
        item.visible_children = []

    # Removed manual setting of item.url - use item.get_url() in templates instead.

    return item