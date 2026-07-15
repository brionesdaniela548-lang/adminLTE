from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    CategoriaForm,
    EntradaForm,
    ProductoForm,
    ProveedorForm,
    SalidaForm,
)
from .models import Categoria, Entrada, Producto, Proveedor, Salida


@login_required
def dashboard(request):
    productos_usuario = Producto.objects.filter(
        propietario=request.user
    )

    categorias_usuario = Categoria.objects.filter(
        propietario=request.user
    )

    proveedores_usuario = Proveedor.objects.filter(
        propietario=request.user
    )

    entradas_usuario = Entrada.objects.filter(
        propietario=request.user
    )

    salidas_usuario = Salida.objects.filter(
        propietario=request.user
    )

    total_productos = productos_usuario.count()
    total_categorias = categorias_usuario.count()
    total_proveedores = proveedores_usuario.count()

    stock_total = productos_usuario.aggregate(
        total=Sum("stock")
    )["total"] or 0

    categorias = categorias_usuario.annotate(
        stock_categoria=Sum("productos__stock")
    ).order_by("nombre")

    nombres_categorias = [
        categoria.nombre
        for categoria in categorias
    ]

    cantidades_productos = [
        categoria.stock_categoria or 0
        for categoria in categorias
    ]

    ultimas_entradas = entradas_usuario.select_related(
        "producto",
        "proveedor",
    ).order_by("-fecha")[:5]

    ultimas_salidas = salidas_usuario.select_related(
        "producto"
    ).order_by("-fecha")[:5]

    productos_stock_bajo = productos_usuario.filter(
        estado=True,
        stock__lte=5,
    ).order_by("stock")[:5]

    context = {
        "total_productos": total_productos,
        "total_categorias": total_categorias,
        "total_proveedores": total_proveedores,
        "total_usuarios": 1,
        "stock_total": stock_total,
        "nombres_categorias": nombres_categorias,
        "cantidades_productos": cantidades_productos,
        "ultimas_entradas": ultimas_entradas,
        "ultimas_salidas": ultimas_salidas,
        "productos_stock_bajo": productos_stock_bajo,
    }

    return render(
        request,
        "inventory/dashboard.html",
        context,
    )


# =========================================================
# PRODUCTOS
# =========================================================

@login_required
def products(request):
    products = Producto.objects.filter(
        propietario=request.user
    ).select_related(
        "categoria"
    )

    return render(
        request,
        "inventory/products.html",
        {
            "products": products,
        },
    )


@login_required
def product_create(request):
    if request.method == "POST":
        form = ProductoForm(
            request.POST,
            user=request.user,
        )

        if form.is_valid():
            product = form.save(
                commit=False
            )

            product.propietario = request.user
            product.save()

            messages.success(
                request,
                "Producto registrado correctamente.",
            )

            return redirect("products")

    else:
        form = ProductoForm(
            user=request.user
        )

    return render(
        request,
        "inventory/product_form.html",
        {
            "form": form,
            "title": "Agregar Producto",
        },
    )


@login_required
def product_update(request, id):
    product = get_object_or_404(
        Producto,
        id=id,
        propietario=request.user,
    )

    if request.method == "POST":
        form = ProductoForm(
            request.POST,
            instance=product,
            user=request.user,
        )

        if form.is_valid():
            product = form.save(
                commit=False
            )

            product.propietario = request.user
            product.save()

            messages.success(
                request,
                "Producto actualizado correctamente.",
            )

            return redirect("products")

    else:
        form = ProductoForm(
            instance=product,
            user=request.user,
        )

    return render(
        request,
        "inventory/product_form.html",
        {
            "form": form,
            "title": "Editar Producto",
            "product": product,
        },
    )


@login_required
def product_delete(request, id):
    product = get_object_or_404(
        Producto,
        id=id,
        propietario=request.user,
    )

    if request.method == "POST":
        try:
            product.delete()

            messages.success(
                request,
                "Producto eliminado correctamente.",
            )

        except Exception:
            messages.error(
                request,
                (
                    "No se puede eliminar el producto porque tiene "
                    "movimientos registrados."
                ),
            )

    return redirect("products")


# =========================================================
# CATEGORÍAS
# =========================================================

@login_required
def categories(request):
    categories = Categoria.objects.filter(
        propietario=request.user
    )

    return render(
        request,
        "inventory/categories.html",
        {
            "categories": categories,
        },
    )


