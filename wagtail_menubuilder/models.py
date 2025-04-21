from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, InlinePanel, PageChooserPanel
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from modelcluster.fields import Orderable
from wagtail.snippets.models import register_snippet

@register_snippet
class Menu(ClusterableModel):
    title = models.CharField(max_length=255, unique=True, help_text="Menu Title")
    slug = models.SlugField(unique=True, help_text="Unique identifier for this menu.")

    panels = [
        FieldPanel("title"),
        FieldPanel("slug"),
        InlinePanel("menu_items", label="Menu Items"),
    ]

    class Meta:
        verbose_name = "Menubuilder"
        verbose_name_plural = "Menubuilder"

    def __str__(self):
        return self.title


class MenuItem(Orderable):
    menu = ParentalKey("wagtail_menubuilder.Menu", on_delete=models.CASCADE, related_name="menu_items")
    parent = ParentalKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="children",
        help_text="Set a parent menu item to create a dropdown.",
    )
    title = models.CharField(max_length=255, blank=False, help_text="Menu Item Title") # Added blank=False
    url = models.URLField(blank=True, null=True, help_text="External URL for this menu item. Leave blank if this is a dropdown parent.") # Updated help_text
    internal_link = models.ForeignKey(
        Page,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="menu_links",
        help_text="Internal link to a page. Overrides external URL if set.",
    )
    # is_dropdown field removed
    order = models.PositiveIntegerField(default=0, help_text="Menu item display order.")

    panels = [
        FieldPanel("title"),
        FieldPanel("url"),
        PageChooserPanel("internal_link"), # Changed to PageChooserPanel
        # is_dropdown panel removed
        FieldPanel("parent"),
        FieldPanel("order"),
    ]

    class Meta:
        ordering = ["order"]

    def get_url(self):
        """Return the URL, prioritizing the internal link."""
        if self.internal_link and self.internal_link.live:
            return self.internal_link.url
        return self.url or "#"

    def is_visible(self):
        """Determine if this menu item should be visible."""
        if self.internal_link and not self.internal_link.live:
            return False
        return True

    def __str__(self):
        return self.title