from django.contrib.auth.decorators import login_required
from django.db.models import (
    Count,
    DecimalField,
    ExpressionWrapper,
    F,
    Sum,
)
from django.shortcuts import render

from .models import Categoria, Entrada, Producto, Proveedor, Salida


@login_required
def reports(request):
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

    valor_expression = ExpressionWrapper(
        F("stock") * F("precio"),
        output_field=DecimalField(
            max_digits=15,
            decimal_places=2,
        ),
    )

    valor_inventario = productos_usuario.aggregate(
        total=Sum(valor_expression)
    )["total"] or 0

    total_entradas = entradas_usuario.aggregate(
        total=Sum("cantidad")
    )["total"] or 0

    total_salidas = salidas_usuario.aggregate(
        total=Sum("cantidad")
    )["total"] or 0

    productos_stock_bajo = productos_usuario.filter(
        estado=True,
        stock__lte=5,
    ).count()

    productos = productos_usuario.select_related(
        "categoria"
    ).annotate(
        valor_total=ExpressionWrapper(
            F("stock") * F("precio"),
            output_field=DecimalField(
                max_digits=15,
                decimal_places=2,
            ),
        )
    ).order_by("nombre")

    entradas = entradas_usuario.select_related(
        "producto",
        "proveedor",
    ).order_by("-fecha")

    salidas = salidas_usuario.select_related(
        "producto"
    ).order_by("-fecha")

    categorias = categorias_usuario.annotate(
        total_productos=Count(
            "productos"
        ),
        stock_categoria=Sum(
            "productos__stock"
        ),
    ).order_by("nombre")

    context = {
        "total_productos": total_productos,
        "total_categorias": total_categorias,
        "total_proveedores": total_proveedores,
        "stock_total": stock_total,
        "valor_inventario": valor_inventario,
        "total_entradas": total_entradas,
        "total_salidas": total_salidas,
        "productos_stock_bajo": productos_stock_bajo,
        "productos": productos,
        "entradas": entradas,
        "salidas": salidas,
        "categorias": categorias,
    }

    return render(
        request,
        "inventory/reports.html",
        context,
    )