@login_required
def category_create(request):
    if request.method == "POST":
        form = CategoriaForm(
            request.POST,
            user=request.user,
        )

        if form.is_valid():
            category = form.save(
                commit=False
            )

            category.propietario = request.user
            category.save()

            messages.success(
                request,
                "Categoría registrada correctamente.",
            )

            return redirect("categories")

    else:
        form = CategoriaForm(
            user=request.user
        )

    return render(
        request,
        "inventory/category_form.html",
        {
            "form": form,
            "title": "Agregar Categoría",
        },
    )


@login_required
def category_update(request, id):
    category = get_object_or_404(
        Categoria,
        id=id,
        propietario=request.user,
    )

    if request.method == "POST":
        form = CategoriaForm(
            request.POST,
            instance=category,
            user=request.user,
        )

        if form.is_valid():
            category = form.save(
                commit=False
            )

            category.propietario = request.user
            category.save()

            messages.success(
                request,
                "Categoría actualizada correctamente.",
            )

            return redirect("categories")

    else:
        form = CategoriaForm(
            instance=category,
            user=request.user,
        )

    return render(
        request,
        "inventory/category_form.html",
        {
            "form": form,
            "title": "Editar Categoría",
            "category": category,
        },
    )


@login_required
def category_delete(request, id):
    category = get_object_or_404(
        Categoria,
        id=id,
        propietario=request.user,
    )

    if request.method == "POST":
        try:
            category.delete()

            messages.success(
                request,
                "Categoría eliminada correctamente.",
            )

        except Exception:
            messages.error(
                request,
                (
                    "No se puede eliminar la categoría porque tiene "
                    "productos relacionados."
                ),
            )

    return redirect("categories")


# =========================================================
# PROVEEDORES
# =========================================================

@login_required
def providers(request):
    providers = Proveedor.objects.filter(
        propietario=request.user
    )

    return render(
        request,
        "inventory/providers.html",
        {
            "providers": providers,
        },
    )


@login_required
def provider_create(request):
    if request.method == "POST":
        form = ProveedorForm(
            request.POST,
            user=request.user,
        )

        if form.is_valid():
            provider = form.save(
                commit=False
            )

            provider.propietario = request.user
            provider.save()

            messages.success(
                request,
                "Proveedor registrado correctamente.",
            )

            return redirect("providers")

    else:
        form = ProveedorForm(
            user=request.user
        )

    return render(
        request,
        "inventory/provider_form.html",
        {
            "form": form,
            "title": "Agregar Proveedor",
        },
    )


@login_required
def provider_update(request, id):
    provider = get_object_or_404(
        Proveedor,
        id=id,
        propietario=request.user,
    )

    if request.method == "POST":
        form = ProveedorForm(
            request.POST,
            instance=provider,
            user=request.user,
        )

        if form.is_valid():
            provider = form.save(
                commit=False
            )

            provider.propietario = request.user
            provider.save()

            messages.success(
                request,
                "Proveedor actualizado correctamente.",
            )

            return redirect("providers")

    else:
        form = ProveedorForm(
            instance=provider,
            user=request.user,
        )

    return render(
        request,
        "inventory/provider_form.html",
        {
            "form": form,
            "title": "Editar Proveedor",
            "provider": provider,
        },
    )


@login_required
def provider_delete(request, id):
    provider = get_object_or_404(
        Proveedor,
        id=id,
        propietario=request.user,
    )

    if request.method == "POST":
        try:
            provider.delete()

            messages.success(
                request,
                "Proveedor eliminado correctamente.",
            )

        except Exception:
            messages.error(
                request,
                (
                    "No se puede eliminar el proveedor porque tiene "
                    "entradas registradas."
                ),
            )

    return redirect("providers")


# =========================================================
# ENTRADAS
# =========================================================

@login_required
def entries(request):
    entries = Entrada.objects.filter(
        propietario=request.user
    ).select_related(
        "producto",
        "proveedor",
    )

    return render(
        request,
        "inventory/entries.html",
        {
            "entries": entries,
        },
    )


