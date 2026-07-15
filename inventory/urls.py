from django.urls import path

from . import report_views
from . import views


urlpatterns = [
    path(
        "",
        views.dashboard,
        name="dashboard",
    ),

    # Productos
    path(
        "products/",
        views.products,
        name="products",
    ),
    path(
        "products/create/",
        views.product_create,
        name="product_create",
    ),
    path(
        "products/update/<int:id>/",
        views.product_update,
        name="product_update",
    ),
    path(
        "products/delete/<int:id>/",
        views.product_delete,
        name="product_delete",
    ),

    # Categorías
    path(
        "categories/",
        views.categories,
        name="categories",
    ),
    path(
        "categories/create/",
        views.category_create,
        name="category_create",
    ),
    path(
        "categories/update/<int:id>/",
        views.category_update,
        name="category_update",
    ),
    path(
        "categories/delete/<int:id>/",
        views.category_delete,
        name="category_delete",
    ),

    # Proveedores
    path(
        "providers/",
        views.providers,
        name="providers",
    ),
    path(
        "providers/create/",
        views.provider_create,
        name="provider_create",
    ),
    path(
        "providers/update/<int:id>/",
        views.provider_update,
        name="provider_update",
    ),
    path(
        "providers/delete/<int:id>/",
        views.provider_delete,
        name="provider_delete",
    ),

    # Entradas
    path(
        "entries/",
        views.entries,
        name="entries",
    ),
    path(
        "entries/create/",
        views.entry_create,
        name="entry_create",
    ),
    path(
        "entries/update/<int:id>/",
        views.entry_update,
        name="entry_update",
    ),
    path(
        "entries/delete/<int:id>/",
        views.entry_delete,
        name="entry_delete",
    ),

    # Salidas
    path(
        "exits/",
        views.exits,
        name="exits",
    ),
    path(
        "exits/create/",
        views.exit_create,
        name="exit_create",
    ),
    path(
        "exits/update/<int:id>/",
        views.exit_update,
        name="exit_update",
    ),
    path(
        "exits/delete/<int:id>/",
        views.exit_delete,
        name="exit_delete",
    ),

    # Reportes
    path(
        "reports/",
        report_views.reports,
        name="reports",
    ),
]