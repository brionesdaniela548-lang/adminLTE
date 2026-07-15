from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
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
    total_productos = Producto.objects.count()
    total_categorias = Categoria.objects.count()
    total_proveedores = Proveedor.objects.count()
    total_usuarios = User.objects.count()

    stock_total = Producto.objects.aggregate(
        total=Sum("stock")
    )["total"] or 0

    categorias = Categoria.objects.annotate(
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

    ultimas_entradas = Entrada.objects.select_related(
        "producto",
        "proveedor",
    ).order_by("-fecha")[:5]

    ultimas_salidas = Salida.objects.select_related(
        "producto"
    ).order_by("-fecha")[:5]

    productos_stock_bajo = Producto.objects.filter(
        estado=True,
        stock__lte=5,
    ).order_by("stock")[:5]

    context = {
        "total_productos": total_productos,
        "total_categorias": total_categorias,
        "total_proveedores": total_proveedores,
        "total_usuarios": total_usuarios,
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


@login_required
def products(request):
    products = Producto.objects.select_related(
        "categoria"
    ).all()

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
        form = ProductoForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Producto registrado correctamente.",
            )

            return redirect("products")

    else:
        form = ProductoForm()

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
    )

    if request.method == "POST":
        form = ProductoForm(
            request.POST,
            instance=product,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Producto actualizado correctamente.",
            )

            return redirect("products")

    else:
        form = ProductoForm(
            instance=product,
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


@login_required
def categories(request):
    categories = Categoria.objects.all()

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
        form = CategoriaForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Categoría registrada correctamente.",
            )

            return redirect("categories")

    else:
        form = CategoriaForm()

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
    )

    if request.method == "POST":
        form = CategoriaForm(
            request.POST,
            instance=category,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Categoría actualizada correctamente.",
            )

            return redirect("categories")

    else:
        form = CategoriaForm(
            instance=category,
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


@login_required
def providers(request):
    providers = Proveedor.objects.all()

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
        form = ProveedorForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Proveedor registrado correctamente.",
            )

            return redirect("providers")

    else:
        form = ProveedorForm()

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
    )

    if request.method == "POST":
        form = ProveedorForm(
            request.POST,
            instance=provider,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Proveedor actualizado correctamente.",
            )

            return redirect("providers")

    else:
        form = ProveedorForm(
            instance=provider,
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


@login_required
def entries(request):
    entries = Entrada.objects.select_related(
        "producto",
        "proveedor",
    ).all()

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
        form = EntradaForm(request.POST)

        if form.is_valid():
            try:
                form.save()

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
        form = EntradaForm()

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
    )

    if request.method == "POST":
        form = EntradaForm(
            request.POST,
            instance=entry,
        )

        if form.is_valid():
            try:
                form.save()

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


@login_required
def exits(request):
    exits = Salida.objects.select_related(
        "producto"
    ).all()

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
        form = SalidaForm(request.POST)

        if form.is_valid():
            try:
                form.save()

                messages.success(
                    request,
                    (
                        "Salida registrada correctamente. "
                        "El stock del producto fue actualizado."
                    ),
                )

                return redirect("exits")

            except ValidationError as error:
                if hasattr(error, "message_dict"):
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
        form = SalidaForm()

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
    )

    if request.method == "POST":
        form = SalidaForm(
            request.POST,
            instance=exit_record,
        )

        if form.is_valid():
            try:
                form.save()

                messages.success(
                    request,
                    (
                        "Salida actualizada correctamente. "
                        "El stock fue recalculado."
                    ),
                )

                return redirect("exits")

            except ValidationError as error:
                if hasattr(error, "message_dict"):
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

@login_required
def profile_view(request):
    profile = Profile.objects.filter(
        user=request.user
    ).first()

    return render(
        request,
        "accounts/profile.html",
        {
            "profile": profile,
        },
    )