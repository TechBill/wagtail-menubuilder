# Wagtail MenuBuilder

A flexible and easy-to-use menu management system for Wagtail CMS that allows you to create and manage menus directly from the Wagtail admin interface.

---

## Features

- Create multiple menus with different slugs
- Hierarchical menu structure with unlimited depth
- Drag-and-drop menu item ordering
- Automatic page link updates when pages are moved
- Custom template support
- Built-in templates for common menu types (e.g., top navigation, footer)
- Wagtail 6.0+ compatible

---

## Requirements

- Python 3.8+
- Django 4.2+
- Wagtail 6.0+

---

## Installation

1. Install the package using pip:

   ```bash
   pip install wagtail-menubuilder
   ```

2. Add `wagtail_menubuilder` to your `INSTALLED_APPS` in `settings.py`:

   ```python
   INSTALLED_APPS = [
       ...
       'wagtail.admin',
       'wagtail.core',
       ...
       'wagtail_menubuilder',
       ...
   ]
   ```

3. Run migrations:

   ```bash
   python manage.py migrate wagtail_menubuilder
   ```

---

## Quick Start

### 1. Creating and Managing Menus

1. Access the **Wagtail Admin Panel**.
2. Navigate to **Snippets** in the left sidebar.
3. Click on **Menubuilder**.
4. Click **Add Menubuilder** to create a new menu.

### 2. Menu Configuration

- **Title**: Give your menu a descriptive name (e.g., "Main Navigation", "Footer Menu").
- **Slug**: Use a unique identifier (e.g., "main-nav", "footer").
- **Menu Items**: Add and organize your menu items:
  - Title: The text that appears in the menu.
  - URL: External link (optional).
  - Internal Link: Link to a Wagtail page (optional).
  - Parent Item: Create dropdown menus by setting a parent.

---

## Using Menus in Templates

### Rendering Menus

1. Load the template tags in your template:
   ```django
   {% load menubuilder_tags %}
   ```

2. Render a menu using its slug:
   ```django
   {% render_menu "your-menu-slug" %}
   ```

### Example: Using the `top-navbar.html` Template

The package includes an example template, `wagtail_menubuilder/templates/menubuilder/top-navbar.html`, which demonstrates a responsive navigation bar.
**Note:** This template is provided as a starting point. Its CSS and JavaScript are now in separate static files (`wagtail_menubuilder/static/menubuilder/css/top-navbar.css` and `js/top-navbar.js`) and should be included in your project's base template as shown below.

#### Steps to Use `top-navbar.html`:

1. **Add the Template to Your Base Template**

   Load the required tags and render the menu in your global template (e.g., `base.html`):

   ```django
   {% load static menubuilder_tags %}
   {% render_menu "top-navbar" %}
   ```

   If your template uses Wagtail-specific features (e.g., `{% pageurl %}`), also load `wagtailcore_tags`:

   ```django
   {% load static wagtailcore_tags menubuilder_tags %}
   ```

2. **Create a Template File Matching the Slug**

   The slug defined in the Menubuilder menu must match the name of the template file used to render it. For example:

   - If the menu slug is `top-navbar`, the `render_menu` tag will look for `wagtail_menubuilder/templates/menubuilder/top-navbar.html`. You can override this by creating your own `templates/wagtail_menubuilder/top-navbar.html` in your project.

3. **Include Styles and Scripts**

   Ensure the required CSS and JavaScript files (provided with the package) are loaded in your base template (`base.html`):

   ```html
   {% load static %}
   ...
   <link rel="stylesheet" type="text/css" href="{% static 'menubuilder/css/top-navbar.css' %}">
   ...
   <script type="text/javascript" src="{% static 'menubuilder/js/top-navbar.js' %}"></script>
   ...
   ```
   *(Note: The paths assume your static files setup correctly collects files from `wagtail_menubuilder/static/`)*

4. **(Optional) Customize `top-navbar.html`**

   - If you need to modify the HTML structure, copy the template file from `wagtail_menubuilder/templates/menubuilder/top-navbar.html` into your project's template directory at `templates/wagtail_menubuilder/top-navbar.html` and edit it there. Django will automatically pick up your overridden version.

---

## Advanced Usage

### Custom Menu Templates

You can create custom templates for your menus by using the following context variables:

- `menu`: The menu object (instance of `Menu`).
- `visible_items`: List of top-level menu item objects (instances of `MenuItem`) that should be displayed (e.g., linked page is live, and if it was a parent, it has visible children). Each item object has a `visible_children` attribute containing a list of its processed child items.
- `request`: The current request object.

#### Example Custom Template

```html
<nav class="custom-menu">
    <ul>
        {% for item in visible_items %} {# Use visible_items passed from the tag #}
            <li class="{% if item.active %}active{% endif %}"> {# Note: 'active' class logic needs implementation based on request.path #}
                <a href="{{ item.get_url }}">{{ item.title }}</a> {# Use get_url method #}
                {% if item.visible_children %} {# Check for processed visible children #}
                    <ul class="submenu">
                        {% for child in item.visible_children %}
                            <li><a href="{{ child.get_url }}">{{ child.title }}</a></li> {# Use get_url method #}
                        {% endfor %}
                    </ul>
                {% endif %}
            </li>
        {% endfor %}
    </ul>
</nav>
```

Then use your custom template:

```django
{% render_menu "main-menu" template="wagtail_menubuilder/custom-menu.html" %}
```

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support This Project 💖

If you find this project helpful, consider supporting my work:

- [💸 Donate via PayPal](https://paypal.me/techbill?country.x=US&locale.x=en_US)
- [☕ Buy Me a Coffee](https://www.buymeacoffee.com/techbill)

Your support helps me maintain and improve this project. Thank you! 🙏