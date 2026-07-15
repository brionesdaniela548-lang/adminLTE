from django.contrib import admin

from .models import Categoria, Entrada, Producto, Proveedor, Salida


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "estado",
    )

    search_fields = (
        "nombre",
    )

    list_filter = (
        "estado",
    )


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        "codigo",
        "nombre",
        "categoria",
        "stock",
        "precio",
        "estado",
    )

    search_fields = (
        "codigo",
        "nombre",
    )

    list_filter = (
        "categoria",
        "estado",
    )


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "empresa",
        "telefono",
        "correo",
        "estado",
    )

    search_fields = (
        "nombre",
        "empresa",
    )

    list_filter = (
        "estado",
    )


@admin.register(Entrada)
class EntradaAdmin(admin.ModelAdmin):
    list_display = (
        "producto",
        "proveedor",
        "cantidad",
        "fecha",
    )

    search_fields = (
        "producto__nombre",
        "producto__codigo",
        "proveedor__nombre",
    )

    list_filter = (
        "fecha",
        "proveedor",
    )


@admin.register(Salida)
class SalidaAdmin(admin.ModelAdmin):
    list_display = (
        "producto",
        "cantidad",
        "destinatario",
        "fecha",
    )

    search_fields = (
        "producto__nombre",
        "producto__codigo",
        "destinatario",
    )

    list_filter = (
        "fecha",
    )