@login_required
def entry_create(request):
    if request.method == "POST":
        form = EntradaForm(
            request.POST,
            user=request.user,
        )

        if form.is_valid():
            try:
                entry = form.save(
                    commit=False
                )

                entry.propietario = request.user
                entry.save()

                messages.success(
                    request,
                    (
                        "Entrada registrada correctamente. "
                        "El stock fue actualizado."
                    ),
                )

                return redirect("entries")

            except ValidationError as error:
                form.add_error(
                    None,
                    error,
                )

    else:
        form = EntradaForm(
            user=request.user
        )

    return render(
        request,
        "inventory/entry_form.html",
        {
            "form": form,
            "title": "Registrar Entrada",
        },
    )


@login_required
def entry_update(request, id):
    entry = get_object_or_404(
        Entrada,
        id=id,
        propietario=request.user,
    )

    if request.method == "POST":
        form = EntradaForm(
            request.POST,
            instance=entry,
            user=request.user,
        )

        if form.is_valid():
            try:
                entry = form.save(
                    commit=False
                )

                entry.propietario = request.user
                entry.save()

                messages.success(
                    request,
                    (
                        "Entrada actualizada correctamente. "
                        "El stock fue recalculado."
                    ),
                )

                return redirect("entries")

            except ValidationError as error:
                form.add_error(
                    None,
                    error,
                )

    else:
        form = EntradaForm(
            instance=entry,
            user=request.user,
        )

    return render(
        request,
        "inventory/entry_form.html",
        {
            "form": form,
            "title": "Editar Entrada",
            "entry": entry,
        },
    )


@login_required
def entry_delete(request, id):
    entry = get_object_or_404(
        Entrada,
        id=id,
        propietario=request.user,
    )

    if request.method == "POST":
        try:
            entry.delete()

            messages.success(
                request,
                (
                    "Entrada eliminada correctamente. "
                    "El stock fue actualizado."
                ),
            )

        except ValidationError as error:
            messages.error(
                request,
                str(error),
            )

    return redirect("entries")


# =========================================================
# SALIDAS
# =========================================================

@login_required
def exits(request):
    exits = Salida.objects.filter(
        propietario=request.user
    ).select_related(
        "producto"
    )

    return render(
        request,
        "inventory/exits.html",
        {
            "exits": exits,
        },
    )


@login_required
def exit_create(request):
    if request.method == "POST":
        form = SalidaForm(
            request.POST,
            user=request.user,
        )

        if form.is_valid():
            try:
                exit_record = form.save(
                    commit=False
                )

                exit_record.propietario = request.user
                exit_record.save()

                messages.success(
                    request,
                    (
                        "Salida registrada correctamente. "
                        "El stock del producto fue actualizado."
                    ),
                )

                return redirect("exits")

            except ValidationError as error:
                if hasattr(
                    error,
                    "message_dict",
                ):
                    for field, errors in error.message_dict.items():
                        for message in errors:
                            form.add_error(
                                field,
                                message,
                            )
                else:
                    form.add_error(
                        None,
                        error,
                    )

    else:
        form = SalidaForm(
            user=request.user
        )

    return render(
        request,
        "inventory/exit_form.html",
        {
            "form": form,
            "title": "Registrar Salida",
        },
    )


@login_required
def exit_update(request, id):
    exit_record = get_object_or_404(
        Salida,
        id=id,
        propietario=request.user,
    )

    if request.method == "POST":
        form = SalidaForm(
            request.POST,
            instance=exit_record,
            user=request.user,
        )

        if form.is_valid():
            try:
                exit_record = form.save(
                    commit=False
                )

                exit_record.propietario = request.user
                exit_record.save()

                messages.success(
                    request,
                    (
                        "Salida actualizada correctamente. "
                        "El stock fue recalculado."
                    ),
                )

                return redirect("exits")

            except ValidationError as error:
                if hasattr(
                    error,
                    "message_dict",
                ):
                    for field, errors in error.message_dict.items():
                        for message in errors:
                            form.add_error(
                                field,
                                message,
                            )
                else:
                    form.add_error(
                        None,
                        error,
                    )

    else:
        form = SalidaForm(
            instance=exit_record,
            user=request.user,
        )

    return render(
        request,
        "inventory/exit_form.html",
        {
            "form": form,
            "title": "Editar Salida",
            "exit_record": exit_record,
        },
    )


@login_required
def exit_delete(request, id):
    exit_record = get_object_or_404(
        Salida,
        id=id,
        propietario=request.user,
    )

    if request.method == "POST":
        exit_record.delete()

        messages.success(
            request,
            (
                "Salida eliminada correctamente. "
                "Las unidades fueron devueltas al stock."
            ),
        )

    return redirect("exits")