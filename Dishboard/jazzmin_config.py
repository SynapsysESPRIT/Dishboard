# jazzmin_config.py

# Jazzmin settings for customization
JAZZMIN_SETTINGS = {
    "site_title": "Dishboard",  # Title of the browser tab
    "site_header": "Dishboard",  # Title on the admin header
    "site_brand": "Dishboard",   # Title in the sidebar and topbar
    "welcome_sign": "Welcome to Dishboard Admin",  # Welcome text
    "copyright": "Copyright © 2024",  # Copyright in the footer
    "show_sidebar": True,  # Show the sidebar
    "navigation_expanded": False,  # Start with collapsed sidebar
    "order_with_respect_to": ["auth", "auth.user", "auth.Group"],  # Order in the admin panel
    "topmenu_links": [
        {"name": "Dashboard", "url": "admin:index", "permissions": ["auth.view_user"]},
    ],  # Top menu link
    "usermenu_links": [
        {"name": "See Profile", "url": "/admin/User/user/2/change/", "icon": "fas fa-user"},
        {"model": "auth.user"},
        {"name": "Change password", "url": "/admin/password_change/", "icon": "fas fa-key"},
    ],  # User menu
    # Add custom CSS class for background image
    "site_logo": "logo"
}

# UI Tweaks
JAZZMIN_UI_TWEAKS = {
    "theme": "minty",  # Set theme to darkly
    "accent": "accent-primary",  # Accent color
    "navbar": "navbar-dark navbar-primary",  # Dark navbar
    "sidebar": "sidebar-dark-primary",  # Dark sidebar
}