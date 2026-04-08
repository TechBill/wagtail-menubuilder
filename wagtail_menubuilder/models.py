from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from wagtail.models import Orderable, Page
from wagtail.admin.panels import FieldPanel, InlinePanel, PageChooserPanel
from wagtail.search import index
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


class Menu(index.Indexed, ClusterableModel):
    title = models.CharField(max_length=255, unique=True, help_text="Menu title.")
    slug = models.SlugField(unique=True, help_text="Unique identifier used to render this menu in templates.")

    panels = [
        FieldPanel("title"),
        FieldPanel("slug"),
        InlinePanel("menu_items", label="Menu Items"),
    ]

    search_fields = [
        index.SearchField("title"),
        index.FilterField("slug"),
    ]

    class Meta:
        verbose_name = "Menu"
        verbose_name_plural = "Menus"

    def __str__(self):
        return self.title


class MenuItemAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "parent" in self.fields:
            if self.instance and self.instance.pk and self.instance.menu_id:
                self.fields["parent"].queryset = MenuItem.objects.filter(
                    menu_id=self.instance.menu_id
                ).exclude(pk=self.instance.pk)
            else:
                self.fields["parent"].queryset = MenuItem.objects.none()
            self.fields["parent"].empty_label = "— None (top-level item) —"
            self.fields["parent"].help_text = (
                "Save the menu first, then edit items individually to assign a parent."
            )


class MenuItem(Orderable):
    base_form_class = MenuItemAdminForm
    menu = ParentalKey(
        "wagtail_menubuilder.Menu",
        on_delete=models.CASCADE,
        related_name="menu_items",
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="children",
        help_text="Set a parent item to create a dropdown. Must belong to the same menu.",
    )
    title = models.CharField(max_length=255, help_text="Text displayed in the menu.")
    url = models.URLField(
        blank=True,
        null=True,
        help_text="External URL. Leave blank if using an internal page link or this is a dropdown parent.",
    )
    internal_link = models.ForeignKey(
        Page,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="menu_links",
        help_text="Internal page link. Overrides external URL if set.",
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("url"),
        PageChooserPanel("internal_link"),
        FieldPanel("parent"),
    ]

    def clean(self):
        super().clean()

        if self.parent_id:
            # Prevent an item from being its own parent
            if self.pk and self.parent_id == self.pk:
                raise ValidationError({"parent": "A menu item cannot be its own parent."})

            # Prevent cross-menu parent assignment.
            # self.menu_id may be None for new inline items (modelcluster holds the
            # relation in memory before the first save), so only validate when both
            # sides have a known PK.
            if self.menu_id and self.parent.menu_id and self.parent.menu_id != self.menu_id:
                raise ValidationError({"parent": "Parent item must belong to the same menu."})

            # Prevent circular reference chains (e.g. A → B → A)
            ancestor = self.parent
            while ancestor is not None:
                if self.pk and ancestor.pk == self.pk:
                    raise ValidationError({"parent": "This parent selection creates a circular reference."})
                ancestor = ancestor.parent

    def get_url(self):
        """Return the URL, prioritising the internal link."""
        if self.internal_link and self.internal_link.live:
            return self.internal_link.url
        return self.url or "#"

    def is_visible(self):
        """Return False if this item links to an unpublished page."""
        if self.internal_link and not self.internal_link.live:
            return False
        return True

    def __str__(self):
        return self.title
