from django.db import migrations


def copy_order_to_sort_order(apps, schema_editor):
    """
    Copy the old `order` value into `sort_order` so that existing menu item
    ordering is preserved after the `order` field is dropped.
    Items that already have a sort_order set (from drag-and-drop) keep it;
    only rows with sort_order=NULL get the order value copied in.
    """
    MenuItem = apps.get_model("wagtail_menubuilder", "MenuItem")
    for item in MenuItem.objects.filter(sort_order__isnull=True):
        item.sort_order = item.order
        item.save(update_fields=["sort_order"])


class Migration(migrations.Migration):
    """
    1. Copy `order` → `sort_order` for any rows where sort_order is NULL.
    2. Drop `is_dropdown` (removed from the model without a migration).
    3. Drop `order` (redundant with Orderable.sort_order).
    """

    dependencies = [
        ("wagtail_menubuilder", "0002_menuitem_parent"),
    ]

    operations = [
        migrations.RunPython(copy_order_to_sort_order, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="menuitem",
            name="is_dropdown",
        ),
        migrations.RemoveField(
            model_name="menuitem",
            name="order",
        ),
    ]
