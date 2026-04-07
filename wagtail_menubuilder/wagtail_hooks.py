from wagtail.admin.ui.tables import UpdatedAtColumn
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import Menu


class MenuViewSet(SnippetViewSet):
    model = Menu
    icon = "list-ul"
    menu_label = "Menus"
    menu_order = 300
    list_display = ["title", "slug", UpdatedAtColumn()]
    search_fields = ["title", "slug"]
    list_per_page = 20
    copy_view_enabled = True


register_snippet(MenuViewSet)
