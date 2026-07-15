from django import forms

from .models import Categoria, Entrada, Producto, Proveedor, Salida


class ProductoForm(forms.ModelForm):

    class Meta:
        model = Producto

        fields = [
            "codigo",
            "nombre",
            "descripcion",
            "categoria",
            "stock",
            "precio",
            "estado",
        ]

        widgets = {
            "codigo": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Código del producto",
                }
            ),
            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombre del producto",
                }
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Descripción del producto",
                }
            ),
            "categoria": forms.Select(
                attrs={
                    "class": "form-control select2",
                    "style": "width: 100%;",
                }
            ),
            "stock": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "placeholder": "Stock inicial",
                }
            ),
            "precio": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": 0,
                    "placeholder": "Precio del producto",
                }
            ),
            "estado": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user

        if user:
            self.fields["categoria"].queryset = Categoria.objects.filter(
                propietario=user,
                estado=True,
            ).order_by("nombre")
        else:
            self.fields["categoria"].queryset = Categoria.objects.none()

    def clean_codigo(self):
        codigo = self.cleaned_data.get("codigo", "").strip()

        if not codigo:
            return codigo

        queryset = Producto.objects.filter(
            propietario=self.user,
            codigo__iexact=codigo,
        )

        if self.instance and self.instance.pk:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():
            raise forms.ValidationError(
                "Ya tienes un producto registrado con este código."
            )

        return codigo

    def clean_precio(self):
        precio = self.cleaned_data.get("precio")

        if precio is not None and precio < 0:
            raise forms.ValidationError(
                "El precio no puede ser negativo."
            )

        return precio


class CategoriaForm(forms.ModelForm):

    class Meta:
        model = Categoria

        fields = [
            "nombre",
            "descripcion",
            "estado",
        ]

        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombre de la categoría",
                }
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Descripción de la categoría",
                }
            ),
            "estado": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre", "").strip()

        if not nombre:
            return nombre

        queryset = Categoria.objects.filter(
            propietario=self.user,
            nombre__iexact=nombre,
        )

        if self.instance and self.instance.pk:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():
            raise forms.ValidationError(
                "Ya tienes una categoría registrada con este nombre."
            )

        return nombre


class ProveedorForm(forms.ModelForm):

    class Meta:
        model = Proveedor

        fields = [
            "nombre",
            "empresa",
            "telefono",
            "correo",
            "direccion",
            "estado",
        ]

        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombre del proveedor",
                }
            ),
            "empresa": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombre de la empresa",
                }
            ),
            "telefono": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Número de teléfono",
                }
            ),
            "correo": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Correo electrónico",
                }
            ),
            "direccion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Dirección del proveedor",
                }
            ),
            "estado": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user


class EntradaForm(forms.ModelForm):

    class Meta:
        model = Entrada

        fields = [
            "producto",
            "proveedor",
            "cantidad",
            "observacion",
        ]

        widgets = {
            "producto": forms.Select(
                attrs={
                    "class": "form-control select2",
                    "style": "width: 100%;",
                }
            ),
            "proveedor": forms.Select(
                attrs={
                    "class": "form-control select2",
                    "style": "width: 100%;",
                }
            ),
            "cantidad": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                    "placeholder": "Cantidad que ingresa",
                }
            ),
            "observacion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Observación opcional",
                }
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user

        if user:
            self.fields["producto"].queryset = Producto.objects.filter(
                propietario=user,
                estado=True,
            ).order_by("nombre")

            self.fields["proveedor"].queryset = Proveedor.objects.filter(
                propietario=user,
                estado=True,
            ).order_by("nombre")
        else:
            self.fields["producto"].queryset = Producto.objects.none()
            self.fields["proveedor"].queryset = Proveedor.objects.none()

        self.fields["producto"].empty_label = "Seleccione un producto"
        self.fields["proveedor"].empty_label = "Seleccione un proveedor"

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get("cantidad")

        if cantidad is None or cantidad <= 0:
            raise forms.ValidationError(
                "La cantidad debe ser mayor que cero."
            )

        return cantidad


class SalidaForm(forms.ModelForm):

    class Meta:
        model = Salida

        fields = [
            "producto",
            "cantidad",
            "destinatario",
            "observacion",
        ]

        widgets = {
            "producto": forms.Select(
                attrs={
                    "class": "form-control select2",
                    "style": "width: 100%;",
                }
            ),
            "cantidad": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                    "placeholder": "Cantidad que sale",
                }
            ),
            "destinatario": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Persona, departamento o cliente",
                }
            ),
            "observacion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Observación opcional",
                }
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user

        if user:
            self.fields["producto"].queryset = Producto.objects.filter(
                propietario=user,
                estado=True,
            ).order_by("nombre")
        else:
            self.fields["producto"].queryset = Producto.objects.none()

        self.fields["producto"].empty_label = "Seleccione un producto"

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get("cantidad")
        producto = self.cleaned_data.get("producto")

        if cantidad is None or cantidad <= 0:
            raise forms.ValidationError(
                "La cantidad debe ser mayor que cero."
            )

        if producto:
            stock_disponible = producto.stock

            if (
                self.instance
                and self.instance.pk
                and self.instance.producto_id == producto.id
            ):
                stock_disponible += self.instance.cantidad

            if cantidad > stock_disponible:
                raise forms.ValidationError(
                    (
                        f"Stock insuficiente. Hay "
                        f"{stock_disponible} unidades disponibles."
                    )
                )

        return cantidad