from django import template
from menubuilder.models import Menu

register = template.Library()


@register.inclusion_tag("menubuilder/default.html", takes_context=True)
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

        return {
            "menu": menu,
            "navigation_items": visible_items,
            "template": f"menubuilder/{menu_slug}.html",
            "request": context["request"],
        }
    except Menu.DoesNotExist:
        return {
            "menu": None,
            "navigation_items": [],
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
        
        # If it's a dropdown and has no visible children, hide it
        if item.is_dropdown and not visible_children:
            return None
        
        # Set the visible children on the item
        item.visible_children = visible_children
    else:
        item.visible_children = []

    # Set the URL for the item
    if item.internal_link:
        item.url = item.internal_link.url
    
    return item