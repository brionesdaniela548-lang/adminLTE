from django.core.exceptions import ValidationError
from django.db import models, transaction



class Categoria(models.Model):
    nombre = models.CharField(
        max_length=100,
        unique=True
    )

    descripcion = models.TextField(
        blank=True,
        null=True
    )

    estado = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    codigo = models.CharField(
        max_length=20,
        unique=True
    )

    nombre = models.CharField(
        max_length=100
    )

    descripcion = models.TextField(
        blank=True,
        null=True
    )

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="productos"
    )

    stock = models.PositiveIntegerField(
        default=0
    )

    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    estado = models.BooleanField(
        default=True
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Proveedor(models.Model):
    nombre = models.CharField(
        max_length=100
    )

    empresa = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    telefono = models.CharField(
        max_length=20
    )

    correo = models.EmailField(
        blank=True,
        null=True
    )

    direccion = models.TextField(
        blank=True,
        null=True
    )

    estado = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

    def __str__(self):
        if self.empresa:
            return f"{self.nombre} - {self.empresa}"

        return self.nombre


class Entrada(models.Model):
    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name="entradas"
    )

    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.PROTECT,
        related_name="entradas"
    )

    cantidad = models.PositiveIntegerField()

    fecha = models.DateTimeField(
        auto_now_add=True
    )

    observacion = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        ordering = ["-fecha"]
        verbose_name = "Entrada"
        verbose_name_plural = "Entradas"

    def __str__(self):
        return f"Entrada de {self.cantidad} - {self.producto.nombre}"

    def clean(self):
        super().clean()

        if self.cantidad is None or self.cantidad <= 0:
            raise ValidationError(
                {
                    "cantidad": "La cantidad debe ser mayor que cero."
                }
            )

    @transaction.atomic
    def save(self, *args, **kwargs):
        self.full_clean()

        if self.pk:
            entrada_anterior = Entrada.objects.select_for_update().get(
                pk=self.pk
            )

            producto_anterior = Producto.objects.select_for_update().get(
                pk=entrada_anterior.producto_id
            )

            producto_anterior.stock += entrada_anterior.cantidad
            producto_anterior.save(update_fields=["stock"])

        producto_nuevo = Producto.objects.select_for_update().get(
            pk=self.producto_id
        )

        super().save(*args, **kwargs)

        producto_nuevo.stock += self.cantidad
        producto_nuevo.save(update_fields=["stock"])

    @transaction.atomic
    def delete(self, *args, **kwargs):
        producto = Producto.objects.select_for_update().get(
            pk=self.producto_id
        )

        if producto.stock < self.cantidad:
            raise ValidationError(
                "No se puede eliminar la entrada porque el stock actual "
                "es menor que la cantidad registrada."
            )

        producto.stock -= self.cantidad
        producto.save(update_fields=["stock"])

        return super().delete(*args, **kwargs)


class Salida(models.Model):
    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name="salidas"
    )

    cantidad = models.PositiveIntegerField()

    destinatario = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    fecha = models.DateTimeField(
        auto_now_add=True
    )

    observacion = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        ordering = ["-fecha"]
        verbose_name = "Salida"
        verbose_name_plural = "Salidas"

    def __str__(self):
        return f"Salida de {self.cantidad} - {self.producto.nombre}"

    def clean(self):
        super().clean()

        if self.cantidad is None or self.cantidad <= 0:
            raise ValidationError(
                {
                    "cantidad": "La cantidad debe ser mayor que cero."
                }
            )

    @transaction.atomic
    def save(self, *args, **kwargs):
        self.full_clean()

        if self.pk:
            salida_anterior = Salida.objects.select_for_update().get(
                pk=self.pk
            )

            producto_anterior = Producto.objects.select_for_update().get(
                pk=salida_anterior.producto_id
            )

            producto_anterior.stock += salida_anterior.cantidad
            producto_anterior.save(update_fields=["stock"])

        producto_nuevo = Producto.objects.select_for_update().get(
            pk=self.producto_id
        )

        if producto_nuevo.stock < self.cantidad:
            raise ValidationError(
                {
                    "cantidad": (
                        f"Stock insuficiente. Actualmente hay "
                        f"{producto_nuevo.stock} unidades disponibles."
                    )
                }
            )

        super().save(*args, **kwargs)

        producto_nuevo.stock -= self.cantidad
        producto_nuevo.save(update_fields=["stock"])

    @transaction.atomic
    def delete(self, *args, **kwargs):
        producto = Producto.objects.select_for_update().get(
            pk=self.producto_id
        )

        producto.stock += self.cantidad
        producto.save(update_fields=["stock"])

        return super().delete(*args, **kwargs)