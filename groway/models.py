import math
import pytz
import locale
import qrcode
import numpy as np
from datetime import date
from datetime import datetime
from matplotlib import pyplot as plt
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django import forms
from datetime import timedelta
from . import choices
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

# Modelos de la APP

class Organizacion(models.Model):
	nombre_legal = models.CharField(max_length=50)
	identificacion = models.CharField(max_length=7, choices=choices.DOCUMENTOS_IDENTIDAD)
	numero_identificacion = models.CharField(max_length=50)
	numero_id_adicional = models.CharField(max_length=4, null=True, blank=True)
	activad_economica = models.CharField(max_length=100)
	codigo_actividad_economica = models.CharField(max_length=5)
	descripcion = models.TextField(null=True, blank=True)
	logo_organizacion = models.ImageField(max_length=100, upload_to='user_img/', null=True, blank=True)
	nombre_visible_cia = models.CharField(max_length=20)
	moneda_base = models.CharField(max_length=3, choices=choices.MONEDAS)
	direccion = models.CharField(max_length=50)
	ciudad = models.CharField(max_length=50)
	departamento = models.CharField(max_length=50)
	pais = models.CharField(max_length=2, choices=choices.PAISES)
	cod_postal = models.CharField(max_length=50, null=True, blank=True)
	persona_contacto = models.CharField(max_length=50, null=True, blank=True)
	telefono = models.PositiveIntegerField()
	telefono_dos = models.PositiveIntegerField(null=True, blank=True)
	email = models.EmailField(max_length=254, null=True, blank=True)
	website = models.CharField(max_length=254, null=True, blank=True)
	numero_cuenta = models.IntegerField(null=True, blank=True)
	tipo_cuenta = models.CharField(max_length=3, null=True, blank=True, choices=choices.TIPO_CUENTA)
	entidad_financiera = models.CharField(max_length=50, null=True, blank=True)
	regimen_tributario = models.CharField(max_length=1, choices=choices.REGIMEN_TRIBUTARIO)
	responsable_iva = models.CharField(max_length=2, choices=choices.RESPONSABLE_IVA)
	gran_contribuyente = models.BooleanField()
	declarante_impuesto_renta = models.BooleanField()
	compras_practicar_reterenta = models.BooleanField()
	compras_practicar_reteiva_proveedores_regimen_comun = models.BooleanField()
	compras_practicar_reteiva_proveedores_regimen_simple = models.BooleanField()
	compras_practicar_reteica = models.BooleanField()
	tarifa_practicar_reteica = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	ventas_liquidar_reterenta = models.BooleanField()
	ventas_liquidar_autoretencion_renta = models.BooleanField()
	tarifa_autoreterenta = models.CharField(max_length=2, choices=choices.TARIFA_AUTORETERENTA, blank=True)
	ventas_liquidar_autorreterenta_clientes_regimen_simple = models.BooleanField()
	ventas_liquidar_reteica = models.BooleanField()
	tarifa_liquidar_reteica = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	administrador = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
	activa = models.BooleanField()

	def clean(self):
		img_logo = self.logo_organizacion
		if img_logo:
			w, h = get_image_dimensions(img_logo)
			if w != 300:
				raise ValidationError("El ancho para 'Logo Organización' debe ser de %spx. El archivo seleccionado tiene %spx" %(300, w))
			if h != 60:
				raise ValidationError("El alto para 'Logo Organización' debe ser de %spx. El archivo seleccionado tiene %spx" %(60, h))
			filesize = img_logo.size
			if filesize > 350*1024:
				raise ValidationError("El tamaño máximo para 'Logo Organización' es de %sKB" %(350))

	def __str__(self):
		self.save()
		return self.nombre_legal


class Contacto(models.Model):
	naturaleza = models.CharField(max_length=1, choices=choices.NATURALEZA)
	identificacion = models.CharField(max_length=7, choices=choices.DOCUMENTOS_IDENTIDAD)
	numero_identificacion = models.CharField(max_length=50)
	numero_id_adicional = models.CharField(max_length=4, null=True, blank=True)
	nombre_legal = models.CharField(max_length=50)
	activad_economica = models.CharField(max_length=100, null=True, blank=True)
	codigo_actividad_economica = models.CharField(max_length=5, null=True, blank=True)
	relacion_activa = models.CharField(max_length=2, null=True, blank=True, choices=choices.RELACIONES)
	consumidor_final = models.BooleanField()
	regimen_tributario = models.CharField(max_length=1, choices=choices.REGIMEN_TRIBUTARIO)
	responsable_iva = models.CharField(max_length=2, choices=choices.RESPONSABLE_IVA)
	gran_contribuyente = models.BooleanField()
	ventas_liquidar_reteiva_responsable_iva_regimen_comun = models.BooleanField()
	ventas_liquidar_reteiva_responsable_iva_regimen_simple = models.BooleanField()
	ventas_liquidar_reterenta = models.BooleanField()
	ventas_liquidar_reteica = models.BooleanField()
	compras_declarante_impuesto_renta = models.BooleanField()
	compras_autoretenedor_impuesto_renta = models.BooleanField()
	compras_exento_de_reterenta = models.BooleanField()
	direccion = models.CharField(max_length=50)
	ciudad = models.CharField(max_length=50)
	departamento = models.CharField(max_length=50)
	pais = models.CharField(max_length=2, choices=choices.PAISES)
	cod_postal = models.CharField(max_length=50, null=True, blank=True)
	persona_contacto = models.CharField(max_length=50, null=True, blank=True)
	persona_contacto_adicional = models.CharField(max_length=50, null=True, blank=True)
	telefono = models.PositiveIntegerField()
	telefono_dos = models.PositiveIntegerField(null=True, blank=True)
	email = models.EmailField(max_length=254, null=True, blank=True)
	numero_cuenta = models.IntegerField(null=True, blank=True)
	tipo_cuenta = models.CharField(max_length=3, null=True, blank=True, choices=choices.TIPO_CUENTA)
	entidad_financiera = models.CharField(max_length=50, null=True, blank=True)
	terminos_de_pago = models.CharField(max_length=300, null=True, blank=True)
	medio_de_pago = models.CharField(max_length=2, choices=choices.MEDIOS_DE_PAGO, null=True, blank=True)
	org_creadora = models.ForeignKey(Organizacion, on_delete=models.CASCADE, limit_choices_to={'activa':True}, null=True, blank=True)

		
	def __str__(self):
		self.save()
		return self.nombre_legal


class Categoria(models.Model):
	destino_item = models.CharField(max_length=2, choices=choices.DESTINO_ITEM)
	pre_fijo = models.CharField(max_length=3)
	numero = models.IntegerField(null=True, blank=True, default=1)
	nombre = models.CharField(max_length=50)
	descripcion = models.TextField(null=True, blank=True)
	org_creadora = models.ForeignKey(Organizacion, on_delete=models.CASCADE, limit_choices_to={'activa':True}, null=True, blank=True)

	def __str__(self):
		self.save()
		return self.nombre


class Item(models.Model):
	imagen = models.ImageField(max_length=100, upload_to='user_img/', null=True, blank=True)
	categoria = models.CharField(max_length=300, null=True, blank=True)
	codigo = models.CharField(max_length=100, null=True, blank=True)
	tipo_item = models.CharField(max_length=2, choices=choices.TIPO_ITEM)
	descripcion = models.CharField(max_length=200)
	descripcion_detalle = models.TextField(null=True, blank=True)
	codigo_barras = models.CharField(max_length=50, null=True, blank=True)
	unidad_medida = models.CharField(max_length=4, choices=choices.UNIDADES_MEDIDA)
	precio_venta = models.DecimalField(max_digits=11, decimal_places=2)
	iva_ventas = models.CharField(max_length=2, choices=choices.TARIFA_IVA)
	impuesto_consumo_ventas = models.CharField(max_length=2, choices=choices.TARIFA_ICO)
	tarifa_reterenta = models.CharField(max_length=2, choices=choices.TARIFA_RETERENTA)
	cantidad = models.PositiveIntegerField(null=True, blank=True)
	org_creadora = models.ForeignKey(Organizacion, on_delete=models.CASCADE, limit_choices_to={'activa':True}, null=True, blank=True)

	def auto_codigo(self):
		item_creados = Item.objects.filter(categoria=self.categoria, id__lt=self.id).count()
		codigo = Categoria.objects.get(nombre=self.categoria, destino_item="IV")
		if item_creados == 0:
			self.codigo = "%s%s"%(codigo.pre_fijo, codigo.numero)
			self.save()
		elif item_creados > 0:
			nuevo_numero = codigo.numero + item_creados
			self.codigo = "%s%s"%(codigo.pre_fijo, nuevo_numero)
			self.save()

	def clean(self):
		img_item = self.imagen
		if img_item:
			w, h = get_image_dimensions(img_item)
			if w != 300:
				raise ValidationError("El ancho para 'Imagen del Item' debe ser de %spx. El archivo seleccionado tiene %spx" %(300, w))
			if h != 200:
				raise ValidationError("El alto para 'Imagen del Item' debe ser de %spx. El archivo seleccionado tiene %spx" %(200, h))
			filesize = img_item.size
			if filesize > 350*1024:
				raise ValidationError("El tamaño máximo para 'Imagen del Item' es de %sKB" %(350))

	def __str__(self):
		self.save()
		return "%s | %s"%(self.codigo, self.descripcion)

class Insumo(models.Model):
	imagen = models.ImageField(max_length=100, upload_to='user_img/', null=True, blank=True)
	categoria = models.CharField(max_length=300, null=True, blank=True)
	codigo = models.CharField(max_length=100, null=True, blank=True)
	tipo_item = models.CharField(max_length=2, choices=choices.TIPO_ITEM)
	descripcion = models.CharField(max_length=200)
	descripcion_detalle = models.TextField(null=True, blank=True)
	codigo_barras = models.CharField(max_length=50, null=True, blank=True)
	unidad_medida = models.CharField(max_length=4, choices=choices.UNIDADES_MEDIDA)
	precio_compra = models.DecimalField(max_digits=11, decimal_places=2)
	iva_compras = models.CharField(max_length=2, choices=choices.TARIFA_IVA)
	impuesto_consumo_compras = models.CharField(max_length=2, choices=choices.TARIFA_ICO)
	tarifa_reterenta = models.CharField(max_length=2, choices=choices.TARIFA_RETERENTA)
	cantidad = models.PositiveIntegerField(null=True, blank=True)
	org_creadora = models.ForeignKey(Organizacion, on_delete=models.CASCADE, limit_choices_to={'activa':True}, null=True, blank=True)

	def auto_codigo(self):
		insumos_creados = Insumo.objects.filter(categoria=self.categoria, id__lt=self.id).count()
		codigo = Categoria.objects.get(nombre=self.categoria, destino_item="IM")
		if insumos_creados == 0:
			self.codigo = "%s%s"%(codigo.pre_fijo, codigo.numero)
			self.save()
		elif insumos_creados > 0:
			nuevo_numero = codigo.numero + insumos_creados
			self.codigo = "%s%s"%(codigo.pre_fijo, nuevo_numero)
			self.save()

	def clean(self):
		img_item = self.imagen
		if img_item:
			w, h = get_image_dimensions(img_item)
			if w != 300:
				raise ValidationError("El ancho para 'Imagen del Insumo' debe ser de %spx. El archivo seleccionado tiene %spx" %(300, w))
			if h != 200:
				raise ValidationError("El alto para 'Imagen del Insumo' debe ser de %spx. El archivo seleccionado tiene %spx" %(200, h))
			filesize = img_item.size
			if filesize > 350*1024:
				raise ValidationError("El tamaño máximo para 'Imagen del Insumo' es de %sKB" %(350))

	def __str__(self):
		self.save()
		return "%s | %s"%(self.codigo, self.descripcion)


class Termino_de_pago(models.Model):
	codigo = models.CharField(max_length=30, null=True, blank=True)
	descripcion = models.CharField(max_length=50)
	plazo_dias = models.IntegerField()
	org_creadora = models.ForeignKey(Organizacion, on_delete=models.CASCADE, limit_choices_to={'activa':True}, null=True, blank=True)

	def auto_codigo(self):
		if self.plazo_dias == 0:
			self.codigo = "CONT0"
		else:
			self.codigo = "CRED%s"%(self.plazo_dias)
		self.save()

	def __str__(self):
		self.save()
		return self.descripcion

class Consecutivo_documento(models.Model):
	tipo_de_documento = models.CharField(max_length=3, choices=choices.TIPO_DE_DOCUMENTO)
	pre_fijo = models.CharField(max_length=2, null=True, blank=True)
	numero = models.IntegerField(default=1, null=True, blank=True)
	aut_num_facturacion = models.BigIntegerField(null=True, blank=True)
	num_inicio = models.IntegerField(null=True, blank=True)
	num_final = models.IntegerField(null=True, blank=True)
	fecha_inicio = models.DateField(null=True, blank=True)
	fecha_fin = models.DateField(null=True, blank=True)
	fecha_inicio_format = models.CharField(max_length=100, null=True, blank=True)
	fecha_fin_format = models.CharField(max_length=100, null=True, blank=True)
	codigo = models.IntegerField(null=True, blank=True)
	org_creadora = models.ForeignKey(Organizacion, on_delete=models.CASCADE, limit_choices_to={'activa':True}, null=True, blank=True)
	generado = models.BooleanField(default=False)

	def auto_codigo(self):
		if self.tipo_de_documento == "FVE":
			self.codigo = 1
			self.save()
		elif self.tipo_de_documento == "FEX":
			self.codigo = 2
			self.save()
		elif self.tipo_de_documento == "FCG":
			self.codigo = 3
			self.save()
		else:
			self.codigo = 0
			self.save()

	def __str__(self):
		self.save()
		return '%s %s'%(self.pre_fijo, self.numero)

class Cotizacion(models.Model):
	consec_inter_prefijo = models.CharField(max_length=3, null=True, blank=True)
	consec_inter_numero = models.PositiveIntegerField(null=True, blank=True)
	consecutivo_interno = models.CharField(max_length=100, null=True, blank=True)
	referencia_orden_compra = models.CharField(max_length=100, null=True, blank=True)
	referencia_remision = models.CharField(max_length=100, null=True, blank=True)
	referencia_factura = models.CharField(max_length=100, null=True, blank=True)
	referencia_otro_documento = models.CharField(max_length=100, null=True, blank=True)
	fecha_emision = models.DateTimeField(null=True, blank=True)
	tipo_imp1 = models.CharField(max_length=2, choices=choices.TIPO_IMPUESTO, null=True, blank=True)
	tipo_imp2 = models.CharField(max_length=2, choices=choices.TIPO_IMPUESTO, null=True, blank=True)
	tipo_imp3 = models.CharField(max_length=2, choices=choices.TIPO_IMPUESTO, null=True, blank=True)
	terminos_de_pago = models.CharField(max_length=300, null=True, blank=True)
	medio_de_pago = models.CharField(max_length=2, choices=choices.MEDIOS_DE_PAGO, null=True, blank=True)
	moneda = models.CharField(max_length=3, choices=choices.MONEDAS, null=True, blank=True)
	vendedor = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
	org_creadora = models.ForeignKey(Organizacion, on_delete=models.CASCADE, limit_choices_to={'activa':True}, null=True, blank=True)
	id_organizacion = models.CharField(max_length=50, null=True, blank=True)
	numero_id_organizacion = models.CharField(max_length=50, null=True, blank=True)
	numero_id_org_adicional = models.CharField(max_length=4, null=True, blank=True)
	dir_organizacion = models.CharField(max_length=50, null=True, blank=True)
	ciudad_organizacion = models.CharField(max_length=50, null=True, blank=True)
	departamento_organizacion = models.CharField(max_length=50, null=True, blank=True)
	pais_organizacion = models.CharField(max_length=50, null=True, blank=True)
	telefono_organizacion = models.CharField(max_length=50, null=True, blank=True)
	cliente = models.CharField(max_length=300, null=True, blank=True)
	nombre_cliente = models.CharField(max_length=50, null=True, blank=True)
	id_cliente = models.CharField(max_length=50, null=True, blank=True)
	numero_id_cliente = models.CharField(max_length=50, null=True, blank=True)
	numero_id_cli_adicional = models.CharField(max_length=4, null=True, blank=True)
	dir_cliente = models.CharField(max_length=50, null=True, blank=True)
	ciudad_cliente = models.CharField(max_length=50, null=True, blank=True)
	departamento_cliente = models.CharField(max_length=50, null=True, blank=True)
	pais_cliente = models.CharField(max_length=50, null=True, blank=True)
	telefono_cliente = models.CharField(max_length=50, null=True, blank=True)
	item_1 = models.CharField(max_length=300, null=True, blank=True)
	item_2 = models.CharField(max_length=300, null=True, blank=True)
	item_3 = models.CharField(max_length=300, null=True, blank=True)
	item_4 = models.CharField(max_length=300, null=True, blank=True)
	item_5 = models.CharField(max_length=300, null=True, blank=True)
	cantidad_1 = models.IntegerField(blank=True, null=True)
	cantidad_2 = models.IntegerField(blank=True, null=True)
	cantidad_3 = models.IntegerField(blank=True, null=True)
	cantidad_4 = models.IntegerField(blank=True, null=True)
	cantidad_5 = models.IntegerField(blank=True, null=True)
	UM_1 = models.CharField(max_length=20, null=True, blank=True)
	UM_2 = models.CharField(max_length=20, null=True, blank=True)
	UM_3 = models.CharField(max_length=20, null=True, blank=True)
	UM_4 = models.CharField(max_length=20, null=True, blank=True)
	UM_5 = models.CharField(max_length=20, null=True, blank=True)
	valor_unitario_1 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_unitario_2 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_unitario_3 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_unitario_4 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_unitario_5 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	porcentaje_descuento_1 = models.IntegerField(blank=True, null=True)
	porcentaje_descuento_2 = models.IntegerField(blank=True, null=True)
	porcentaje_descuento_3 = models.IntegerField(blank=True, null=True)
	porcentaje_descuento_4 = models.IntegerField(blank=True, null=True)
	porcentaje_descuento_5 = models.IntegerField(blank=True, null=True)
	valor_descuento_1 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_descuento_2 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_descuento_3 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_descuento_4 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_descuento_5 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	iva_1 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	iva_2 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	iva_3 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	iva_4 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	iva_5 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	ico_1 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	ico_2 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	ico_3 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	ico_4 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	ico_5 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_total_1 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_total_2 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_total_3 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_total_4 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_total_5 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	iva_total = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	ico_total = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	reterenta = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	autoreterenta = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	reteiva = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	reteica = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	sub_total = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	total_impuestos = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	total_retenciones = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	total_documento = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	anticipo = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	saldo_pendiente = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	descripcion_1 = models.CharField(max_length=400,  null=True, blank=True)
	descripcion_2 = models.CharField(max_length=400,  null=True, blank=True)
	descripcion_3 = models.CharField(max_length=400,  null=True, blank=True)
	descripcion_4 = models.CharField(max_length=400,  null=True, blank=True)
	descripcion_5 = models.CharField(max_length=400,  null=True, blank=True)
	descripcion_detallada = models.TextField(null=True, blank=True)
	observacion = models.CharField(max_length=200,  null=True, blank=True)
	cifra_total_en_palabras = models.CharField(max_length=300,  null=True, blank=True)
	generado = models.BooleanField(default=False)

	def auto_consecutivo(self):
		consecutivo = Consecutivo_documento.objects.get(org_creadora=self.org_creadora, tipo_de_documento="CZN", generado=True)
		doc_creados = Cotizacion.objects.filter(org_creadora=self.org_creadora, generado=True).count()
		ultimo_doc = Cotizacion.objects.filter(org_creadora=self.org_creadora, generado=True).last()
		if doc_creados == 0:
			self.consec_inter_prefijo = consecutivo.pre_fijo
			self.consec_inter_numero = consecutivo.numero
			self.consecutivo_interno = '%s %s'%(self.consec_inter_prefijo, self.consec_inter_numero)
			self.save()
		elif doc_creados > 0:
			nuevo_num = ultimo_doc.consec_inter_numero + 1
			self.consec_inter_prefijo = consecutivo.pre_fijo
			self.consec_inter_numero = nuevo_num
			self.consecutivo_interno = '%s %s'%(self.consec_inter_prefijo, self.consec_inter_numero)
			self.save()

	def auto_info_organizacion(self):
		self.id_organizacion = self.org_creadora.identificacion
		self.numero_id_organizacion = self.org_creadora.numero_identificacion
		self.numero_id_org_adicional = self.org_creadora.numero_id_adicional
		self.dir_organizacion = self.org_creadora.direccion
		self.ciudad_organizacion = self.org_creadora.ciudad
		self.departamento_organizacion = self.org_creadora.departamento
		self.pais_organizacion = self.org_creadora.pais
		self.telefono_organizacion = self.org_creadora.telefono
		self.moneda = self.org_creadora.moneda_base
		self.save()

	def auto_info_cliente(self):
		cliente = Contacto.objects.get(nombre_legal=self.cliente, relacion_activa="CL", org_creadora=self.org_creadora)
		self.nombre_cliente = cliente.nombre_legal
		self.id_cliente = cliente.identificacion
		self.numero_id_cliente = cliente.numero_identificacion
		self.numero_id_cli_adicional = cliente.numero_id_adicional
		self.dir_cliente = cliente.direccion
		self.ciudad_cliente = cliente.ciudad
		self.departamento_cliente = cliente.departamento
		self.pais_cliente = cliente.pais
		self.telefono_cliente = cliente.telefono
		if cliente.terminos_de_pago:
			self.terminos_de_pago = cliente.terminos_de_pago
		if cliente.medio_de_pago:
			self.medio_de_pago = cliente.medio_de_pago
		for llave, valor in choices.MEDIOS_DE_PAGO:
			if self.medio_de_pago == llave:
				self.medio_de_pago = valor
		self.save()

	def info_item(self):
		item_selecionados = [self.item_1, self.item_2, self.item_3, self.item_4, self.item_5]
		items_codes = []
		for item in item_selecionados:
			if item:
				item_doc = Item.objects.get(codigo=item, org_creadora=self.org_creadora)
				item_code = item_doc.codigo
				items_codes.append(item_code)
			else:
				items_codes.append(None)
		self.item_1_code = items_codes[0]
		self.item_2_code = items_codes[1]
		self.item_3_code = items_codes[2]
		self.item_4_code = items_codes[3]
		self.item_5_code = items_codes[4]
		self.save()

		descripciones = []
		for item in item_selecionados:
			if item:
				item_doc = Item.objects.get(codigo=item, org_creadora=self.org_creadora)
				descripcion = item_doc.descripcion
				descripciones.append(descripcion)
			else:
				descripciones.append(None)
		self.descripcion_1 = descripciones[0]
		self.descripcion_2 = descripciones[1]
		self.descripcion_3 = descripciones[2]
		self.descripcion_4 = descripciones[3]
		self.descripcion_5 = descripciones[4]
		self.save()

		if self.descripcion_detallada == 'No Registrado' or self.descripcion_detallada == '':
			descripciones_detalle = []
			for item in item_selecionados:
				if item:
					item_doc = Item.objects.get(codigo=item, org_creadora=self.org_creadora)
					if item_doc.descripcion_detalle:
						descripcion = '- %s\n' %(item_doc.descripcion_detalle)
						descripciones_detalle.append(descripcion)
			descrip_detail = ''
			for descripcion in descripciones_detalle:
				descrip_detail = descrip_detail + descripcion
			self.descripcion_detallada = descrip_detail

		unidadesmedida = []
		for item in item_selecionados:
			if item:
				item_doc = Item.objects.get(codigo=item, org_creadora=self.org_creadora)
				UM = item_doc.unidad_medida
				unidadesmedida.append(UM)
			else:
				unidadesmedida.append(None)
		self.UM_1 = unidadesmedida[0]
		self.UM_2 = unidadesmedida[1]
		self.UM_3 = unidadesmedida[2]
		self.UM_4 = unidadesmedida[3]
		self.UM_5 = unidadesmedida[4]
		self.save()

		valoresunitarios = []
		for item in item_selecionados:
			if item:
				item_doc = Item.objects.get(codigo=item, org_creadora=self.org_creadora)
				valor_unitario = item_doc.precio_venta
				valoresunitarios.append(valor_unitario)
			else:
				valoresunitarios.append(0)
		self.valor_unitario_1 = valoresunitarios[0]
		self.valor_unitario_2 = valoresunitarios[1]
		self.valor_unitario_3 = valoresunitarios[2]
		self.valor_unitario_4 = valoresunitarios[3]
		self.valor_unitario_5 = valoresunitarios[4]
		self.save()

	def calculo_item(self):
		item_selecionados = [self.item_1, self.item_2, self.item_3, self.item_4, self.item_5]
		valoresunitarios = []
		for item in item_selecionados:
			if item:
				item_doc = Item.objects.get(codigo=item, org_creadora=self.org_creadora)
				valor_unitario = item_doc.precio_venta
				valoresunitarios.append(valor_unitario)
			else:
				valoresunitarios.append(0)
		self.valor_unitario_1 = valoresunitarios[0]
		self.valor_unitario_2 = valoresunitarios[1]
		self.valor_unitario_3 = valoresunitarios[2]
		self.valor_unitario_4 = valoresunitarios[3]
		self.valor_unitario_5 = valoresunitarios[4]

		porcentajesdescuento = [self.porcentaje_descuento_1, self.porcentaje_descuento_2, self.porcentaje_descuento_3, self.porcentaje_descuento_4, self.porcentaje_descuento_5]
		cantidades = [self.cantidad_1, self.cantidad_2, self.cantidad_3, self.cantidad_4, self.cantidad_5]
		cantidades_nuevo = []
		for valor in cantidades:
			if valor == None:
				cantidades_nuevo.append(0)
			else:
				cantidades_nuevo.append(valor)
		self.cantidad_1 = cantidades_nuevo[0]
		self.cantidad_2 = cantidades_nuevo[1]
		self.cantidad_3 = cantidades_nuevo[2]
		self.cantidad_4 = cantidades_nuevo[3]
		self.cantidad_5 = cantidades_nuevo[4]

		porcentajesdescuento_nuevo = []
		for valor in porcentajesdescuento:
			if valor == None:
				porcentajesdescuento_nuevo.append(0)
			else:
				porcentajesdescuento_nuevo.append(valor)
		self.porcentaje_descuento_1 = porcentajesdescuento_nuevo[0]
		self.porcentaje_descuento_2 = porcentajesdescuento_nuevo[1]
		self.porcentaje_descuento_3 = porcentajesdescuento_nuevo[2]
		self.porcentaje_descuento_4 = porcentajesdescuento_nuevo[3]
		self.porcentaje_descuento_5 = porcentajesdescuento_nuevo[4]

		valoresdescuento = []
		indice = 0
		for valor in valoresunitarios:
			if cantidades_nuevo[indice] or porcentajesdescuento_nuevo[indice]:
				valordescuento = valor * cantidades_nuevo[indice] * porcentajesdescuento_nuevo[indice]/100
				valoresdescuento.append(valordescuento)
			else:
				valoresdescuento.append(0)
			indice += 1
		self.valor_descuento_1 = valoresdescuento[0]
		self.valor_descuento_2 = valoresdescuento[1]
		self.valor_descuento_3 = valoresdescuento[2]
		self.valor_descuento_4 = valoresdescuento[3]
		self.valor_descuento_5 = valoresdescuento[4]

		valorestotales = []
		indice = 0
		for valor in valoresunitarios:
			if cantidades[indice]:
				valortotal = valor * cantidades_nuevo[indice] - valoresdescuento[indice]
				valorestotales.append(valortotal)
			else:
				valorestotales.append(0)
			indice += 1
		self.valor_total_1 = valorestotales[0]
		self.valor_total_2 = valorestotales[1]
		self.valor_total_3 = valorestotales[2]
		self.valor_total_4 = valorestotales[3]
		self.valor_total_5 = valorestotales[4]
		self.sub_total = self.valor_total_1 + self.valor_total_2 + self.valor_total_3 + self.valor_total_4 + self.valor_total_5

		if self.org_creadora.responsable_iva == 'SI':
			numeros = ['1', '2', '3', '4']
			tarifas_de_iva = [19, 5, 0, 0]
			iva_item = []
			indice = 0
			for item in item_selecionados:
				if item:
					item_doc = Item.objects.get(codigo=item, org_creadora=self.org_creadora)
					if item_doc.iva_ventas:
						tariva = 0
						for numero in numeros:
							if item_doc.iva_ventas == numero:
								iva = float(valorestotales[indice]) * (tarifas_de_iva[tariva]/100)
								iva_item.append(int(iva))
							tariva += 1
				else:
					iva_item.append(0)
				indice += 1
			self.iva_1 = iva_item[0]
			self.iva_2 = iva_item[1]
			self.iva_3 = iva_item[2]
			self.iva_4 = iva_item[3]
			self.iva_5 = iva_item[4]
			self.iva_total = self.iva_1 + self.iva_2 + self.iva_3 + self.iva_4 + self.iva_5
			self.save()
		else:
			self.iva_total = 0
			self.save()

		cliente = Contacto.objects.get(nombre_legal=self.cliente, relacion_activa="CL", org_creadora=self.org_creadora)
		if cliente.consumidor_final == True:
			numeros = ['1', '2', '3', '4']
			tarifas_de_ico = [16, 8, 4, 0]
			ico_item = []
			indice = 0
			for item in item_selecionados:
				if item:
					item_doc = Item.objects.get(codigo=item, org_creadora=self.org_creadora)
					if item_doc.impuesto_consumo_ventas:
						tarico = 0
						for numero in numeros:
							if item_doc.impuesto_consumo_ventas == numero:
								ico = float(valorestotales[indice]) * (tarifas_de_ico[tarico]/100)
								ico_item.append(int(ico))
							tarico += 1
				else:
					ico_item.append(0)
				indice += 1
			self.ico_1 = ico_item[0]
			self.ico_2 = ico_item[1]
			self.ico_3 = ico_item[2]
			self.ico_4 = ico_item[3]
			self.ico_5 = ico_item[4]
			self.ico_total = self.ico_1 + self.ico_2 + self.ico_3 + self.ico_4 + self.ico_5
			self.save()
		else:
			self.ico_total = 0
			self.save()

		if self.org_creadora.declarante_impuesto_renta == True or self.org_creadora.declarante_impuesto_renta == False:
			if self.org_creadora.ventas_liquidar_reterenta == True and self.org_creadora.ventas_liquidar_autoretencion_renta == False and cliente.ventas_liquidar_reterenta == True:
				numeros = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16" ,"17", "18", "19", "20",
				"21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40",
				"41", "42", "43", "44", "45", "46", "47", "48"]
				bases = [0,961000,0,961000,0,0,0,0,0,0,0,0,0,0,142000,0,142000,0,142000,961000,0,142000,0,142000,0,142000,0,142000,0,0,
				961000,0,0,0,3276000,0,0,0,0,0,0,961000,0,0,5697000,0,0,0]
				tarifas_de_reterenta = [0,2.5,2.5,3.5,3.5,1,0.1,10,11,3.5,6,10,10,11,1,1,2,2,3.5,3.5,3.5,4,4,6,6,1,1,2,2,4,3.5,3.5,7,4,1.5,1.5,0.75,
				15,20,5,15,2,2,0.5,0.5,10,11,2.5]
				indice = 0
				reterentas = 0
				for numero in numeros:
					totalval = 0
					bases_retefuenterenta = 0
					for item in item_selecionados:
						if item:
							item_doc = Item.objects.get(codigo=item, org_creadora=self.org_creadora)
							if item_doc.tarifa_reterenta:
								if item_doc.tarifa_reterenta == numero:
									bases_retefuenterenta = bases_retefuenterenta + valorestotales[totalval]
						totalval = totalval + 1
					if bases_retefuenterenta > bases[indice]:
						reterentas = reterentas + (float(bases_retefuenterenta) * (tarifas_de_reterenta[indice]/100))
					indice = indice + 1
				self.reterenta = int(reterentas)
				self.autoreterenta = 0
				self.save()
			elif self.org_creadora.ventas_liquidar_autoretencion_renta == True:
				numeros = ['1', '2', '3']
				tarifas_autoreterenta = [0.4, 0.8, 1.6]
				indice = 0
				if self.org_creadora.tarifa_autoreterenta == None:
					self.autoreterenta = 0
					self.save()
				for numero in numeros:
					if self.org_creadora.tarifa_autoreterenta == numero:
						self.autoreterenta = self.sub_total * (tarifas_autoreterenta[indice]/100)
						self.reterenta = 0
						self.save()
					indice = indice + 1
			elif self.org_creadora.ventas_liquidar_reterenta == True and self.org_creadora.ventas_liquidar_autorreterenta_clientes_regimen_simple == True :
				if self.org_creadora.regimen_tributario == 2 and cliente.regimen_tributario == 0:
					numeros = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16" ,"17", "18", "19", "20",
				"21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40",
				"41", "42", "43", "44", "45", "46", "47", "48"]
				bases = [0,961000,0,961000,0,0,0,0,0,0,0,0,0,0,142000,0,142000,0,142000,961000,0,142000,0,142000,0,142000,0,142000,0,0,
				961000,0,0,0,3276000,0,0,0,0,0,0,961000,0,0,5697000,0,0,0]
				tarifas_de_reterenta = [0,2.5,2.5,3.5,3.5,1,0.1,10,11,3.5,6,10,10,11,1,1,2,2,3.5,3.5,3.5,4,4,6,6,1,1,2,2,4,3.5,3.5,7,4,1.5,1.5,0.75,
				15,20,5,15,2,2,0.5,0.5,10,11,2.5]
				indice = 0
				reterentas = 0
				for numero in numeros:
					totalval = 0
					bases_retefuenterenta = 0
					for item in item_selecionados:
						if item:
							item_doc = Item.objects.get(codigo=item, org_creadora=self.org_creadora)
							if item_doc.tarifa_reterenta:
								if item_doc.tarifa_reterenta == numero:
									bases_retefuenterenta = bases_retefuenterenta + valorestotales[totalval]
						totalval = totalval + 1
					if bases_retefuenterenta > bases[indice]:
						reterentas = reterentas + (float(bases_retefuenterenta) * (tarifas_de_reterenta[indice]/100))
					indice = indice + 1
					self.autoreterenta = int(reterentas)
					self.reterenta = 0
					self.save()
			else:
				self.reterenta = 0
				self.autoreterenta = 0
				self.save()
		else:
			self.reterenta = 0
			self.autoreterenta = 0
			self.save()
	
		if self.org_creadora.ventas_liquidar_reteica == True and cliente.ventas_liquidar_reteica == True:
			if self.org_creadora.ciudad == cliente.ciudad:
				if self.org_creadora.gran_contribuyente == True:
					self.reteica = 0
					self.save()
				elif self.org_creadora.regimen_tributario == '2' or self.org_creadora.regimen_tributario == '0':
					if cliente.regimen_tributario == '0':
						self.reteica = 0
						self.save()
					else:
						if self.org_creadora.tarifa_liquidar_reteica == None:
							self.reteica = 0
							self.save()
						else:
							self.reteica = self.sub_total * (self.org_creadora.tarifa_liquidar_reteica/1000)
							self.save()
				else:
					self.reteica = 0
					self.save()
			else:
				self.reteica = 0
				self.save()
		else:
			self.reteica = 0
			self.save()

		if cliente.gran_contribuyente == True:
			self.reteiva = int(self.iva_total * 0.15)
			self.save()
		elif cliente.ventas_liquidar_reteiva_responsable_iva_regimen_comun and cliente.gran_contribuyente == False and cliente.responsable_iva == 'SI':
			if self.org_creadora.responsable_iva == 'SI' and self.org_creadora.gran_contribuyente == False and self.org_creadora.regimen_tributario == '2':
				self.reteiva = int(self.iva_total * 0.15)
				self.save()
			else:
				self.reteiva = 0
				self.save()
		elif cliente.ventas_liquidar_reteiva_responsable_iva_regimen_simple and cliente.regimen_tributario == '2' and cliente.responsable_iva == 'SI':
			if self.org_creadora.responsable_iva == 'SI' and self.org_creadora.regimen_tributario == '0':
				self.reteiva = int(self.iva_total * 0.15)
				self.save()
			else:
				self.reteiva = 0
				self.save()
		else:
			self.reteiva = 0
			self.save()

		if self.anticipo == None:
			self.anticipo = 0
			self.save()

	def calculo_total_cotizacion(self):
		self.total_impuestos = self.iva_total + self.ico_total
		self.total_retenciones = self.reterenta + self.autoreterenta + self.reteiva + self.reteica
		self.total_documento = self.sub_total + self.total_impuestos - self.total_retenciones
		self.saldo_pendiente = self.total_documento - self.anticipo
		self.save()

	def tipo_impuestodoc(self):
		if self.iva_total:
			self.tipo_imp1 = "01"
			self.save()
		if self.ico_total:
			self.tipo_imp2 = "02"
			self.save()
		if self.reteica:
			self.tipo_imp3 = "03"
			self.save()

	def generar_remision(self):
		nueva_remision = Remision(referencia_cotizacion=self.consecutivo_interno,referencia_factura=self.referencia_factura,referencia_orden_compra=self.referencia_orden_compra,
			referencia_otro_documento=self.referencia_otro_documento,vendedor=self.vendedor,org_creadora=self.org_creadora,cliente=self.cliente,
			item_1=self.item_1,item_2=self.item_2,item_3=self.item_3,item_4=self.item_4,item_5=self.item_5,UM_1=self.UM_1,UM_2=self.UM_2,UM_3=self.UM_3,
			UM_4=self.UM_4,UM_5=self.UM_5,cantidad_1=self.cantidad_1,cantidad_2=self.cantidad_2,cantidad_3=self.cantidad_3,cantidad_4=self.cantidad_4,cantidad_5=self.cantidad_5,
			descripcion_1=self.descripcion_1,descripcion_2=self.descripcion_2,descripcion_3=self.descripcion_3,descripcion_4=self.descripcion_4,descripcion_5=self.descripcion_5,
			descripcion_detallada=self.descripcion_detallada,observacion=self.observacion)
		return nueva_remision

	def generar_factura_venta(self):
		nueva_factura = Factura_de_venta(referencia_cotizacion=self.consecutivo_interno,referencia_remision=self.referencia_remision,
			referencia_orden_compra=self.referencia_orden_compra,referencia_otro_documento=self.referencia_otro_documento,vendedor=self.vendedor,org_creadora=self.org_creadora,
			terminos_de_pago=self.terminos_de_pago, medio_de_pago=self.medio_de_pago, moneda=self.moneda, tipo_imp1=self.tipo_imp1,tipo_imp2=self.tipo_imp2,tipo_imp3=self.tipo_imp3,
			cliente=self.cliente, item_1=self.item_1, item_2=self.item_2, item_3=self.item_3, item_4=self.item_4, item_5=self.item_5,  cantidad_1=self.cantidad_1,
			cantidad_2=self.cantidad_2, cantidad_3=self.cantidad_3, cantidad_4=self.cantidad_4, cantidad_5=self.cantidad_5, porcentaje_descuento_1=self.porcentaje_descuento_1,
			porcentaje_descuento_2=self.porcentaje_descuento_2, porcentaje_descuento_3=self.porcentaje_descuento_3, porcentaje_descuento_4=self.porcentaje_descuento_4, porcentaje_descuento_5=self.porcentaje_descuento_5,
			anticipo=self.anticipo, descripcion_detallada=self.descripcion_detallada, observacion=self.observacion)
		return nueva_factura

	def duplicar_documento(self):
		nueva_cotizacion = Cotizacion(vendedor=self.vendedor,org_creadora=self.org_creadora,
			terminos_de_pago=self.terminos_de_pago, medio_de_pago=self.medio_de_pago, moneda=self.moneda, tipo_imp1=self.tipo_imp1,tipo_imp2=self.tipo_imp2,tipo_imp3=self.tipo_imp3,
			cliente=self.cliente, item_1=self.item_1, item_2=self.item_2, item_3=self.item_3, item_4=self.item_4, item_5=self.item_5,  cantidad_1=self.cantidad_1,
			cantidad_2=self.cantidad_2, cantidad_3=self.cantidad_3, cantidad_4=self.cantidad_4, cantidad_5=self.cantidad_5, porcentaje_descuento_1=self.porcentaje_descuento_1,
			porcentaje_descuento_2=self.porcentaje_descuento_2, porcentaje_descuento_3=self.porcentaje_descuento_3, porcentaje_descuento_4=self.porcentaje_descuento_4, porcentaje_descuento_5=self.porcentaje_descuento_5,
			anticipo=self.anticipo, descripcion_detallada=self.descripcion_detallada, observacion=self.observacion)
		return nueva_cotizacion

	def __str__(self):
		self.save()
		return "%s %s %s"%(self.consecutivo_interno, self.cliente, self.fecha_emision)



class Remision(models.Model):
	consec_inter_prefijo = models.CharField(max_length=3, null=True, blank=True)
	consec_inter_numero = models.PositiveIntegerField(null=True, blank=True)
	consecutivo_interno = models.CharField(max_length=100, null=True, blank=True)
	fecha_emision = models.DateTimeField(null=True, blank=True)
	referencia_cotizacion = models.CharField(max_length=100, null=True, blank=True)
	referencia_factura = models.CharField(max_length=100, null=True, blank=True)
	referencia_orden_compra = models.CharField(max_length=100, null=True, blank=True)
	referencia_otro_documento = models.CharField(max_length=100, null=True, blank=True)
	vendedor = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
	org_creadora = models.ForeignKey(Organizacion, on_delete=models.CASCADE, limit_choices_to={'activa':True}, null=True, blank=True)
	id_organizacion = models.CharField(max_length=50, null=True, blank=True)
	numero_id_organizacion = models.CharField(max_length=50, null=True, blank=True)
	numero_id_org_adicional = models.CharField(max_length=4, null=True, blank=True)
	dir_organizacion = models.CharField(max_length=50, null=True, blank=True)
	ciudad_organizacion = models.CharField(max_length=50, null=True, blank=True)
	departamento_organizacion = models.CharField(max_length=50, null=True, blank=True)
	pais_organizacion = models.CharField(max_length=50, null=True, blank=True)
	telefono_organizacion = models.CharField(max_length=50, null=True, blank=True)
	cliente = models.CharField(max_length=300, null=True, blank=True)
	nombre_cliente = models.CharField(max_length=50, null=True, blank=True)
	id_cliente = models.CharField(max_length=50, null=True, blank=True)
	numero_id_cliente = models.CharField(max_length=50, null=True, blank=True)
	numero_id_cli_adicional = models.CharField(max_length=4, null=True, blank=True)
	dir_cliente = models.CharField(max_length=50, null=True, blank=True)
	ciudad_cliente = models.CharField(max_length=50, null=True, blank=True)
	departamento_cliente = models.CharField(max_length=50, null=True, blank=True)
	pais_cliente = models.CharField(max_length=50, null=True, blank=True)
	telefono_cliente = models.CharField(max_length=50, null=True, blank=True)
	item_1 = models.CharField(max_length=300, null=True, blank=True)
	item_2 = models.CharField(max_length=300, null=True, blank=True)
	item_3 = models.CharField(max_length=300, null=True, blank=True)
	item_4 = models.CharField(max_length=300, null=True, blank=True)
	item_5 = models.CharField(max_length=300, null=True, blank=True)
	cantidad_1 = models.IntegerField(blank=True, null=True)
	cantidad_2 = models.IntegerField(blank=True, null=True)
	cantidad_3 = models.IntegerField(blank=True, null=True)
	cantidad_4 = models.IntegerField(blank=True, null=True)
	cantidad_5 = models.IntegerField(blank=True, null=True)
	UM_1 = models.CharField(max_length=20, null=True, blank=True)
	UM_2 = models.CharField(max_length=20, null=True, blank=True)
	UM_3 = models.CharField(max_length=20, null=True, blank=True)
	UM_4 = models.CharField(max_length=20, null=True, blank=True)
	UM_5 = models.CharField(max_length=20, null=True, blank=True)
	descripcion_1 = models.CharField(max_length=400,  null=True, blank=True)
	descripcion_2 = models.CharField(max_length=400,  null=True, blank=True)
	descripcion_3 = models.CharField(max_length=400,  null=True, blank=True)
	descripcion_4 = models.CharField(max_length=400,  null=True, blank=True)
	descripcion_5 = models.CharField(max_length=400,  null=True, blank=True)
	descripcion_detallada = models.TextField(max_length=300, null=True, blank=True)
	observacion = models.CharField(max_length=200,  null=True, blank=True)
	datos_transportador = models.TextField(max_length=300, null=True, blank=True)
	generado = models.BooleanField(default=False)

	
	def auto_consecutivo(self):
		consecutivo = Consecutivo_documento.objects.get(org_creadora=self.org_creadora, tipo_de_documento="RSN", generado=True)
		doc_creados = Remision.objects.filter(org_creadora=self.org_creadora, generado=True).count()
		ultimo_doc = Remision.objects.filter(org_creadora=self.org_creadora, generado=True).last()
		if doc_creados == 0:
			self.consec_inter_prefijo = consecutivo.pre_fijo
			self.consec_inter_numero = consecutivo.numero
			self.consecutivo_interno = '%s %s'%(self.consec_inter_prefijo, self.consec_inter_numero)
			self.save()
		elif doc_creados > 0:
			nuevo_num = ultimo_doc.consec_inter_numero + 1
			self.consec_inter_prefijo = consecutivo.pre_fijo
			self.consec_inter_numero = nuevo_num
			self.consecutivo_interno = '%s %s'%(self.consec_inter_prefijo, self.consec_inter_numero)
			self.save()

	def auto_info_organizacion(self):
		self.id_organizacion = self.org_creadora.identificacion
		self.numero_id_organizacion = self.org_creadora.numero_identificacion
		self.numero_id_org_adicional = self.org_creadora.numero_id_adicional
		self.dir_organizacion = self.org_creadora.direccion
		self.ciudad_organizacion = self.org_creadora.ciudad
		self.departamento_organizacion = self.org_creadora.departamento
		self.pais_organizacion = self.org_creadora.pais
		self.telefono_organizacion = self.org_creadora.telefono
		self.moneda = self.org_creadora.moneda_base
		self.save()

	def auto_info_cliente(self):
		cliente = Contacto.objects.get(nombre_legal=self.cliente, relacion_activa="CL", org_creadora=self.org_creadora)
		self.nombre_cliente = cliente.nombre_legal
		self.id_cliente = cliente.identificacion
		self.numero_id_cliente = cliente.numero_identificacion
		self.numero_id_cli_adicional = cliente.numero_id_adicional
		self.dir_cliente = cliente.direccion
		self.ciudad_cliente = cliente.ciudad
		self.departamento_cliente = cliente.departamento
		self.pais_cliente = cliente.pais
		self.telefono_cliente = cliente.telefono
		self.save()

	def __str__(self):
		self.save()
		return "%s %s %s"%(self.consecutivo_interno, self.cliente, self.fecha_emision)

class Factura_de_venta(models.Model):
	tipo_de_documento = models.CharField(max_length=100, null=True, blank=True)
	consecutivo_DIAN = models.CharField(max_length=100, null=True, blank=True)
	consec_inter_prefijo = models.CharField(max_length=3, null=True, blank=True)
	consec_inter_numero = models.PositiveIntegerField(null=True, blank=True)
	consecutivo_interno = models.CharField(max_length=100, null=True, blank=True)
	referencia_orden_compra = models.CharField(max_length=100, null=True, blank=True)
	referencia_cotizacion = models.CharField(max_length=100, null=True, blank=True)
	referencia_remision = models.CharField(max_length=100, null=True, blank=True)
	referencia_notacredito = models.CharField(max_length=100, null=True, blank=True)
	referencia_notadebito = models.CharField(max_length=100, null=True, blank=True)
	referencia_otro_documento = models.CharField(max_length=100, null=True, blank=True)
	fecha_para_consec = models.DateField(null=True, blank=True)
	fecha_emision = models.DateTimeField(null=True, blank=True)
	fecha_vencimiento = models.DateTimeField(null=True, blank=True)
	fecha_pago = models.DateTimeField(null=True, blank=True)
	tipo_imp1 = models.CharField(max_length=2, choices=choices.TIPO_IMPUESTO, null=True, blank=True)
	tipo_imp2 = models.CharField(max_length=2, choices=choices.TIPO_IMPUESTO, null=True, blank=True)
	tipo_imp3 = models.CharField(max_length=2, choices=choices.TIPO_IMPUESTO, null=True, blank=True)
	terminos_de_pago = models.CharField(max_length=300, null=True, blank=True)
	medio_de_pago = models.CharField(max_length=2, choices=choices.MEDIOS_DE_PAGO, null=True, blank=True)
	moneda = models.CharField(max_length=3, choices=choices.MONEDAS, null=True, blank=True)
	vendedor = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
	org_creadora = models.ForeignKey(Organizacion, on_delete=models.CASCADE, limit_choices_to={'activa':True}, null=True, blank=True)
	id_organizacion = models.CharField(max_length=50, null=True, blank=True)
	numero_id_organizacion = models.CharField(max_length=50, null=True, blank=True)
	numero_id_org_adicional = models.CharField(max_length=4, null=True, blank=True)
	dir_organizacion = models.CharField(max_length=50, null=True, blank=True)
	ciudad_organizacion = models.CharField(max_length=50, null=True, blank=True)
	departamento_organizacion = models.CharField(max_length=50, null=True, blank=True)
	pais_organizacion = models.CharField(max_length=50, null=True, blank=True)
	telefono_organizacion = models.CharField(max_length=50, null=True, blank=True)
	cliente = models.CharField(max_length=300, null=True, blank=True)
	nombre_cliente = models.CharField(max_length=50, null=True, blank=True)
	id_cliente = models.CharField(max_length=50, null=True, blank=True)
	numero_id_cliente = models.CharField(max_length=50, null=True, blank=True)
	numero_id_cli_adicional = models.CharField(max_length=4, null=True, blank=True)
	dir_cliente = models.CharField(max_length=50, null=True, blank=True)
	ciudad_cliente = models.CharField(max_length=50, null=True, blank=True)
	departamento_cliente = models.CharField(max_length=50, null=True, blank=True)
	pais_cliente = models.CharField(max_length=50, null=True, blank=True)
	telefono_cliente = models.CharField(max_length=50, null=True, blank=True)
	item_1 = models.CharField(max_length=300, null=True, blank=True)
	item_2 = models.CharField(max_length=300, null=True, blank=True)
	item_3 = models.CharField(max_length=300, null=True, blank=True)
	item_4 = models.CharField(max_length=300, null=True, blank=True)
	item_5 = models.CharField(max_length=300, null=True, blank=True)
	cantidad_1 = models.IntegerField(blank=True, null=True)
	cantidad_2 = models.IntegerField(blank=True, null=True)
	cantidad_3 = models.IntegerField(blank=True, null=True)
	cantidad_4 = models.IntegerField(blank=True, null=True)
	cantidad_5 = models.IntegerField(blank=True, null=True)
	UM_1 = models.CharField(max_length=20, null=True, blank=True)
	UM_2 = models.CharField(max_length=20, null=True, blank=True)
	UM_3 = models.CharField(max_length=20, null=True, blank=True)
	UM_4 = models.CharField(max_length=20, null=True, blank=True)
	UM_5 = models.CharField(max_length=20, null=True, blank=True)
	valor_unitario_1 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_unitario_2 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_unitario_3 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_unitario_4 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_unitario_5 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	porcentaje_descuento_1 = models.IntegerField(blank=True, null=True)
	porcentaje_descuento_2 = models.IntegerField(blank=True, null=True)
	porcentaje_descuento_3 = models.IntegerField(blank=True, null=True)
	porcentaje_descuento_4 = models.IntegerField(blank=True, null=True)
	porcentaje_descuento_5 = models.IntegerField(blank=True, null=True)
	valor_descuento_1 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_descuento_2 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_descuento_3 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_descuento_4 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_descuento_5 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	iva_1 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	iva_2 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	iva_3 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	iva_4 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	iva_5 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	ico_1 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	ico_2 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	ico_3 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	ico_4 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	ico_5 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_total_1 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_total_2 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_total_3 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_total_4 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_total_5 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	iva_total = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	ico_total = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	reterenta = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	autoreterenta = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	reteiva = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	reteica = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	sub_total = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	total_impuestos = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	total_retenciones = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	total_documento = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	anticipo = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	saldo_pendiente = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	descripcion_1 = models.CharField(max_length=400,  null=True, blank=True)
	descripcion_2 = models.CharField(max_length=400,  null=True, blank=True)
	descripcion_3 = models.CharField(max_length=400,  null=True, blank=True)
	descripcion_4 = models.CharField(max_length=400,  null=True, blank=True)
	descripcion_5 = models.CharField(max_length=400,  null=True, blank=True)
	descripcion_detallada = models.TextField(null=True, blank=True)
	observacion = models.CharField(max_length=200,  null=True, blank=True)
	cifra_total_en_palabras = models.CharField(max_length=300,  null=True, blank=True)
	cufe = models.CharField(max_length=300,  null=True, blank=True)
	imagen_qr = models.ImageField(max_length=100, null=True, blank=True)
	generado = models.BooleanField(default=False)
	anulada = models.BooleanField(default=False)
	pagada = models.BooleanField(default=False)


	def auto_consecutivo(self):
		consecutivo = Consecutivo_documento.objects.get(org_creadora=self.org_creadora, tipo_de_documento="FVE", generado=True)
		doc_creados = Factura_de_venta.objects.filter(org_creadora=self.org_creadora, generado=True).count()
		ultimo_doc = Factura_de_venta.objects.filter(org_creadora=self.org_creadora, generado=True).last()
		self.tipo_de_documento = consecutivo.codigo
		if doc_creados == 0:
			self.consec_inter_prefijo = consecutivo.pre_fijo
			self.consec_inter_numero = consecutivo.numero
			self.consecutivo_interno = '%s %s'%(self.consec_inter_prefijo, self.consec_inter_numero)
			self.save()
		elif doc_creados > 0:
			nuevo_num = ultimo_doc.consec_inter_numero + 1
			self.consec_inter_prefijo = consecutivo.pre_fijo
			self.consec_inter_numero = nuevo_num
			self.consecutivo_interno = '%s %s'%(self.consec_inter_prefijo, self.consec_inter_numero)
			self.save()
		if consecutivo.fecha_fin < self.fecha_para_consec or consecutivo.num_final < self.consec_inter_numero:
			consecutivo.generado = False
			consecutivo.save()
			self.consecutivo_interno = 'vencido'
			self.save()


	def auto_vencimiento(self):
		terminos = Termino_de_pago.objects.get(descripcion=self.terminos_de_pago, org_creadora=self.org_creadora)
		hoy = self.fecha_emision
		dias = terminos.plazo_dias
		if terminos == 'Contado':
			dias = 0
		plazo_dias = timedelta(days=dias)
		self.fecha_vencimiento = hoy + plazo_dias
		self.save()

	def auto_codigo_qr(self):
		qr = qrcode.QRCode(
			version = 1,
			error_correction = qrcode.constants.ERROR_CORRECT_H,
			box_size = 10,
			border = 4
		)

		info = self.cufe
		qr.add_data(info)
		qr.make(fit=True)
		img = qr.make_image()
		img.save("%s.png"%(self.consecutivo_interno))

	def auto_info_organizacion(self):
		self.id_organizacion = self.org_creadora.identificacion
		self.numero_id_organizacion = self.org_creadora.numero_identificacion
		self.numero_id_org_adicional = self.org_creadora.numero_id_adicional
		self.dir_organizacion = self.org_creadora.direccion
		self.ciudad_organizacion = self.org_creadora.ciudad
		self.departamento_organizacion = self.org_creadora.departamento
		self.pais_organizacion = self.org_creadora.pais
		self.telefono_organizacion = self.org_creadora.telefono
		self.moneda = self.org_creadora.moneda_base
		self.save()

	def auto_info_cliente(self):
		cliente = Contacto.objects.get(nombre_legal=self.cliente, relacion_activa="CL", org_creadora=self.org_creadora)
		self.nombre_cliente = cliente.nombre_legal
		self.id_cliente = cliente.identificacion
		self.numero_id_cliente = cliente.numero_identificacion
		self.numero_id_cli_adicional = cliente.numero_id_adicional
		self.dir_cliente = cliente.direccion
		self.ciudad_cliente = cliente.ciudad
		self.departamento_cliente = cliente.departamento
		self.pais_cliente = cliente.pais
		self.telefono_cliente = cliente.telefono
		if cliente.terminos_de_pago:
			self.terminos_de_pago = cliente.terminos_de_pago
		if cliente.medio_de_pago:
			self.medio_de_pago = cliente.medio_de_pago
		for llave, valor in choices.MEDIOS_DE_PAGO:
			if self.medio_de_pago == llave:
				self.medio_de_pago = valor
		self.save()

	def info_item(self):
		item_selecionados = [self.item_1, self.item_2, self.item_3, self.item_4, self.item_5]
		items_codes = []
		for item in item_selecionados:
			if item:
				item_doc = Item.objects.get(codigo=item, org_creadora=self.org_creadora)
				item_code = item_doc.codigo
				items_codes.append(item_code)
			else:
				items_codes.append(None)
		self.item_1_code = items_codes[0]
		self.item_2_code = items_codes[1]
		self.item_3_code = items_codes[2]
		self.item_4_code = items_codes[3]
		self.item_5_code = items_codes[4]
		self.save()

		descripciones = []
		for item in item_selecionados:
			if item:
				item_doc = Item.objects.get(codigo=item, org_creadora=self.org_creadora)
				descripcion = item_doc.descripcion
				descripciones.append(descripcion)
			else:
				descripciones.append(None)
		self.descripcion_1 = descripciones[0]
		self.descripcion_2 = descripciones[1]
		self.descripcion_3 = descripciones[2]
		self.descripcion_4 = descripciones[3]
		self.descripcion_5 = descripciones[4]
		self.save()

		if self.descripcion_detallada == 'No Registrado' or self.descripcion_detallada == '':
			descripciones_detalle = []
			for item in item_selecionados:
				if item:
					item_doc = Item.objects.get(codigo=item, org_creadora=self.org_creadora)
					if item_doc.descripcion_detalle:
						descripcion = '- %s\n' %(item_doc.descripcion_detalle)
						descripciones_detalle.append(descripcion)
			descrip_detail = ''
			for descripcion in descripciones_detalle:
				descrip_detail = descrip_detail + descripcion
			self.descripcion_detallada = descrip_detail

		unidadesmedida = []
		for item in item_selecionados:
			if item:
				item_doc = Item.objects.get(codigo=item, org_creadora=self.org_creadora)
				UM = item_doc.unidad_medida
				unidadesmedida.append(UM)
			else:
				unidadesmedida.append(None)
		self.UM_1 = unidadesmedida[0]
		self.UM_2 = unidadesmedida[1]
		self.UM_3 = unidadesmedida[2]
		self.UM_4 = unidadesmedida[3]
		self.UM_5 = unidadesmedida[4]
		self.save()

		valoresunitarios = []
		for item in item_selecionados:
			if item:
				item_doc = Item.objects.get(codigo=item, org_creadora=self.org_creadora)
				valor_unitario = item_doc.precio_venta
				valoresunitarios.append(valor_unitario)
			else:
				valoresunitarios.append(0)
		self.valor_unitario_1 = valoresunitarios[0]
		self.valor_unitario_2 = valoresunitarios[1]
		self.valor_unitario_3 = valoresunitarios[2]
		self.valor_unitario_4 = valoresunitarios[3]
		self.valor_unitario_5 = valoresunitarios[4]
		self.save()

	def calculo_item(self):
		item_selecionados = [self.item_1, self.item_2, self.item_3, self.item_4, self.item_5]
		valoresunitarios = []
		for item in item_selecionados:
			if item:
				item_doc = Item.objects.get(codigo=item, org_creadora=self.org_creadora)
				valor_unitario = item_doc.precio_venta
				valoresunitarios.append(valor_unitario)
			else:
				valoresunitarios.append(0)
		self.valor_unitario_1 = valoresunitarios[0]
		self.valor_unitario_2 = valoresunitarios[1]
		self.valor_unitario_3 = valoresunitarios[2]
		self.valor_unitario_4 = valoresunitarios[3]
		self.valor_unitario_5 = valoresunitarios[4]

		porcentajesdescuento = [self.porcentaje_descuento_1, self.porcentaje_descuento_2, self.porcentaje_descuento_3, self.porcentaje_descuento_4, self.porcentaje_descuento_5]
		cantidades = [self.cantidad_1, self.cantidad_2, self.cantidad_3, self.cantidad_4, self.cantidad_5]
		cantidades_nuevo = []
		for valor in cantidades:
			if valor == None:
				cantidades_nuevo.append(0)
			else:
				cantidades_nuevo.append(valor)
		self.cantidad_1 = cantidades_nuevo[0]
		self.cantidad_2 = cantidades_nuevo[1]
		self.cantidad_3 = cantidades_nuevo[2]
		self.cantidad_4 = cantidades_nuevo[3]
		self.cantidad_5 = cantidades_nuevo[4]

		porcentajesdescuento_nuevo = []
		for valor in porcentajesdescuento:
			if valor == None:
				porcentajesdescuento_nuevo.append(0)
			else:
				porcentajesdescuento_nuevo.append(valor)
		self.porcentaje_descuento_1 = porcentajesdescuento_nuevo[0]
		self.porcentaje_descuento_2 = porcentajesdescuento_nuevo[1]
		self.porcentaje_descuento_3 = porcentajesdescuento_nuevo[2]
		self.porcentaje_descuento_4 = porcentajesdescuento_nuevo[3]
		self.porcentaje_descuento_5 = porcentajesdescuento_nuevo[4]

		valoresdescuento = []
		indice = 0
		for valor in valoresunitarios:
			if cantidades_nuevo[indice] or porcentajesdescuento_nuevo[indice]:
				valordescuento = valor * cantidades_nuevo[indice] * porcentajesdescuento_nuevo[indice]/100
				valoresdescuento.append(valordescuento)
			else:
				valoresdescuento.append(0)
			indice += 1
		self.valor_descuento_1 = valoresdescuento[0]
		self.valor_descuento_2 = valoresdescuento[1]
		self.valor_descuento_3 = valoresdescuento[2]
		self.valor_descuento_4 = valoresdescuento[3]
		self.valor_descuento_5 = valoresdescuento[4]

		valorestotales = []
		indice = 0
		for valor in valoresunitarios:
			if cantidades[indice]:
				valortotal = valor * cantidades_nuevo[indice] - valoresdescuento[indice]
				valorestotales.append(valortotal)
			else:
				valorestotales.append(0)
			indice += 1
		self.valor_total_1 = valorestotales[0]
		self.valor_total_2 = valorestotales[1]
		self.valor_total_3 = valorestotales[2]
		self.valor_total_4 = valorestotales[3]
		self.valor_total_5 = valorestotales[4]
		self.sub_total = self.valor_total_1 + self.valor_total_2 + self.valor_total_3 + self.valor_total_4 + self.valor_total_5

		if self.org_creadora.responsable_iva == 'SI':
			numeros = ['1', '2', '3', '4']
			tarifas_de_iva = [19, 5, 0, 0]
			iva_item = []
			indice = 0
			for item in item_selecionados:
				if item:
					item_doc = Item.objects.get(codigo=item, org_creadora=self.org_creadora)
					if item_doc.iva_ventas:
						tariva = 0
						for numero in numeros:
							if item_doc.iva_ventas == numero:
								iva = float(valorestotales[indice]) * (tarifas_de_iva[tariva]/100)
								iva_item.append(int(iva))
							tariva += 1
				else:
					iva_item.append(0)
				indice += 1
			self.iva_1 = iva_item[0]
			self.iva_2 = iva_item[1]
			self.iva_3 = iva_item[2]
			self.iva_4 = iva_item[3]
			self.iva_5 = iva_item[4]
			self.iva_total = self.iva_1 + self.iva_2 + self.iva_3 + self.iva_4 + self.iva_5
			self.save()
		else:
			self.iva_total = 0
			self.save()

		cliente = Contacto.objects.get(nombre_legal=self.cliente, relacion_activa="CL", org_creadora=self.org_creadora)
		if cliente.consumidor_final == True:
			numeros = ['1', '2', '3', '4']
			tarifas_de_ico = [16, 8, 4, 0]
			ico_item = []
			indice = 0
			for item in item_selecionados:
				if item:
					item_doc = Item.objects.get(codigo=item, org_creadora=self.org_creadora)
					if item_doc.impuesto_consumo_ventas:
						tarico = 0
						for numero in numeros:
							if item_doc.impuesto_consumo_ventas == numero:
								ico = float(valorestotales[indice]) * (tarifas_de_ico[tarico]/100)
								ico_item.append(int(ico))
							tarico += 1
				else:
					ico_item.append(0)
				indice += 1
			self.ico_1 = ico_item[0]
			self.ico_2 = ico_item[1]
			self.ico_3 = ico_item[2]
			self.ico_4 = ico_item[3]
			self.ico_5 = ico_item[4]
			self.ico_total = self.ico_1 + self.ico_2 + self.ico_3 + self.ico_4 + self.ico_5
			self.save()
		else:
			self.ico_total = 0
			self.save()

		item_selecionados = [self.item_1, self.item_2, self.item_3, self.item_4, self.item_5]
		cantidades = [self.cantidad_1, self.cantidad_2, self.cantidad_3, self.cantidad_4, self.cantidad_5]
		indice = 0
		for item in item_selecionados:
			if item:
				item_doc = Item.objects.get(codigo=item, org_creadora=self.org_creadora)
				if item_doc.tipo_item == 'IN':
					if item_doc.cantidad != None and item_doc.cantidad != 'No Registrado':
						item_doc.cantidad = item_doc.cantidad - cantidades[indice]
						item_doc.save()
			indice += 1

		if self.org_creadora.declarante_impuesto_renta == True or self.org_creadora.declarante_impuesto_renta == False:
			if self.org_creadora.ventas_liquidar_reterenta == True and self.org_creadora.ventas_liquidar_autoretencion_renta == False and cliente.ventas_liquidar_reterenta == True:
				numeros = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16" ,"17", "18", "19", "20",
				"21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40",
				"41", "42", "43", "44", "45", "46", "47", "48"]
				bases = [0,961000,0,961000,0,0,0,0,0,0,0,0,0,0,142000,0,142000,0,142000,961000,0,142000,0,142000,0,142000,0,142000,0,0,
				961000,0,0,0,3276000,0,0,0,0,0,0,961000,0,0,5697000,0,0,0]
				tarifas_de_reterenta = [0,2.5,2.5,3.5,3.5,1,0.1,10,11,3.5,6,10,10,11,1,1,2,2,3.5,3.5,3.5,4,4,6,6,1,1,2,2,4,3.5,3.5,7,4,1.5,1.5,0.75,
				15,20,5,15,2,2,0.5,0.5,10,11,2.5]
				indice = 0
				reterentas = 0
				for numero in numeros:
					totalval = 0
					bases_retefuenterenta = 0
					for item in item_selecionados:
						if item:
							item_doc = Item.objects.get(codigo=item, org_creadora=self.org_creadora)
							if item_doc.tarifa_reterenta:
								if item_doc.tarifa_reterenta == numero:
									bases_retefuenterenta = bases_retefuenterenta + valorestotales[totalval]
						totalval = totalval + 1
					if bases_retefuenterenta > bases[indice]:
						reterentas = reterentas + (float(bases_retefuenterenta) * (tarifas_de_reterenta[indice]/100))
					indice = indice + 1
				self.reterenta = int(reterentas)
				self.autoreterenta = 0
				self.save()
			elif self.org_creadora.ventas_liquidar_autoretencion_renta == True:
				numeros = ['1', '2', '3']
				tarifas_autoreterenta = [0.4, 0.8, 1.6]
				indice = 0
				if self.org_creadora.tarifa_autoreterenta == None:
					self.autoreterenta = 0
					self.save()
				for numero in numeros:
					if self.org_creadora.tarifa_autoreterenta == numero:
						self.autoreterenta = self.sub_total * (tarifas_autoreterenta[indice]/100)
						self.reterenta = 0
						self.save()
					indice = indice + 1
			elif self.org_creadora.ventas_liquidar_reterenta == True and self.org_creadora.ventas_liquidar_autorreterenta_clientes_regimen_simple == True :
				if self.org_creadora.regimen_tributario == 2 and cliente.regimen_tributario == 0:
					numeros = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16" ,"17", "18", "19", "20",
				"21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40",
				"41", "42", "43", "44", "45", "46", "47", "48"]
				bases = [0,961000,0,961000,0,0,0,0,0,0,0,0,0,0,142000,0,142000,0,142000,961000,0,142000,0,142000,0,142000,0,142000,0,0,
				961000,0,0,0,3276000,0,0,0,0,0,0,961000,0,0,5697000,0,0,0]
				tarifas_de_reterenta = [0,2.5,2.5,3.5,3.5,1,0.1,10,11,3.5,6,10,10,11,1,1,2,2,3.5,3.5,3.5,4,4,6,6,1,1,2,2,4,3.5,3.5,7,4,1.5,1.5,0.75,
				15,20,5,15,2,2,0.5,0.5,10,11,2.5]
				indice = 0
				reterentas = 0
				for numero in numeros:
					totalval = 0
					bases_retefuenterenta = 0
					for item in item_selecionados:
						if item:
							item_doc = Item.objects.get(codigo=item, org_creadora=self.org_creadora)
							if item_doc.tarifa_reterenta:
								if item_doc.tarifa_reterenta == numero:
									bases_retefuenterenta = bases_retefuenterenta + valorestotales[totalval]
						totalval = totalval + 1
					if bases_retefuenterenta > bases[indice]:
						reterentas = reterentas + (float(bases_retefuenterenta) * (tarifas_de_reterenta[indice]/100))
					indice = indice + 1
					self.autoreterenta = int(reterentas)
					self.reterenta = 0
					self.save()
			else:
				self.reterenta = 0
				self.autoreterenta = 0
				self.save()
		else:
			self.reterenta = 0
			self.autoreterenta = 0
			self.save()

		if self.org_creadora.ventas_liquidar_reteica == True and cliente.ventas_liquidar_reteica == True:
			if self.org_creadora.ciudad == cliente.ciudad:
				if self.org_creadora.gran_contribuyente == True:
					self.reteica = 0
					self.save()
				elif self.org_creadora.regimen_tributario == '2' or self.org_creadora.regimen_tributario == '0':
					if cliente.regimen_tributario == '0':
						self.reteica = 0
						self.save()
					else:
						if self.org_creadora.tarifa_liquidar_reteica == None:
							self.reteica = 0
							self.save()
						else:
							self.reteica = self.sub_total * (self.org_creadora.tarifa_liquidar_reteica/1000)
							self.save()
				else:
					self.reteica = 0
					self.save()
			else:
				self.reteica = 0
				self.save()
		else:
			self.reteica = 0
			self.save()

		if cliente.gran_contribuyente == True:
			self.reteiva = int(self.iva_total * 0.15)
			self.save()
		elif cliente.ventas_liquidar_reteiva_responsable_iva_regimen_comun and cliente.gran_contribuyente == False and cliente.responsable_iva == 'SI':
			if self.org_creadora.responsable_iva == 'SI' and self.org_creadora.gran_contribuyente == False and self.org_creadora.regimen_tributario == '2':
				self.reteiva = int(self.iva_total * 0.15)
				self.save()
			else:
				self.reteiva = 0
				self.save()
		elif cliente.ventas_liquidar_reteiva_responsable_iva_regimen_simple and cliente.regimen_tributario == '2' and cliente.responsable_iva == 'SI':
			if self.org_creadora.responsable_iva == 'SI' and self.org_creadora.regimen_tributario == '0':
				self.reteiva = int(self.iva_total * 0.15)
				self.save()
			else:
				self.reteiva = 0
				self.save()
		else:
			self.reteiva = 0
			self.save()
			
		if self.anticipo == None:
			self.anticipo = 0
			self.save()

	def calculo_total_factura(self):
		self.total_impuestos = self.iva_total + self.ico_total
		self.total_retenciones = self.reterenta + self.autoreterenta + self.reteiva + self.reteica
		self.total_documento = self.sub_total + self.total_impuestos - self.total_retenciones
		self.saldo_pendiente = self.total_documento - self.anticipo
		self.save()

	def tipo_impuestodoc(self):
		if self.iva_total:
			self.tipo_imp1 = "01"
			self.save()
		if self.ico_total:
			self.tipo_imp2 = "02"
			self.save()
		if self.reteica:
			self.tipo_imp3 = "03"
			self.save()

	def generar_remision(self):
		nueva_remision = Remision(referencia_factura=self.consecutivo_interno,referencia_cotizacion=self.referencia_cotizacion,referencia_orden_compra=self.referencia_orden_compra,
			referencia_otro_documento=self.referencia_otro_documento,vendedor=self.vendedor,org_creadora=self.org_creadora,cliente=self.cliente,
			item_1=self.item_1,item_2=self.item_2,item_3=self.item_3,item_4=self.item_4,item_5=self.item_5,UM_1=self.UM_1,UM_2=self.UM_2,UM_3=self.UM_3,
			UM_4=self.UM_4,UM_5=self.UM_5,cantidad_1=self.cantidad_1,cantidad_2=self.cantidad_2,cantidad_3=self.cantidad_3,cantidad_4=self.cantidad_4,cantidad_5=self.cantidad_5,
			descripcion_1=self.descripcion_1,descripcion_2=self.descripcion_2,descripcion_3=self.descripcion_3,descripcion_4=self.descripcion_4,descripcion_5=self.descripcion_5,
			descripcion_detallada=self.descripcion_detallada,observacion=self.observacion)
		return nueva_remision

	
	def generar_nota_credito(self):
		nueva_creditnote = Nota_credito(referencia_factura=self.consecutivo_interno, referencia_factura_DIAN=self.consecutivo_DIAN,fecha_emision_factura=self.fecha_emision,referencia_cotizacion=self.referencia_cotizacion,
			referencia_remision=self.referencia_remision,referencia_orden_compra=self.referencia_orden_compra,referencia_otro_documento=self.referencia_otro_documento,
		    tipo_imp1=self.tipo_imp1,tipo_imp2=self.tipo_imp2,tipo_imp3=self.tipo_imp3,terminos_de_pago=self.terminos_de_pago, medio_de_pago=self.medio_de_pago, moneda=self.moneda, vendedor=self.vendedor,
		    org_creadora=self.org_creadora,id_organizacion=self.id_organizacion,numero_id_organizacion=self.numero_id_organizacion,numero_id_org_adicional=self.numero_id_org_adicional,dir_organizacion=self.dir_organizacion,
			ciudad_organizacion=self.ciudad_organizacion,departamento_organizacion=self.departamento_organizacion,pais_organizacion=self.pais_organizacion, telefono_organizacion=self.telefono_organizacion,
			cliente=self.cliente,id_cliente=self.id_cliente,numero_id_cliente=self.numero_id_cliente,numero_id_cli_adicional=self.numero_id_cli_adicional,dir_cliente=self.dir_cliente,
			ciudad_cliente=self.ciudad_cliente,departamento_cliente=self.departamento_cliente,pais_cliente=self.pais_cliente,telefono_cliente=self.telefono_cliente,item_1=self.item_1,
			item_2=self.item_2, item_3=self.item_3, item_4=self.item_4, item_5=self.item_5,cantidad_1=self.cantidad_1,cantidad_2=self.cantidad_2, cantidad_3=self.cantidad_3, cantidad_4=self.cantidad_4, cantidad_5=self.cantidad_5, UM_1=self.UM_1,
			UM_2=self.UM_2,UM_3=self.UM_3,UM_4=self.UM_4,UM_5=self.UM_5,valor_unitario_1=self.valor_unitario_1,valor_unitario_2=self.valor_unitario_2,
			valor_unitario_3=self.valor_unitario_3, valor_unitario_4=self.valor_unitario_4, valor_unitario_5=self.valor_unitario_5, porcentaje_descuento_1=self.porcentaje_descuento_1,
			porcentaje_descuento_2=self.porcentaje_descuento_2, porcentaje_descuento_3=self.porcentaje_descuento_3, porcentaje_descuento_4=self.porcentaje_descuento_4, porcentaje_descuento_5=self.porcentaje_descuento_5,
			valor_descuento_1=self.valor_descuento_1, valor_descuento_2=self.valor_descuento_2, valor_descuento_3=self.valor_descuento_3, valor_descuento_4=self.valor_descuento_4, valor_descuento_5=self.valor_descuento_5,
			iva_1=self.iva_1,iva_2=self.iva_2,iva_3=self.iva_3,iva_4=self.iva_4,iva_5=self.iva_5,ico_1=self.ico_1,ico_2=self.ico_2,ico_3=self.ico_3,ico_4=self.ico_4,ico_5=self.ico_5,
			valor_total_1=self.valor_total_1, valor_total_2=self.valor_total_2, valor_total_3=self.valor_total_3, valor_total_4=self.valor_total_4, valor_total_5=self.valor_total_5,iva_total=self.iva_total,ico_total=self.ico_total,
			reterenta=self.reterenta,reteiva=self.reteiva,reteica=self.reteica,descripcion_1=self.descripcion_1, descripcion_2=self.descripcion_2, descripcion_3=self.descripcion_3, descripcion_4=self.descripcion_4, descripcion_5=self.descripcion_5,
			sub_total=self.sub_total,total_impuestos=self.total_impuestos,total_retenciones=self.total_retenciones,total_documento=self.total_documento,anticipo=self.anticipo,saldo_pendiente=self.saldo_pendiente,
			descripcion_detallada=self.descripcion_detallada,observacion=self.observacion)
		return nueva_creditnote


	def generar_nota_debito(self):
		nueva_debitnote = Nota_debito(referencia_factura=self.consecutivo_interno, referencia_factura_DIAN=self.consecutivo_DIAN,fecha_emision_factura=self.fecha_emision,referencia_cotizacion=self.referencia_cotizacion,
			referencia_remision=self.referencia_remision,referencia_orden_compra=self.referencia_orden_compra,referencia_otro_documento=self.referencia_otro_documento,
		    tipo_imp1=self.tipo_imp1,tipo_imp2=self.tipo_imp2,tipo_imp3=self.tipo_imp3,terminos_de_pago=self.terminos_de_pago, medio_de_pago=self.medio_de_pago, moneda=self.moneda, vendedor=self.vendedor,
		    org_creadora=self.org_creadora,id_organizacion=self.id_organizacion,numero_id_organizacion=self.numero_id_organizacion,numero_id_org_adicional=self.numero_id_org_adicional,dir_organizacion=self.dir_organizacion,
			ciudad_organizacion=self.ciudad_organizacion,departamento_organizacion=self.departamento_organizacion,pais_organizacion=self.pais_organizacion, telefono_organizacion=self.telefono_organizacion,
			cliente=self.cliente,id_cliente=self.id_cliente,numero_id_cliente=self.numero_id_cliente,numero_id_cli_adicional=self.numero_id_cli_adicional,dir_cliente=self.dir_cliente,
			ciudad_cliente=self.ciudad_cliente,departamento_cliente=self.departamento_cliente,pais_cliente=self.pais_cliente,telefono_cliente=self.telefono_cliente,item_1=self.item_1,
			item_2=self.item_2, item_3=self.item_3, item_4=self.item_4, item_5=self.item_5,cantidad_1=self.cantidad_1,cantidad_2=self.cantidad_2, cantidad_3=self.cantidad_3, cantidad_4=self.cantidad_4, cantidad_5=self.cantidad_5, UM_1=self.UM_1,
			UM_2=self.UM_2,UM_3=self.UM_3,UM_4=self.UM_4,UM_5=self.UM_5,valor_unitario_1=self.valor_unitario_1,valor_unitario_2=self.valor_unitario_2,
			valor_unitario_3=self.valor_unitario_3, valor_unitario_4=self.valor_unitario_4, valor_unitario_5=self.valor_unitario_5, porcentaje_descuento_1=self.porcentaje_descuento_1,
			porcentaje_descuento_2=self.porcentaje_descuento_2, porcentaje_descuento_3=self.porcentaje_descuento_3, porcentaje_descuento_4=self.porcentaje_descuento_4, porcentaje_descuento_5=self.porcentaje_descuento_5,
			valor_descuento_1=self.valor_descuento_1, valor_descuento_2=self.valor_descuento_2, valor_descuento_3=self.valor_descuento_3, valor_descuento_4=self.valor_descuento_4, valor_descuento_5=self.valor_descuento_5,
			iva_1=self.iva_1,iva_2=self.iva_2,iva_3=self.iva_3,iva_4=self.iva_4,iva_5=self.iva_5,ico_1=self.ico_1,ico_2=self.ico_2,ico_3=self.ico_3,ico_4=self.ico_4,ico_5=self.ico_5,
			valor_total_1=self.valor_total_1, valor_total_2=self.valor_total_2, valor_total_3=self.valor_total_3, valor_total_4=self.valor_total_4, valor_total_5=self.valor_total_5,iva_total=self.iva_total,ico_total=self.ico_total,
			reterenta=self.reterenta,reteiva=self.reteiva,reteica=self.reteica,descripcion_1=self.descripcion_1, descripcion_2=self.descripcion_2, descripcion_3=self.descripcion_3, descripcion_4=self.descripcion_4, descripcion_5=self.descripcion_5,
			sub_total=self.sub_total,total_impuestos=self.total_impuestos,total_retenciones=self.total_retenciones,total_documento=self.total_documento,anticipo=self.anticipo,saldo_pendiente=self.saldo_pendiente,
			descripcion_detallada=self.descripcion_detallada,observacion=self.observacion)
		return nueva_debitnote

	def __str__(self):
		self.save()
		return '%s %s %s'%(self.consecutivo_interno, self.cliente, self.fecha_emision)


class Nota_credito(models.Model):
	tipo_de_documento = models.CharField(max_length=100, null=True, blank=True)
	consecutivo_DIAN = models.CharField(max_length=100, null=True, blank=True)
	consecutivo_interno = models.CharField(max_length=100, null=True, blank=True)
	consec_inter_prefijo = models.CharField(max_length=3, null=True, blank=True)
	consec_inter_numero = models.PositiveIntegerField(null=True, blank=True)
	referencia_otro_documento = models.CharField(max_length=100, null=True, blank=True)
	referencia_orden_compra = models.CharField(max_length=100, null=True, blank=True)
	referencia_cotizacion = models.CharField(max_length=100, null=True, blank=True)
	referencia_remision = models.CharField(max_length=100, null=True, blank=True)
	referencia_factura = models.CharField(max_length=100, null=True, blank=True)
	referencia_factura_DIAN = models.TextField(max_length=200, null=True, blank=True)
	fecha_emision_factura = models.DateTimeField(null=True, blank=True)
	fecha_emision = models.DateTimeField(null=True, blank=True)
	fecha_pago = models.DateTimeField(null=True, blank=True)
	tipo_imp1 = models.CharField(max_length=2, choices=choices.TIPO_IMPUESTO, null=True, blank=True)
	tipo_imp2 = models.CharField(max_length=2, choices=choices.TIPO_IMPUESTO, null=True, blank=True)
	tipo_imp3 = models.CharField(max_length=2, choices=choices.TIPO_IMPUESTO, null=True, blank=True)
	terminos_de_pago = models.CharField(max_length=300, null=True, blank=True)
	medio_de_pago = models.CharField(max_length=2, choices=choices.MEDIOS_DE_PAGO, null=True, blank=True)
	moneda = models.CharField(max_length=3, choices=choices.MONEDAS, null=True, blank=True)
	vendedor = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
	org_creadora = models.ForeignKey(Organizacion, on_delete=models.CASCADE, limit_choices_to={'activa':True}, null=True, blank=True)
	id_organizacion = models.CharField(max_length=50, null=True, blank=True)
	numero_id_organizacion = models.CharField(max_length=50, null=True, blank=True)
	numero_id_org_adicional = models.CharField(max_length=4, null=True, blank=True)
	dir_organizacion = models.CharField(max_length=50, null=True, blank=True)
	ciudad_organizacion = models.CharField(max_length=50, null=True, blank=True)
	departamento_organizacion = models.CharField(max_length=50, null=True, blank=True)
	pais_organizacion = models.CharField(max_length=50, null=True, blank=True)
	telefono_organizacion = models.CharField(max_length=50, null=True, blank=True)
	cliente = models.CharField(max_length=300, null=True, blank=True)
	nombre_cliente = models.CharField(max_length=50, null=True, blank=True)
	id_cliente = models.CharField(max_length=50, null=True, blank=True)
	numero_id_cliente = models.CharField(max_length=50, null=True, blank=True)
	numero_id_cli_adicional = models.CharField(max_length=4, null=True, blank=True)
	dir_cliente = models.CharField(max_length=50, null=True, blank=True)
	ciudad_cliente = models.CharField(max_length=50, null=True, blank=True)
	departamento_cliente = models.CharField(max_length=50, null=True, blank=True)
	pais_cliente = models.CharField(max_length=50, null=True, blank=True)
	telefono_cliente = models.CharField(max_length=50, null=True, blank=True)
	item_1 = models.CharField(max_length=300, null=True, blank=True)
	item_2 = models.CharField(max_length=300, null=True, blank=True)
	item_3 = models.CharField(max_length=300, null=True, blank=True)
	item_4 = models.CharField(max_length=300, null=True, blank=True)
	item_5 = models.CharField(max_length=300, null=True, blank=True)
	cantidad_1 = models.IntegerField(blank=True, null=True)
	cantidad_2 = models.IntegerField(blank=True, null=True)
	cantidad_3 = models.IntegerField(blank=True, null=True)
	cantidad_4 = models.IntegerField(blank=True, null=True)
	cantidad_5 = models.IntegerField(blank=True, null=True)
	UM_1 = models.CharField(max_length=20, null=True, blank=True)
	UM_2 = models.CharField(max_length=20, null=True, blank=True)
	UM_3 = models.CharField(max_length=20, null=True, blank=True)
	UM_4 = models.CharField(max_length=20, null=True, blank=True)
	UM_5 = models.CharField(max_length=20, null=True, blank=True)
	valor_unitario_1 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_unitario_2 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_unitario_3 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_unitario_4 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_unitario_5 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	porcentaje_descuento_1 = models.IntegerField(blank=True, null=True)
	porcentaje_descuento_2 = models.IntegerField(blank=True, null=True)
	porcentaje_descuento_3 = models.IntegerField(blank=True, null=True)
	porcentaje_descuento_4 = models.IntegerField(blank=True, null=True)
	porcentaje_descuento_5 = models.IntegerField(blank=True, null=True)
	valor_descuento_1 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_descuento_2 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_descuento_3 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_descuento_4 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_descuento_5 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	iva_1 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	iva_2 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	iva_3 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	iva_4 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	iva_5 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	ico_1 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	ico_2 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	ico_3 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	ico_4 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	ico_5 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_total_1 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_total_2 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_total_3 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_total_4 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_total_5 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	iva_total = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	ico_total = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	reterenta = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	autoreterenta = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	reteiva = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	reteica = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	sub_total = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	total_impuestos = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	total_retenciones = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	total_documento = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	anticipo = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	saldo_pendiente = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	descripcion_1 = models.CharField(max_length=400,  null=True, blank=True)
	descripcion_2 = models.CharField(max_length=400,  null=True, blank=True)
	descripcion_3 = models.CharField(max_length=400,  null=True, blank=True)
	descripcion_4 = models.CharField(max_length=400,  null=True, blank=True)
	descripcion_5 = models.CharField(max_length=400,  null=True, blank=True)
	descripcion_detallada = models.TextField(null=True, blank=True)
	observacion = models.CharField(max_length=200,  null=True, blank=True)
	cifra_total_en_palabras = models.CharField(max_length=300,  null=True, blank=True)
	concepto_nota_credito = models.CharField(max_length=1, choices=choices.CONCEPTO_NOTA_CREDITO, null=True, blank=True)
	item_1_afec = models.CharField(max_length=100, null=True, blank=True)
	item_2_afec = models.CharField(max_length=100, null=True, blank=True)
	item_3_afec = models.CharField(max_length=100, null=True, blank=True)
	item_4_afec = models.CharField(max_length=100, null=True, blank=True)
	item_5_afec = models.CharField(max_length=100, null=True, blank=True)
	descuento_rebaja = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	saldo_total = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	generado = models.BooleanField(default=False)
	pagada = models.BooleanField(default=False)


	def auto_consecutivo(self):
		consecutivo = Consecutivo_documento.objects.get(org_creadora=self.org_creadora, tipo_de_documento="NCT", generado=True)
		doc_creados = Nota_credito.objects.filter(org_creadora=self.org_creadora, generado=True).count()
		ultimo_doc = Nota_credito.objects.filter(org_creadora=self.org_creadora, generado=True).last()
		self.tipo_de_documento = consecutivo.codigo
		if doc_creados == 0:
			self.consec_inter_prefijo = consecutivo.pre_fijo
			self.consec_inter_numero = consecutivo.numero
			self.consecutivo_interno = '%s %s'%(self.consec_inter_prefijo, self.consec_inter_numero)
			self.save()
		elif doc_creados > 0:
			nuevo_num = ultimo_doc.consec_inter_numero + 1
			self.consec_inter_prefijo = consecutivo.pre_fijo
			self.consec_inter_numero = nuevo_num
			self.consecutivo_interno = '%s %s'%(self.consec_inter_prefijo, self.consec_inter_numero)
			self.save()


	def calculo_item(self):
		item_selecionados = [self.item_1, self.item_2, self.item_3, self.item_4, self.item_5]
		valoresunitarios = []
		for item in item_selecionados:
			if item:
				item_doc = Item.objects.get(codigo=item, org_creadora=self.org_creadora)
				valor_unitario = item_doc.precio_venta
				valoresunitarios.append(valor_unitario)
			else:
				valoresunitarios.append(0)
		self.valor_unitario_1 = valoresunitarios[0]
		self.valor_unitario_2 = valoresunitarios[1]
		self.valor_unitario_3 = valoresunitarios[2]
		self.valor_unitario_4 = valoresunitarios[3]
		self.valor_unitario_5 = valoresunitarios[4]

		porcentajesdescuento = [self.porcentaje_descuento_1, self.porcentaje_descuento_2, self.porcentaje_descuento_3, self.porcentaje_descuento_4, self.porcentaje_descuento_5]
		cantidades = [self.cantidad_1, self.cantidad_2, self.cantidad_3, self.cantidad_4, self.cantidad_5]
		cantidades_nuevo = []
		for valor in cantidades:
			if valor == None:
				cantidades_nuevo.append(0)
			else:
				cantidades_nuevo.append(valor)
		self.cantidad_1 = cantidades_nuevo[0]
		self.cantidad_2 = cantidades_nuevo[1]
		self.cantidad_3 = cantidades_nuevo[2]
		self.cantidad_4 = cantidades_nuevo[3]
		self.cantidad_5 = cantidades_nuevo[4]

		porcentajesdescuento_nuevo = []
		for valor in porcentajesdescuento:
			if valor == None:
				porcentajesdescuento_nuevo.append(0)
			else:
				porcentajesdescuento_nuevo.append(valor)
		self.porcentaje_descuento_1 = porcentajesdescuento_nuevo[0]
		self.porcentaje_descuento_2 = porcentajesdescuento_nuevo[1]
		self.porcentaje_descuento_3 = porcentajesdescuento_nuevo[2]
		self.porcentaje_descuento_4 = porcentajesdescuento_nuevo[3]
		self.porcentaje_descuento_5 = porcentajesdescuento_nuevo[4]

		valoresdescuento = []
		indice = 0
		for valor in valoresunitarios:
			if cantidades_nuevo[indice] or porcentajesdescuento_nuevo[indice]:
				valordescuento = valor * cantidades_nuevo[indice] * porcentajesdescuento_nuevo[indice]/100
				valoresdescuento.append(valordescuento)
			else:
				valoresdescuento.append(0)
			indice += 1
		self.valor_descuento_1 = valoresdescuento[0]
		self.valor_descuento_2 = valoresdescuento[1]
		self.valor_descuento_3 = valoresdescuento[2]
		self.valor_descuento_4 = valoresdescuento[3]
		self.valor_descuento_5 = valoresdescuento[4]

		valorestotales = []
		indice = 0
		for valor in valoresunitarios:
			if cantidades[indice]:
				valortotal = valor * cantidades_nuevo[indice] - valoresdescuento[indice]
				valorestotales.append(valortotal)
			else:
				valorestotales.append(0)
			indice += 1
		self.valor_total_1 = valorestotales[0]
		self.valor_total_2 = valorestotales[1]
		self.valor_total_3 = valorestotales[2]
		self.valor_total_4 = valorestotales[3]
		self.valor_total_5 = valorestotales[4]
		self.sub_total = self.valor_total_1 + self.valor_total_2 + self.valor_total_3 + self.valor_total_4 + self.valor_total_5

		if self.org_creadora.responsable_iva == 'SI':
			numeros = ['1', '2', '3', '4']
			tarifas_de_iva = [19, 5, 0, 0]
			iva_item = []
			indice = 0
			for item in item_selecionados:
				if item:
					item_doc = Item.objects.get(codigo=item, org_creadora=self.org_creadora)
					if item_doc.iva_ventas:
						tariva = 0
						for numero in numeros:
							if item_doc.iva_ventas == numero:
								iva = float(valorestotales[indice]) * (tarifas_de_iva[tariva]/100)
								iva_item.append(int(iva))
							tariva += 1
				else:
					iva_item.append(0)
				indice += 1
			self.iva_1 = iva_item[0]
			self.iva_2 = iva_item[1]
			self.iva_3 = iva_item[2]
			self.iva_4 = iva_item[3]
			self.iva_5 = iva_item[4]
			self.iva_total = self.iva_1 + self.iva_2 + self.iva_3 + self.iva_4 + self.iva_5
			self.save()
		else:
			self.iva_total = 0
			self.save()

		cliente = Contacto.objects.get(nombre_legal=self.cliente, relacion_activa="CL", org_creadora=self.org_creadora)
		if cliente.consumidor_final == True:
			numeros = ['1', '2', '3', '4']
			tarifas_de_ico = [16, 8, 4, 0]
			ico_item = []
			indice = 0
			for item in item_selecionados:
				if item:
					item_doc = Item.objects.get(codigo=item, org_creadora=self.org_creadora)
					if item_doc.impuesto_consumo_ventas:
						tarico = 0
						for numero in numeros:
							if item_doc.impuesto_consumo_ventas == numero:
								ico = float(valorestotales[indice]) * (tarifas_de_ico[tarico]/100)
								ico_item.append(int(ico))
							tarico += 1
				else:
					ico_item.append(0)
				indice += 1
			self.ico_1 = ico_item[0]
			self.ico_2 = ico_item[1]
			self.ico_3 = ico_item[2]
			self.ico_4 = ico_item[3]
			self.ico_5 = ico_item[4]
			self.ico_total = self.ico_1 + self.ico_2 + self.ico_3 + self.ico_4 + self.ico_5
			self.save()
		else:
			self.ico_total = 0
			self.save()

		if self.org_creadora.declarante_impuesto_renta == True or self.org_creadora.declarante_impuesto_renta == False:
			if self.org_creadora.ventas_liquidar_reterenta == True and self.org_creadora.ventas_liquidar_autoretencion_renta == False and cliente.ventas_liquidar_reterenta == True:
				numeros = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16" ,"17", "18", "19", "20",
				"21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40",
				"41", "42", "43", "44", "45", "46", "47", "48"]
				bases = [0,961000,0,961000,0,0,0,0,0,0,0,0,0,0,142000,0,142000,0,142000,961000,0,142000,0,142000,0,142000,0,142000,0,0,
				961000,0,0,0,3276000,0,0,0,0,0,0,961000,0,0,5697000,0,0,0]
				tarifas_de_reterenta = [0,2.5,2.5,3.5,3.5,1,0.1,10,11,3.5,6,10,10,11,1,1,2,2,3.5,3.5,3.5,4,4,6,6,1,1,2,2,4,3.5,3.5,7,4,1.5,1.5,0.75,
				15,20,5,15,2,2,0.5,0.5,10,11,2.5]
				indice = 0
				reterentas = 0
				for numero in numeros:
					totalval = 0
					bases_retefuenterenta = 0
					for item in item_selecionados:
						if item:
							item_doc = Item.objects.get(codigo=item, org_creadora=self.org_creadora)
							if item_doc.tarifa_reterenta:
								if item_doc.tarifa_reterenta == numero:
									bases_retefuenterenta = bases_retefuenterenta + valorestotales[totalval]
						totalval = totalval + 1
					if bases_retefuenterenta > bases[indice]:
						reterentas = reterentas + (float(bases_retefuenterenta) * (tarifas_de_reterenta[indice]/100))
					indice = indice + 1
				self.reterenta = int(reterentas)
				self.autoreterenta = 0
				self.save()
			elif self.org_creadora.ventas_liquidar_autoretencion_renta == True:
				numeros = ['1', '2', '3']
				tarifas_autoreterenta = [0.4, 0.8, 1.6]
				indice = 0
				if self.org_creadora.tarifa_autoreterenta == None:
					self.autoreterenta = 0
					self.save()
				for numero in numeros:
					if self.org_creadora.tarifa_autoreterenta == numero:
						self.autoreterenta = self.sub_total * (tarifas_autoreterenta[indice]/100)
						self.reterenta = 0
						self.save()
					indice = indice + 1
			elif self.org_creadora.ventas_liquidar_reterenta == True and self.org_creadora.ventas_liquidar_autorreterenta_clientes_regimen_simple == True :
				if self.org_creadora.regimen_tributario == 2 and cliente.regimen_tributario == 0:
					numeros = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16" ,"17", "18", "19", "20",
				"21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40",
				"41", "42", "43", "44", "45", "46", "47", "48"]
				bases = [0,961000,0,961000,0,0,0,0,0,0,0,0,0,0,142000,0,142000,0,142000,961000,0,142000,0,142000,0,142000,0,142000,0,0,
				961000,0,0,0,3276000,0,0,0,0,0,0,961000,0,0,5697000,0,0,0]
				tarifas_de_reterenta = [0,2.5,2.5,3.5,3.5,1,0.1,10,11,3.5,6,10,10,11,1,1,2,2,3.5,3.5,3.5,4,4,6,6,1,1,2,2,4,3.5,3.5,7,4,1.5,1.5,0.75,
				15,20,5,15,2,2,0.5,0.5,10,11,2.5]
				indice = 0
				reterentas = 0
				for numero in numeros:
					totalval = 0
					bases_retefuenterenta = 0
					for item in item_selecionados:
						if item:
							item_doc = Item.objects.get(codigo=item, org_creadora=self.org_creadora)
							if item_doc.tarifa_reterenta:
								if item_doc.tarifa_reterenta == numero:
									bases_retefuenterenta = bases_retefuenterenta + valorestotales[totalval]
						totalval = totalval + 1
					if bases_retefuenterenta > bases[indice]:
						reterentas = reterentas + (float(bases_retefuenterenta) * (tarifas_de_reterenta[indice]/100))
					indice = indice + 1
					self.autoreterenta = int(reterentas)
					self.reterenta = 0
					self.save()
			else:
				self.reterenta = 0
				self.autoreterenta = 0
				self.save()
		else:
			self.reterenta = 0
			self.autoreterenta = 0
			self.save()

		if self.org_creadora.ventas_liquidar_reteica == True and cliente.ventas_liquidar_reteica == True:
			if self.org_creadora.ciudad == cliente.ciudad:
				if self.org_creadora.gran_contribuyente == True:
					self.reteica = 0
					self.save()
				elif self.org_creadora.regimen_tributario == '2' or self.org_creadora.regimen_tributario == '0':
					if cliente.regimen_tributario == '0':
						self.reteica = 0
						self.save()
					else:
						if self.org_creadora.tarifa_liquidar_reteica == None:
							self.reteica = 0
							self.save()
						else:
							self.reteica = self.sub_total * (self.org_creadora.tarifa_liquidar_reteica/1000)
							self.save()
				else:
					self.reteica = 0
					self.save()
			else:
				self.reteica = 0
				self.save()
		else:
			self.reteica = 0
			self.save()

		if cliente.gran_contribuyente == True:
			self.reteiva = int(self.iva_total * 0.15)
			self.save()
		elif cliente.ventas_liquidar_reteiva_responsable_iva_regimen_comun and cliente.gran_contribuyente == False and cliente.responsable_iva == 'SI':
			if self.org_creadora.responsable_iva == 'SI' and self.org_creadora.gran_contribuyente == False and self.org_creadora.regimen_tributario == '2':
				self.reteiva = int(self.iva_total * 0.15)
				self.save()
			else:
				self.reteiva = 0
				self.save()
		elif cliente.ventas_liquidar_reteiva_responsable_iva_regimen_simple and cliente.regimen_tributario == '2' and cliente.responsable_iva == 'SI':
			if self.org_creadora.responsable_iva == 'SI' and self.org_creadora.regimen_tributario == '0':
				self.reteiva = int(self.iva_total * 0.15)
				self.save()
			else:
				self.reteiva = 0
				self.save()
		else:
			self.reteiva = 0
			self.save()
			
		if self.anticipo == None:
			self.anticipo = 0
			self.save()

	def calculo_total_creditnote(self):
		self.total_impuestos = self.iva_total + self.ico_total
		self.total_retenciones = self.reterenta + self.autoreterenta + self.reteiva + self.reteica
		self.total_documento = self.sub_total + self.total_impuestos - self.total_retenciones
		self.saldo_pendiente = self.total_documento - self.anticipo
		self.save()

	def tipo_impuestodoc(self):
		if self.iva_total:
			self.tipo_imp1 = "01"
			self.save()
		if self.ico_total:
			self.tipo_imp2 = "02"
			self.save()
		if self.reteica:
			self.tipo_imp3 = "03"
			self.save()
	
	def __str__(self):
		self.save()
		return '%s %s %s'%(self.consecutivo_interno, self.cliente, self.fecha_emision)


class Nota_debito(models.Model):
	tipo_de_documento = models.CharField(max_length=100, null=True, blank=True)
	consecutivo_DIAN = models.CharField(max_length=100, null=True, blank=True)
	consecutivo_interno = models.CharField(max_length=100, null=True, blank=True)
	consec_inter_prefijo = models.CharField(max_length=3, null=True, blank=True)
	consec_inter_numero = models.PositiveIntegerField(null=True, blank=True)
	referencia_otro_documento = models.CharField(max_length=100, null=True, blank=True)
	referencia_orden_compra = models.CharField(max_length=100, null=True, blank=True)
	referencia_cotizacion = models.CharField(max_length=100, null=True, blank=True)
	referencia_remision = models.CharField(max_length=100, null=True, blank=True)
	referencia_factura = models.CharField(max_length=100, null=True, blank=True)
	referencia_factura_DIAN = models.TextField(max_length=200, null=True, blank=True)
	fecha_emision_factura = models.DateTimeField(null=True, blank=True)
	fecha_emision = models.DateTimeField(null=True, blank=True)
	fecha_pago = models.DateTimeField(null=True, blank=True)
	tipo_imp1 = models.CharField(max_length=2, choices=choices.TIPO_IMPUESTO, null=True, blank=True)
	tipo_imp2 = models.CharField(max_length=2, choices=choices.TIPO_IMPUESTO, null=True, blank=True)
	tipo_imp3 = models.CharField(max_length=2, choices=choices.TIPO_IMPUESTO, null=True, blank=True)
	terminos_de_pago = models.CharField(max_length=300, null=True, blank=True)
	medio_de_pago = models.CharField(max_length=2, choices=choices.MEDIOS_DE_PAGO, null=True, blank=True)
	moneda = models.CharField(max_length=3, choices=choices.MONEDAS, null=True, blank=True)
	vendedor = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
	org_creadora = models.ForeignKey(Organizacion, on_delete=models.CASCADE, limit_choices_to={'activa':True}, null=True, blank=True)
	id_organizacion = models.CharField(max_length=50, null=True, blank=True)
	numero_id_organizacion = models.CharField(max_length=50, null=True, blank=True)
	numero_id_org_adicional = models.CharField(max_length=4, null=True, blank=True)
	dir_organizacion = models.CharField(max_length=50, null=True, blank=True)
	ciudad_organizacion = models.CharField(max_length=50, null=True, blank=True)
	departamento_organizacion = models.CharField(max_length=50, null=True, blank=True)
	pais_organizacion = models.CharField(max_length=50, null=True, blank=True)
	telefono_organizacion = models.CharField(max_length=50, null=True, blank=True)
	cliente = models.CharField(max_length=300, null=True, blank=True)
	nombre_cliente = models.CharField(max_length=50, null=True, blank=True)
	id_cliente = models.CharField(max_length=50, null=True, blank=True)
	numero_id_cliente = models.CharField(max_length=50, null=True, blank=True)
	numero_id_cli_adicional = models.CharField(max_length=4, null=True, blank=True)
	dir_cliente = models.CharField(max_length=50, null=True, blank=True)
	ciudad_cliente = models.CharField(max_length=50, null=True, blank=True)
	departamento_cliente = models.CharField(max_length=50, null=True, blank=True)
	pais_cliente = models.CharField(max_length=50, null=True, blank=True)
	telefono_cliente = models.CharField(max_length=50, null=True, blank=True)
	item_1 = models.CharField(max_length=300, null=True, blank=True)
	item_2 = models.CharField(max_length=300, null=True, blank=True)
	item_3 = models.CharField(max_length=300, null=True, blank=True)
	item_4 = models.CharField(max_length=300, null=True, blank=True)
	item_5 = models.CharField(max_length=300, null=True, blank=True)
	cantidad_1 = models.IntegerField(blank=True, null=True)
	cantidad_2 = models.IntegerField(blank=True, null=True)
	cantidad_3 = models.IntegerField(blank=True, null=True)
	cantidad_4 = models.IntegerField(blank=True, null=True)
	cantidad_5 = models.IntegerField(blank=True, null=True)
	UM_1 = models.CharField(max_length=20, null=True, blank=True)
	UM_2 = models.CharField(max_length=20, null=True, blank=True)
	UM_3 = models.CharField(max_length=20, null=True, blank=True)
	UM_4 = models.CharField(max_length=20, null=True, blank=True)
	UM_5 = models.CharField(max_length=20, null=True, blank=True)
	valor_unitario_1 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_unitario_2 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_unitario_3 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_unitario_4 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_unitario_5 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	porcentaje_descuento_1 = models.IntegerField(blank=True, null=True)
	porcentaje_descuento_2 = models.IntegerField(blank=True, null=True)
	porcentaje_descuento_3 = models.IntegerField(blank=True, null=True)
	porcentaje_descuento_4 = models.IntegerField(blank=True, null=True)
	porcentaje_descuento_5 = models.IntegerField(blank=True, null=True)
	valor_descuento_1 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_descuento_2 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_descuento_3 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_descuento_4 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_descuento_5 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	iva_1 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	iva_2 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	iva_3 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	iva_4 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	iva_5 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	ico_1 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	ico_2 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	ico_3 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	ico_4 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	ico_5 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_total_1 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_total_2 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_total_3 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_total_4 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_total_5 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	iva_total = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	ico_total = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	reterenta = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	autoreterenta = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	reteiva = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	reteica = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	sub_total = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	total_impuestos = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	total_retenciones = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	total_documento = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	anticipo = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	saldo_pendiente = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	descripcion_1 = models.CharField(max_length=400, null=True, blank=True)
	descripcion_2 = models.CharField(max_length=400, null=True, blank=True)
	descripcion_3 = models.CharField(max_length=400, null=True, blank=True)
	descripcion_4 = models.CharField(max_length=400, null=True, blank=True)
	descripcion_5 = models.CharField(max_length=400, null=True, blank=True)
	descripcion_detallada = models.TextField(null=True, blank=True)
	observacion = models.CharField(max_length=200, null=True, blank=True)
	cifra_total_en_palabras = models.CharField(max_length=300,  null=True, blank=True)
	concepto_nota_debito = models.CharField(max_length=1, choices=choices.CONCEPTO_NOTA_DEBITO, null=True, blank=True)
	cargo_interes = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	descripcion_cargo = models.TextField(null=True, blank=True)
	saldo_total = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	generado = models.BooleanField(default=False)
	pagada = models.BooleanField(default=False)


	def auto_consecutivo(self):
		consecutivo = Consecutivo_documento.objects.get(org_creadora=self.org_creadora, tipo_de_documento="NDT", generado=True)
		doc_creados = Nota_debito.objects.filter(org_creadora=self.org_creadora, generado=True).count()
		ultimo_doc = Nota_debito.objects.filter(org_creadora=self.org_creadora, generado=True).last()
		self.tipo_de_documento = consecutivo.codigo
		if doc_creados == 0:
			self.consec_inter_prefijo = consecutivo.pre_fijo
			self.consec_inter_numero = consecutivo.numero
			self.consecutivo_interno = '%s %s'%(self.consec_inter_prefijo, self.consec_inter_numero)
			self.save()
		elif doc_creados > 0:
			nuevo_num = ultimo_doc.consec_inter_numero + 1
			self.consec_inter_prefijo = consecutivo.pre_fijo
			self.consec_inter_numero = nuevo_num
			self.consecutivo_interno = '%s %s'%(self.consec_inter_prefijo, self.consec_inter_numero)
			self.save()
	
	def __str__(self):
		self.save()
		return '%s %s %s'%(self.consecutivo_interno, self.cliente, self.fecha_emision)


class Factura_de_compra(models.Model):
	tipo_de_documento = models.CharField(max_length=100, null=True, blank=True)
	consecutivo_DIAN = models.CharField(max_length=100, null=True, blank=True)
	consecutivo_interno = models.CharField(max_length=100, null=True, blank=True)
	consec_inter_prefijo = models.CharField(max_length=3, null=True, blank=True)
	consec_inter_numero = models.PositiveIntegerField(null=True, blank=True)
	fecha_emision = models.DateTimeField(null=True, blank=True)
	tipo_imp1 = models.CharField(max_length=2, choices=choices.TIPO_IMPUESTO, null=True, blank=True)
	tipo_imp2 = models.CharField(max_length=2, choices=choices.TIPO_IMPUESTO, null=True, blank=True)
	tipo_imp3 = models.CharField(max_length=2, choices=choices.TIPO_IMPUESTO, null=True, blank=True)
	medio_de_pago = models.CharField(max_length=2, choices=choices.MEDIOS_DE_PAGO)
	moneda = models.CharField(max_length=3, choices=choices.MONEDAS, null=True, blank=True)
	comprador = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
	org_creadora = models.ForeignKey(Organizacion, on_delete=models.CASCADE, limit_choices_to={'activa':True}, null=True, blank=True)
	id_organizacion = models.CharField(max_length=50, null=True, blank=True)
	numero_id_organizacion = models.CharField(max_length=50, null=True, blank=True)
	numero_id_org_adicional = models.CharField(max_length=4, null=True, blank=True)
	dir_organizacion = models.CharField(max_length=50, null=True, blank=True)
	ciudad_organizacion = models.CharField(max_length=50, null=True, blank=True)
	departamento_organizacion = models.CharField(max_length=50, null=True, blank=True)
	pais_organizacion = models.CharField(max_length=50, null=True, blank=True)
	telefono_organizacion = models.CharField(max_length=50, null=True, blank=True)
	proveedor = models.CharField(max_length=300, null=True, blank=True)
	nombre_proveedor = models.CharField(max_length=50, null=True, blank=True)
	id_proveedor = models.CharField(max_length=50, null=True, blank=True)
	numero_id_proveedor = models.CharField(max_length=50, null=True, blank=True)
	numero_id_proveedor_adicional = models.CharField(max_length=4, null=True, blank=True)
	dir_proveedor = models.CharField(max_length=50, null=True, blank=True)
	ciudad_proveedor = models.CharField(max_length=50, null=True, blank=True)
	departamento_proveedor = models.CharField(max_length=50, null=True, blank=True)
	pais_proveedor = models.CharField(max_length=50, null=True, blank=True)
	telefono_proveedor = models.CharField(max_length=50, null=True, blank=True)
	item_1 = models.CharField(max_length=300, null=True, blank=True)
	item_2 = models.CharField(max_length=300, null=True, blank=True)
	item_3 = models.CharField(max_length=300, null=True, blank=True)
	item_4 = models.CharField(max_length=300, null=True, blank=True)
	item_5 = models.CharField(max_length=300, null=True, blank=True)
	cantidad_1 = models.IntegerField(blank=True, null=True)
	cantidad_2 = models.IntegerField(blank=True, null=True)
	cantidad_3 = models.IntegerField(blank=True, null=True)
	cantidad_4 = models.IntegerField(blank=True, null=True)
	cantidad_5 = models.IntegerField(blank=True, null=True)
	UM_1 = models.CharField(max_length=20, null=True, blank=True)
	UM_2 = models.CharField(max_length=20, null=True, blank=True)
	UM_3 = models.CharField(max_length=20, null=True, blank=True)
	UM_4 = models.CharField(max_length=20, null=True, blank=True)
	UM_5 = models.CharField(max_length=20, null=True, blank=True)
	valor_unitario_1 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_unitario_2 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_unitario_3 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_unitario_4 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_unitario_5 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	porcentaje_descuento_1 = models.IntegerField(blank=True, null=True)
	porcentaje_descuento_2 = models.IntegerField(blank=True, null=True)
	porcentaje_descuento_3 = models.IntegerField(blank=True, null=True)
	porcentaje_descuento_4 = models.IntegerField(blank=True, null=True)
	porcentaje_descuento_5 = models.IntegerField(blank=True, null=True)
	valor_descuento_1 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_descuento_2 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_descuento_3 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_descuento_4 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_descuento_5 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	iva_1 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	iva_2 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	iva_3 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	iva_4 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	iva_5 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	ico_1 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	ico_2 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	ico_3 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	ico_4 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	ico_5 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_total_1 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_total_2 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_total_3 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_total_4 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	valor_total_5 = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	iva_total = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	ico_total = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	reterenta = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	reteiva = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	reteica = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	sub_total = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	total_impuestos = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	total_retenciones = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	total_documento = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	anticipo = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	saldo_pendiente = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	descripcion_1 = models.CharField(max_length=400,  null=True, blank=True)
	descripcion_2 = models.CharField(max_length=400,  null=True, blank=True)
	descripcion_3 = models.CharField(max_length=400,  null=True, blank=True)
	descripcion_4 = models.CharField(max_length=400,  null=True, blank=True)
	descripcion_5 = models.CharField(max_length=400,  null=True, blank=True)
	descripcion_detallada = models.TextField(null=True, blank=True)
	observacion = models.CharField(max_length=200,  null=True, blank=True)
	cifra_total_en_palabras = models.CharField(max_length=300,  null=True, blank=True)
	generado = models.BooleanField(default=False)


	def auto_consecutivo(self):
		consecutivo = Consecutivo_documento.objects.get(org_creadora=self.org_creadora, tipo_de_documento="FCO", generado=True)
		doc_creados = Factura_de_compra.objects.filter(org_creadora=self.org_creadora, generado=True).count()
		ultimo_doc = Factura_de_compra.objects.filter(org_creadora=self.org_creadora, generado=True).last()
		self.tipo_de_documento = consecutivo.codigo
		if doc_creados == 0:
			self.consec_inter_prefijo = consecutivo.pre_fijo
			self.consec_inter_numero = consecutivo.numero
			self.consecutivo_interno = '%s %s'%(self.consec_inter_prefijo, self.consec_inter_numero)
			self.save()
		elif doc_creados > 0:
			nuevo_num = ultimo_doc.consec_inter_numero + 1
			self.consec_inter_prefijo = consecutivo.pre_fijo
			self.consec_inter_numero = nuevo_num
			self.consecutivo_interno = '%s %s'%(self.consec_inter_prefijo, self.consec_inter_numero)
			self.save()

	
	def auto_info_organizacion(self):
		self.id_organizacion = self.org_creadora.identificacion
		self.numero_id_organizacion = self.org_creadora.numero_identificacion
		self.numero_id_org_adicional = self.org_creadora.numero_id_adicional
		self.dir_organizacion = self.org_creadora.direccion
		self.ciudad_organizacion = self.org_creadora.ciudad
		self.departamento_organizacion = self.org_creadora.departamento
		self.pais_organizacion = self.org_creadora.pais
		self.telefono_organizacion = self.org_creadora.telefono
		self.moneda = self.org_creadora.moneda_base
		self.save()

	def auto_info_proveedor(self):
		proveedor = Contacto.objects.get(nombre_legal=self.proveedor, relacion_activa="PD", org_creadora=self.org_creadora)
		self.nombre_proveedor = proveedor.nombre_legal
		self.id_proveedor = proveedor.identificacion
		self.numero_id_proveedor = proveedor.numero_identificacion
		self.numero_id_proveedor_adicional = proveedor.numero_id_adicional
		self.dir_proveedor = proveedor.direccion
		self.ciudad_proveedor = proveedor.ciudad
		self.departamento_proveedor = proveedor.departamento
		self.pais_proveedor = proveedor.pais
		self.telefono_proveedor = proveedor.telefono
		self.save()

	def info_item(self):
		item_selecionados = [self.item_1, self.item_2, self.item_3, self.item_4, self.item_5]
		items_codes = []
		for item in item_selecionados:
			if item:
				item_doc = Insumo.objects.get(codigo=item, org_creadora=self.org_creadora)
				item_code = item_doc.codigo
				items_codes.append(item_code)
			else:
				items_codes.append(None)
		self.item_1_code = items_codes[0]
		self.item_2_code = items_codes[1]
		self.item_3_code = items_codes[2]
		self.item_4_code = items_codes[3]
		self.item_5_code = items_codes[4]
		self.save()

		descripciones = []
		for item in item_selecionados:
			if item:
				item_doc = Insumo.objects.get(codigo=item, org_creadora=self.org_creadora)
				descripcion = item_doc.descripcion
				descripciones.append(descripcion)
			else:
				descripciones.append(None)
		self.descripcion_1 = descripciones[0]
		self.descripcion_2 = descripciones[1]
		self.descripcion_3 = descripciones[2]
		self.descripcion_4 = descripciones[3]
		self.descripcion_5 = descripciones[4]
		self.save()

		if self.descripcion_detallada == 'No Registrado' or self.descripcion_detallada == '':
			descripciones_detalle = []
			for item in item_selecionados:
				if item:
					item_doc = Insumo.objects.get(codigo=item, org_creadora=self.org_creadora)
					if item_doc.descripcion_detalle:
						descripcion = '- %s\n' %(item_doc.descripcion_detalle)
						descripciones_detalle.append(descripcion)
			descrip_detail = ''
			for descripcion in descripciones_detalle:
				descrip_detail = descrip_detail + descripcion
			self.descripcion_detallada = descrip_detail

		unidadesmedida = []
		for item in item_selecionados:
			if item:
				item_doc = Insumo.objects.get(codigo=item, org_creadora=self.org_creadora)
				UM = item_doc.unidad_medida
				unidadesmedida.append(UM)
			else:
				unidadesmedida.append(None)
		self.UM_1 = unidadesmedida[0]
		self.UM_2 = unidadesmedida[1]
		self.UM_3 = unidadesmedida[2]
		self.UM_4 = unidadesmedida[3]
		self.UM_5 = unidadesmedida[4]
		self.save()

		valoresunitarios = []
		for item in item_selecionados:
			if item:
				item_doc = Insumo.objects.get(codigo=item, org_creadora=self.org_creadora)
				valor_unitario = item_doc.precio_compra
				valoresunitarios.append(valor_unitario)
			else:
				valoresunitarios.append(0)
		self.valor_unitario_1 = valoresunitarios[0]
		self.valor_unitario_2 = valoresunitarios[1]
		self.valor_unitario_3 = valoresunitarios[2]
		self.valor_unitario_4 = valoresunitarios[3]
		self.valor_unitario_5 = valoresunitarios[4]
		self.save()

	def calculo_item(self):
		item_selecionados = [self.item_1, self.item_2, self.item_3, self.item_4, self.item_5]
		valoresunitarios = []
		for item in item_selecionados:
			if item:
				item_doc = Insumo.objects.get(codigo=item, org_creadora=self.org_creadora)
				valor_unitario = item_doc.precio_compra
				valoresunitarios.append(valor_unitario)
			else:
				valoresunitarios.append(0)
		self.valor_unitario_1 = valoresunitarios[0]
		self.valor_unitario_2 = valoresunitarios[1]
		self.valor_unitario_3 = valoresunitarios[2]
		self.valor_unitario_4 = valoresunitarios[3]
		self.valor_unitario_5 = valoresunitarios[4]

		porcentajesdescuento = [self.porcentaje_descuento_1, self.porcentaje_descuento_2, self.porcentaje_descuento_3, self.porcentaje_descuento_4, self.porcentaje_descuento_5]
		cantidades = [self.cantidad_1, self.cantidad_2, self.cantidad_3, self.cantidad_4, self.cantidad_5]
		cantidades_nuevo = []
		for valor in cantidades:
			if valor == None:
				cantidades_nuevo.append(0)
			else:
				cantidades_nuevo.append(valor)
		self.cantidad_1 = cantidades_nuevo[0]
		self.cantidad_2 = cantidades_nuevo[1]
		self.cantidad_3 = cantidades_nuevo[2]
		self.cantidad_4 = cantidades_nuevo[3]
		self.cantidad_5 = cantidades_nuevo[4]

		porcentajesdescuento_nuevo = []
		for valor in porcentajesdescuento:
			if valor == None:
				porcentajesdescuento_nuevo.append(0)
			else:
				porcentajesdescuento_nuevo.append(valor)
		self.porcentaje_descuento_1 = porcentajesdescuento_nuevo[0]
		self.porcentaje_descuento_2 = porcentajesdescuento_nuevo[1]
		self.porcentaje_descuento_3 = porcentajesdescuento_nuevo[2]
		self.porcentaje_descuento_4 = porcentajesdescuento_nuevo[3]
		self.porcentaje_descuento_5 = porcentajesdescuento_nuevo[4]

		valoresdescuento = []
		indice = 0
		for valor in valoresunitarios:
			if cantidades_nuevo[indice] or porcentajesdescuento_nuevo[indice]:
				valordescuento = valor * cantidades_nuevo[indice] * porcentajesdescuento_nuevo[indice]/100
				valoresdescuento.append(valordescuento)
			else:
				valoresdescuento.append(0)
			indice += 1
		self.valor_descuento_1 = valoresdescuento[0]
		self.valor_descuento_2 = valoresdescuento[1]
		self.valor_descuento_3 = valoresdescuento[2]
		self.valor_descuento_4 = valoresdescuento[3]
		self.valor_descuento_5 = valoresdescuento[4]

		valorestotales = []
		indice = 0
		for valor in valoresunitarios:
			if cantidades[indice]:
				valortotal = valor * cantidades_nuevo[indice] - valoresdescuento[indice]
				valorestotales.append(valortotal)
			else:
				valorestotales.append(0)
			indice += 1
		self.valor_total_1 = valorestotales[0]
		self.valor_total_2 = valorestotales[1]
		self.valor_total_3 = valorestotales[2]
		self.valor_total_4 = valorestotales[3]
		self.valor_total_5 = valorestotales[4]
		self.sub_total = self.valor_total_1 + self.valor_total_2 + self.valor_total_3 + self.valor_total_4 + self.valor_total_5


		proveedor = Contacto.objects.get(nombre_legal=self.proveedor, relacion_activa="PD", org_creadora=self.org_creadora)
		if proveedor.responsable_iva == 'SI':
			numeros = ['1', '2', '3', '4']
			tarifas_de_iva = [19, 5, 0, 0]
			iva_item = []
			indice = 0
			for item in item_selecionados:
				if item:
					item_doc = Insumo.objects.get(codigo=item, org_creadora=self.org_creadora)
					if item_doc.iva_compras:
						tariva = 0
						for numero in numeros:
							if item_doc.iva_compras == numero:
								iva = float(valorestotales[indice]) * (tarifas_de_iva[tariva]/100)
								iva_item.append(int(iva))
							tariva += 1
				else:
					iva_item.append(0)
				indice += 1
			self.iva_1 = iva_item[0]
			self.iva_2 = iva_item[1]
			self.iva_3 = iva_item[2]
			self.iva_4 = iva_item[3]
			self.iva_5 = iva_item[4]
			self.iva_total = self.iva_1 + self.iva_2 + self.iva_3 + self.iva_4 + self.iva_5
			self.save()
		else:
			self.iva_total = 0
			self.save()


		numeros = ['1', '2', '3', '4']
		tarifas_de_ico = [16, 8, 4, 0]
		ico_item = []
		indice = 0
		for item in item_selecionados:
			if item:
				item_doc = Insumo.objects.get(codigo=item, org_creadora=self.org_creadora)
				if item_doc.impuesto_consumo_compras:
					tarico = 0
					for numero in numeros:
						if item_doc.impuesto_consumo_compras == numero:
							ico = float(valorestotales[indice]) * (tarifas_de_ico[tarico]/100)
							ico_item.append(int(ico))
						tarico += 1
			else:
				ico_item.append(0)
			indice += 1
		self.ico_1 = ico_item[0]
		self.ico_2 = ico_item[1]
		self.ico_3 = ico_item[2]
		self.ico_4 = ico_item[3]
		self.ico_5 = ico_item[4]
		self.ico_total = self.ico_1 + self.ico_2 + self.ico_3 + self.ico_4 + self.ico_5
		self.save()


		item_selecionados = [self.item_1, self.item_2, self.item_3, self.item_4, self.item_5]
		cantidades = [self.cantidad_1, self.cantidad_2, self.cantidad_3, self.cantidad_4, self.cantidad_5]
		indice = 0
		for item in item_selecionados:
			if item:
				item_doc = Insumo.objects.get(codigo=item, org_creadora=self.org_creadora)
				if item_doc.tipo_item == 'IN':
					if item_doc.cantidad == None:
						item_doc.cantidad = cantidades[indice]
						item_doc.save()
					else:
						item_doc.cantidad = item_doc.cantidad + cantidades[indice]
						item_doc.save()
			indice += 1


		if proveedor.compras_declarante_impuesto_renta == True or proveedor.compras_declarante_impuesto_renta == False:
			if self.org_creadora.compras_practicar_reterenta == True and proveedor.compras_exento_de_reterenta == False and proveedor.compras_autoretenedor_impuesto_renta == False:
				numeros = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16" ,"17", "18", "19", "20",
				"21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40",
				"41", "42", "43", "44", "45", "46", "47", "48"]
				bases = [0,961000,0,961000,0,0,0,0,0,0,0,0,0,0,142000,0,142000,0,142000,961000,0,142000,0,142000,0,142000,0,142000,0,0,
				961000,0,0,0,3276000,0,0,0,0,0,0,961000,0,0,5697000,0,0,0]
				tarifas_de_reterenta = [0,2.5,2.5,3.5,3.5,1,0.1,10,11,3.5,6,10,10,11,1,1,2,2,3.5,3.5,3.5,4,4,6,6,1,1,2,2,4,3.5,3.5,7,4,1.5,1.5,0.75,
				15,20,5,15,2,2,0.5,0.5,10,11,2.5]
				indice = 0
				reterentas = 0
				for numero in numeros:
					totalval = 0
					bases_retefuenterenta = 0
					for item in item_selecionados:
						if item:
							item_doc = Insumo.objects.get(codigo=item, org_creadora=self.org_creadora)
							if item_doc.tarifa_reterenta:
								if item_doc.tarifa_reterenta == numero:
									bases_retefuenterenta = bases_retefuenterenta + valorestotales[totalval]
						totalval = totalval + 1
					if bases_retefuenterenta > bases[indice]:
						reterentas = reterentas + (float(bases_retefuenterenta) * (tarifas_de_reterenta[indice]/100))
					indice = indice + 1
				self.reterenta = int(reterentas)
				self.autoreterenta = 0
				self.save()
			else:
				self.reterenta = 0
				self.autoreterenta = 0
				self.save()
		else:
			self.reterenta = 0
			self.autoreterenta = 0
			self.save()


		if self.org_creadora.compras_practicar_reteica == True:
			if self.org_creadora.ciudad == proveedor.ciudad:
				if proveedor.gran_contribuyente == True:
					self.reteica = 0
					self.save()
				elif proveedor.regimen_tributario == '2' or proveedor.regimen_tributario == '0':
					if self.org_creadora.regimen_tributario == '0':
						self.reteica = 0
						self.save()
					else:
						if self.org_creadora.tarifa_practicar_reteica == None:
							self.reteica = 0
							self.save()
						else:
							self.reteica = self.sub_total * (self.org_creadora.tarifa_practicar_reteica/1000)
							self.save()
				else:
					self.reteica = 0
					self.save()
			else:
				self.reteica = 0
				self.save()
		else:
			self.reteica = 0
			self.save()
	

		if self.org_creadora.gran_contribuyente == True:
			self.reteiva = int(self.iva_total * 0.15)
			self.save()
		elif self.org_creadora.compras_practicar_reteiva_proveedores_regimen_comun and self.org_creadora.gran_contribuyente == False and self.org_creadora.responsable_iva == 'SI':
			if proveedor.responsable_iva == 'SI' and proveedor.gran_contribuyente == False and proveedor.regimen_tributario == '2':
				self.reteiva = int(self.iva_total * 0.15)
				self.save()
			else:
				self.reteiva = 0
				self.save()
		elif self.org_creadora.compras_practicar_reteiva_proveedores_regimen_simple and self.org_creadora.regimen_tributario == '2' and self.org_creadora.responsable_iva == 'SI':
			if proveedor.responsable_iva == 'SI' and proveedor.regimen_tributario == '0':
				self.reteiva = int(self.iva_total * 0.15)
				self.save()
			else:
				self.reteiva = 0
				self.save()
		else:
			self.reteiva = 0
			self.save()


		if self.anticipo == None:
			self.anticipo = 0
			self.save()

	def calculo_total_factura(self):
		self.total_impuestos = self.iva_total + self.ico_total
		self.total_retenciones = self.reterenta + self.reteiva + self.reteica
		self.total_documento = self.sub_total + self.total_impuestos - self.total_retenciones
		self.saldo_pendiente = self.total_documento - self.anticipo
		self.save()

	def tipo_impuestodoc(self):
		if self.iva_total:
			self.tipo_imp1 = "01"
			self.save()
		if self.ico_total:
			self.tipo_imp2 = "02"
			self.save()
		if self.reteica:
			self.tipo_imp3 = "03"
			self.save()

	
	def __str__(self):
		self.save()
		return '%s %s %s'%(self.consecutivo_interno, self.proveedor, self.fecha_emision)



class Gastos_registro(models.Model):
	numero_gasto = models.IntegerField(null=True, blank=True, default=1)
	concepto_gasto = models.CharField(max_length=1, choices=choices.CONCEPTO_GASTO)
	descripcion_gasto = models.TextField(null=True, blank=True)
	valor_gasto = models.DecimalField(max_digits=11, decimal_places=2)
	fecha_emision = models.DateTimeField(null=True, blank=True)
	org_creadora = models.ForeignKey(Organizacion, on_delete=models.CASCADE, limit_choices_to={'activa':True}, null=True, blank=True)

	def auto_numero(self):
		gastos_creados = Gastos_registro.objects.filter(concepto_gasto=self.concepto_gasto).count()
		if gastos_creados == 0:
			self.numero_gasto = 1
			self.save()
		elif gastos_creados > 0:
			self.numero_gasto = gastos_creados
			self.save()

	def __str__(self):
		self.save()
		return '%s %s'%(self.concepto_gasto, self.numero_gasto)


class Crecimiento(models.Model):
	nombre = models.CharField(max_length=50, null=True, blank=True)
	metrica_crecimiento = models.CharField(max_length=1, choices=choices.METRICA_CRECIMIENTO, null=True, blank=True)
	fecha_creacion = models.DateTimeField(null=True, blank=True)
	fecha_inicio = models.DateField()
	fecha_fin = models.DateField(null=True, blank=True)
	tasa_crecimiento_diaria = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	tasa_crecimiento_semana = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	tasa_crecimiento_mensual = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	tasa_crecimiento_anual = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	ventas_dia = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	ventas_semana = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	ventas_mes = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	ventas_año = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	ventas_periodo = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	ganancias_dia = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	ganancias_semana = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	ganancias_mes = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	ganancias_año = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	ganancias_periodo = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
	org_creadora = models.ForeignKey(Organizacion, on_delete=models.CASCADE, limit_choices_to={'activa':True}, null=True, blank=True)
	guardada = models.BooleanField(default=False)
	mostrar = models.BooleanField(default=False)


	def calcular_reporte(self):
		locale.setlocale(locale.LC_ALL,'')
		if self.fecha_fin == None or self.fecha_fin == self.fecha_inicio:
			dia = self.fecha_inicio.day
			mes = self.fecha_inicio.month
			año = self.fecha_inicio.year
			desface_tiempo = timedelta(hours=5)
			inicio = datetime(año, mes, dia, 0, 0, 0, tzinfo=pytz.UTC)
			inicio = inicio + desface_tiempo
			fin = datetime(año, mes, dia, 23, 59, 59, tzinfo=pytz.UTC)
			fin = fin + desface_tiempo
			facturas = Factura_de_venta.objects.filter(fecha_pago__range=(inicio, fin), org_creadora=self.org_creadora, generado=True, anulada=False, pagada=True).order_by('fecha_emision')
			total_facturas = 0
			total_impuestos = 0
			for factura in facturas:
				venta = factura.total_documento
				total_facturas = total_facturas + venta
				total_impuestos = total_impuestos + factura.iva_total + factura.ico_total
			creditnotes_concep_1 = Nota_credito.objects.filter(fecha_pago__range=(inicio, fin), org_creadora=self.org_creadora, generado=True, pagada=True, concepto_nota_credito='1').order_by('fecha_emision')
			creditnotes_concep_3 = Nota_credito.objects.filter(fecha_pago__range=(inicio, fin), org_creadora=self.org_creadora, generado=True, pagada=True, concepto_nota_credito='3').order_by('fecha_emision')
			creditnotes_concep_4 = Nota_credito.objects.filter(fecha_pago__range=(inicio, fin), org_creadora=self.org_creadora, generado=True, pagada=True, concepto_nota_credito='4').order_by('fecha_emision')
			debitnotes = Nota_debito.objects.filter(fecha_pago__range=(inicio, fin), org_creadora=self.org_creadora, generado=True, pagada=True).order_by('fecha_emision')
			total_cn_1 = 0
			imp_cn_1 = 0
			for creditnote in creditnotes_concep_1:
				total = creditnote.total_documento
				total_cn_1 = total_cn_1 + total
				imp_cn_1 = imp_cn_1 + creditnote.iva_total + creditnote.ico_total
			total_cn_3 = 0
			imp_cn_3 = 0
			for creditnote in creditnotes_concep_3:
				total = creditnote.total_documento - creditnote.descuento_rebaja
				total_cn_3 = total_cn_3 + total
				imp_cn_3 = imp_cn_3 + creditnote.iva_total + creditnote.ico_total
			total_cn_4 = 0
			imp_cn_4 = 0
			for creditnote in creditnotes_concep_4:
				total = creditnote.total_documento - creditnote.descuento_rebaja
				total_cn_4 = total_cn_4 + total
				imp_cn_4 = imp_cn_4 + creditnote.iva_total + creditnote.ico_total
			total_dn = 0
			imp_dn = 0
			for debitnote in debitnotes:
				total = debitnote.total_documento + debitnote.cargo_interes
				total_dn = total_dn + total
				imp_dn = imp_dn + debitnote.iva_total + debitnote.ico_total
			facturas_comp = Factura_de_compra.objects.filter(fecha_emision__range=(inicio, fin), org_creadora=self.org_creadora, generado=True).order_by('fecha_emision')
			total_compras = 0
			for factura_c in facturas_comp:
				compra = factura_c.total_documento
				total_compras = total_compras + compra
			gastos = Gastos_registro.objects.filter(fecha_emision__range=(inicio, fin), org_creadora=self.org_creadora).order_by('fecha_emision')
			total_gastos = 0
			for gasto in gastos:
				gasto = gasto.valor_gasto
				total_gastos = total_gastos + gasto
			self.ventas_dia = total_facturas + total_cn_1 + total_cn_3 + total_cn_4 + total_dn
			self.ganancias_dia = total_facturas + total_cn_1 + total_cn_3 + total_cn_4 + total_dn - total_impuestos - imp_cn_1 - imp_cn_3 - imp_cn_4 - imp_dn - total_compras - total_gastos
			self.nombre = "Reporte " + self.fecha_inicio.strftime("%A %d %b %Y")
			self.save()
		else:
			dia_i = self.fecha_inicio.day
			mes_i = self.fecha_inicio.month
			año_i = self.fecha_inicio.year
			dia_f = self.fecha_fin.day
			mes_f = self.fecha_fin.month
			año_f = self.fecha_fin.year
			desface_tiempo = timedelta(hours=5)
			inicio = datetime(año_i, mes_i, dia_i, 0, 0, 0, tzinfo=pytz.UTC)
			inicio = inicio + desface_tiempo
			fin = datetime(año_f, mes_f, dia_f, 23, 59, 59, tzinfo=pytz.UTC)
			fin = fin + desface_tiempo
			periodo = fin - inicio
			semana = timedelta(days=7)
			mes = timedelta(days=30)
			año = timedelta(days=365)
			if periodo <= semana:
				dia_a_dia = timedelta(hours=24)
				inicio_dia = inicio
				fin_dia = inicio_dia + dia_a_dia
				ganancias = []
				ventas_dia = []
				while inicio_dia <= fin:
					facturas = Factura_de_venta.objects.filter(fecha_pago__range=(inicio_dia, fin_dia), org_creadora=self.org_creadora, generado=True, anulada=False, pagada=True).order_by('fecha_emision')
					total_facturas = 0
					total_impuestos = 0
					for factura in facturas:
						venta = factura.total_documento
						total_facturas = total_facturas + venta
						total_impuestos = total_impuestos + factura.iva_total + factura.ico_total
					creditnotes_concep_1 = Nota_credito.objects.filter(fecha_pago__range=(inicio_dia, fin_dia), org_creadora=self.org_creadora, generado=True, pagada=True, concepto_nota_credito='1').order_by('fecha_emision')
					creditnotes_concep_3 = Nota_credito.objects.filter(fecha_pago__range=(inicio_dia, fin_dia), org_creadora=self.org_creadora, generado=True, pagada=True, concepto_nota_credito='3').order_by('fecha_emision')
					creditnotes_concep_4 = Nota_credito.objects.filter(fecha_pago__range=(inicio_dia, fin_dia), org_creadora=self.org_creadora, generado=True, pagada=True, concepto_nota_credito='4').order_by('fecha_emision')
					debitnotes = Nota_debito.objects.filter(fecha_pago__range=(inicio_dia, fin_dia), org_creadora=self.org_creadora, generado=True, pagada=True).order_by('fecha_emision')
					total_cn_1 = 0
					imp_cn_1 = 0
					for creditnote in creditnotes_concep_1:
						total = creditnote.total_documento
						total_cn_1 = total_cn_1 + total
						imp_cn_1 = imp_cn_1 + creditnote.iva_total + creditnote.ico_total
					total_cn_3 = 0
					imp_cn_3 = 0
					for creditnote in creditnotes_concep_3:
						total = creditnote.total_documento - creditnote.descuento_rebaja
						total_cn_3 = total_cn_3 + total
						imp_cn_3 = imp_cn_3 + creditnote.iva_total + creditnote.ico_total
					total_cn_4 = 0
					imp_cn_4 = 0
					for creditnote in creditnotes_concep_4:
						total = creditnote.total_documento - creditnote.descuento_rebaja
						total_cn_4 = total_cn_4 + total
						imp_cn_4 = imp_cn_4 + creditnote.iva_total + creditnote.ico_total
					total_dn = 0
					imp_dn = 0
					for debitnote in debitnotes:
						total = debitnote.total_documento + debitnote.cargo_interes
						total_dn = total_dn + total
						imp_dn = imp_dn + debitnote.iva_total + debitnote.ico_total
					total_ventas = 0
					total_ventas = total_facturas + total_cn_1 + total_cn_3 + total_cn_4 + total_dn
					ventas_dia.append(total_ventas)
					facturas_comp = Factura_de_compra.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=self.org_creadora, generado=True).order_by('fecha_emision')
					total_compras = 0
					for factura_c in facturas_comp:
						compra = factura_c.total_documento
						total_compras = total_compras + compra
					gastos = Gastos_registro.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=self.org_creadora).order_by('fecha_emision')
					total_gastos = 0
					for gasto in gastos:
						gasto = gasto.valor_gasto
						total_gastos = total_gastos + gasto
					total_ganancias = 0
					total_ganancias = total_facturas + total_cn_1 + total_cn_3 + total_cn_4 + total_dn - total_impuestos - imp_cn_1 - imp_cn_3 - imp_cn_4 - imp_dn - total_compras - total_gastos
					ganancias.append(total_ganancias)
					inicio_dia = inicio_dia + dia_a_dia
					fin_dia = inicio_dia + dia_a_dia
				deltas = []
				indice = 1
				while indice < len(ventas_dia):
					if ventas_dia[indice] != 0 and ventas_dia[indice - 1] != 0:
						delta = ventas_dia[indice] - ventas_dia[indice - 1]
						porcentaje_crecimiento = (delta*100)/ventas_dia[indice - 1]
						deltas.append(porcentaje_crecimiento)
					elif ventas_dia[indice - 1] == 0 and deltas == []:
						deltas.append(100)
					elif ventas_dia[indice] == 0 and deltas == []:
						deltas.append(-100)
					indice = indice + 1
				total_ventas = 0
				for venta in ventas_dia:
					total_ventas = total_ventas + venta
				total_ganancias = 0
				for ganancia in ganancias:
					total_ganancias = total_ganancias + ganancia
				suma_crecimiento = 0
				for valor in deltas:
					suma_crecimiento = suma_crecimiento + valor
				self.ventas_semana = total_ventas
				self.ganancias_semana = total_ganancias
				dod = suma_crecimiento/len(deltas)
				self.tasa_crecimiento_diaria = dod
				self.nombre = "Reporte " + self.fecha_inicio.strftime("%d %b") + " al " + self.fecha_fin.strftime("%d %b %Y")
				self.save()

			elif periodo > semana and periodo <= mes:
				semana_a_semana = timedelta(days=7)
				inicio_dia = inicio
				fin_dia = inicio_dia + semana_a_semana
				ganancias = []
				ventas_semana = []
				while inicio_dia <= fin:
					facturas = Factura_de_venta.objects.filter(fecha_pago__range=(inicio_dia, fin_dia), org_creadora=self.org_creadora, generado=True, anulada=False, pagada=True).order_by('fecha_emision')
					total_facturas = 0
					total_impuestos = 0
					for factura in facturas:
						venta = factura.total_documento
						total_facturas = total_facturas + venta
						total_impuestos = total_impuestos + factura.iva_total + factura.ico_total
					creditnotes_concep_1 = Nota_credito.objects.filter(fecha_pago__range=(inicio_dia, fin_dia), org_creadora=self.org_creadora, generado=True, pagada=True, concepto_nota_credito='1').order_by('fecha_emision')
					creditnotes_concep_3 = Nota_credito.objects.filter(fecha_pago__range=(inicio_dia, fin_dia), org_creadora=self.org_creadora, generado=True, pagada=True, concepto_nota_credito='3').order_by('fecha_emision')
					creditnotes_concep_4 = Nota_credito.objects.filter(fecha_pago__range=(inicio_dia, fin_dia), org_creadora=self.org_creadora, generado=True, pagada=True, concepto_nota_credito='4').order_by('fecha_emision')
					debitnotes = Nota_debito.objects.filter(fecha_pago__range=(inicio_dia, fin_dia), org_creadora=self.org_creadora, generado=True, pagada=True).order_by('fecha_emision')
					total_cn_1 = 0
					imp_cn_1 = 0
					for creditnote in creditnotes_concep_1:
						total = creditnote.total_documento
						total_cn_1 = total_cn_1 + total
						imp_cn_1 = imp_cn_1 + creditnote.iva_total + creditnote.ico_total
					total_cn_3 = 0
					imp_cn_3 = 0
					for creditnote in creditnotes_concep_3:
						total = creditnote.total_documento - creditnote.descuento_rebaja
						total_cn_3 = total_cn_3 + total
						imp_cn_3 = imp_cn_3 + creditnote.iva_total + creditnote.ico_total
					total_cn_4 = 0
					imp_cn_4 = 0
					for creditnote in creditnotes_concep_4:
						total = creditnote.total_documento - creditnote.descuento_rebaja
						total_cn_4 = total_cn_4 + total
						imp_cn_4 = imp_cn_4 + creditnote.iva_total + creditnote.ico_total
					total_dn = 0
					imp_dn = 0
					for debitnote in debitnotes:
						total = debitnote.total_documento + debitnote.cargo_interes
						total_dn = total_dn + total
						imp_dn = imp_dn + debitnote.iva_total + debitnote.ico_total
					total_ventas = 0
					total_ventas = total_facturas + total_cn_1 + total_cn_3 + total_cn_4 + total_dn
					ventas_semana.append(total_ventas)
					facturas_comp = Factura_de_compra.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=self.org_creadora, generado=True).order_by('fecha_emision')
					total_compras = 0
					for factura_c in facturas_comp:
						compra = factura_c.total_documento
						total_compras = total_compras + compra
					gastos = Gastos_registro.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=self.org_creadora).order_by('fecha_emision')
					total_gastos = 0
					for gasto in gastos:
						gasto = gasto.valor_gasto
						total_gastos = total_gastos + gasto
					total_ganancias = 0
					total_ganancias = total_facturas + total_cn_1 + total_cn_3 + total_cn_4 + total_dn - total_impuestos - imp_cn_1 - imp_cn_3 - imp_cn_4 - imp_dn - total_compras - total_gastos
					ganancias.append(total_ganancias)
					inicio_dia = inicio_dia + semana_a_semana
					fin_dia = inicio_dia + semana_a_semana
				deltas = []
				indice = 1
				while indice < len(ventas_semana):
					if ventas_semana[indice] != 0 and ventas_semana[indice - 1] != 0:
						delta = ventas_semana[indice] - ventas_semana[indice - 1]
						porcentaje_crecimiento = (delta*100)/ventas_semana[indice - 1]
						deltas.append(porcentaje_crecimiento)
					elif ventas_semana[indice - 1] == 0 and deltas == []:
						deltas.append(100)
					elif ventas_semana[indice] == 0 and deltas == []:
						deltas.append(-100)
					indice = indice + 1
				total_ventas = 0
				for venta in ventas_semana:
					total_ventas = total_ventas + venta
				total_ganancias = 0
				for ganancia in ganancias:
					total_ganancias = total_ganancias + ganancia
				suma_crecimiento = 0
				for valor in deltas:
					suma_crecimiento = suma_crecimiento + valor
				self.ventas_mes = total_ventas
				self.ganancias_mes = total_ganancias
				wow = suma_crecimiento/len(deltas)
				self.tasa_crecimiento_semana = wow
				self.nombre = "Reporte " + self.fecha_inicio.strftime("%d %b") + " al " + self.fecha_fin.strftime("%d %b %Y")
				self.save()

			elif periodo > mes and periodo <= año:
				semana_a_semana = timedelta(days=7)
				inicio_dia = inicio
				fin_dia = inicio_dia + semana_a_semana
				ventas_semana = []
				while inicio_dia <= fin:
					facturas = Factura_de_venta.objects.filter(fecha_pago__range=(inicio_dia, fin_dia), org_creadora=self.org_creadora, generado=True, anulada=False, pagada=True).order_by('fecha_emision')
					total_facturas = 0
					for factura in facturas:
						venta = factura.total_documento
						total_facturas = total_facturas + venta
					creditnotes_concep_1 = Nota_credito.objects.filter(fecha_pago__range=(inicio_dia, fin_dia), org_creadora=self.org_creadora, generado=True, pagada=True, concepto_nota_credito='1').order_by('fecha_emision')
					creditnotes_concep_3 = Nota_credito.objects.filter(fecha_pago__range=(inicio_dia, fin_dia), org_creadora=self.org_creadora, generado=True, pagada=True,  concepto_nota_credito='3').order_by('fecha_emision')
					creditnotes_concep_4 = Nota_credito.objects.filter(fecha_pago__range=(inicio_dia, fin_dia), org_creadora=self.org_creadora, generado=True, pagada=True,  concepto_nota_credito='4').order_by('fecha_emision')
					debitnotes = Nota_debito.objects.filter(fecha_pago__range=(inicio_dia, fin_dia), org_creadora=self.org_creadora, generado=True, pagada=True).order_by('fecha_emision')
					total_cn_1 = 0
					imp_cn_1 = 0
					for creditnote in creditnotes_concep_1:
						total = creditnote.total_documento
						total_cn_1 = total_cn_1 + total
						imp_cn_1 = imp_cn_1 + creditnote.iva_total + creditnote.ico_total
					total_cn_3 = 0
					imp_cn_3 = 0
					for creditnote in creditnotes_concep_3:
						total = creditnote.total_documento - creditnote.descuento_rebaja
						total_cn_3 = total_cn_3 + total
						imp_cn_3 = imp_cn_3 + creditnote.iva_total + creditnote.ico_total
					total_cn_4 = 0
					imp_cn_4 = 0
					for creditnote in creditnotes_concep_4:
						total = creditnote.total_documento - creditnote.descuento_rebaja
						total_cn_4 = total_cn_4 + total
						imp_cn_4 = imp_cn_4 + creditnote.iva_total + creditnote.ico_total
					total_dn = 0
					imp_dn = 0
					for debitnote in debitnotes:
						total = debitnote.total_documento + debitnote.cargo_interes
						total_dn = total_dn + total
						imp_dn = imp_dn + debitnote.iva_total + debitnote.ico_total
					total_ventas = 0
					total_ventas = total_facturas + total_cn_1 + total_cn_3 + total_cn_4 + total_dn
					ventas_semana.append(total_ventas)
					inicio_dia = inicio_dia + semana_a_semana
					fin_dia = inicio_dia + semana_a_semana
				deltas_semana = []
				indice = 1
				while indice < len(ventas_semana):
					if ventas_semana[indice] != 0 and ventas_semana[indice - 1] != 0:
						delta = ventas_semana[indice] - ventas_semana[indice - 1]
						porcentaje_crecimiento = (delta*100)/ventas_semana[indice - 1]
						deltas_semana.append(porcentaje_crecimiento)
					elif ventas_semana[indice - 1] == 0 and deltas_semana == []:
						deltas_semana.append(100)
					elif ventas_semana[indice] == 0 and deltas_semana == []:
						deltas_semana.append(-100)
					indice = indice + 1
				total_ventas = 0
				for venta in ventas_semana:
					total_ventas = total_ventas + venta
				suma_crecimiento = 0
				for valor in deltas_semana:
					suma_crecimiento = suma_crecimiento + valor
				wow = suma_crecimiento/len(deltas_semana)
				self.tasa_crecimiento_semana = wow


				mes_a_mes = timedelta(days=30)
				inicio_dia = inicio
				fin_dia = inicio_dia + mes_a_mes
				ganancias = []
				ventas_mes = []
				while inicio_dia <= fin:
					facturas = Factura_de_venta.objects.filter(fecha_pago__range=(inicio_dia, fin_dia), org_creadora=self.org_creadora, generado=True, anulada=False, pagada=True).order_by('fecha_emision')
					total_facturas = 0
					total_impuestos = 0
					for factura in facturas:
						venta = factura.total_documento
						total_facturas = total_facturas + venta
						total_impuestos = total_impuestos + factura.iva_total + factura.ico_total
					creditnotes_concep_1 = Nota_credito.objects.filter(fecha_pago__range=(inicio_dia, fin_dia), org_creadora=self.org_creadora, generado=True, pagada=True, concepto_nota_credito='1').order_by('fecha_emision')
					creditnotes_concep_3 = Nota_credito.objects.filter(fecha_pago__range=(inicio_dia, fin_dia), org_creadora=self.org_creadora, generado=True, pagada=True, concepto_nota_credito='3').order_by('fecha_emision')
					creditnotes_concep_4 = Nota_credito.objects.filter(fecha_pago__range=(inicio_dia, fin_dia), org_creadora=self.org_creadora, generado=True, pagada=True, concepto_nota_credito='4').order_by('fecha_emision')
					debitnotes = Nota_debito.objects.filter(fecha_pago__range=(inicio_dia, fin_dia), org_creadora=self.org_creadora, generado=True, pagada=True).order_by('fecha_emision')
					total_cn_1 = 0
					imp_cn_1 = 0
					for creditnote in creditnotes_concep_1:
						total = creditnote.total_documento
						total_cn_1 = total_cn_1 + total
						imp_cn_1 = imp_cn_1 + creditnote.iva_total + creditnote.ico_total
					total_cn_3 = 0
					imp_cn_3 = 0
					for creditnote in creditnotes_concep_3:
						total = creditnote.total_documento - creditnote.descuento_rebaja
						total_cn_3 = total_cn_3 + total
						imp_cn_3 = imp_cn_3 + creditnote.iva_total + creditnote.ico_total
					total_cn_4 = 0
					imp_cn_4 = 0
					for creditnote in creditnotes_concep_4:
						total = creditnote.total_documento - creditnote.descuento_rebaja
						total_cn_4 = total_cn_4 + total
						imp_cn_4 = imp_cn_4 + creditnote.iva_total + creditnote.ico_total
					total_dn = 0
					imp_dn = 0
					for debitnote in debitnotes:
						total = debitnote.total_documento + debitnote.cargo_interes
						total_dn = total_dn + total
						imp_dn = imp_dn + debitnote.iva_total + debitnote.ico_total
					total_ventas = 0
					total_ventas = total_facturas + total_cn_1 + total_cn_3 + total_cn_4 + total_dn
					ventas_mes.append(total_ventas)
					facturas_comp = Factura_de_compra.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=self.org_creadora, generado=True).order_by('fecha_emision')
					total_compras = 0
					for factura_c in facturas_comp:
						compra = factura_c.total_documento
						total_compras = total_compras + compra
					gastos = Gastos_registro.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=self.org_creadora).order_by('fecha_emision')
					total_gastos = 0
					for gasto in gastos:
						gasto = gasto.valor_gasto
						total_gastos = total_gastos + gasto
					total_ganancias = 0
					total_ganancias = total_facturas + total_cn_1 + total_cn_3 + total_cn_4 + total_dn - total_impuestos - imp_cn_1 - imp_cn_3 - imp_cn_4 - imp_dn - total_compras - total_gastos
					ganancias.append(total_ganancias)
					inicio_dia = inicio_dia + mes_a_mes
					fin_dia = inicio_dia + mes_a_mes
				deltas = []
				indice = 1
				while indice < len(ventas_mes):
					if ventas_mes[indice] != 0 and ventas_mes[indice - 1] != 0:
						delta = ventas_mes[indice] - ventas_mes[indice - 1]
						porcentaje_crecimiento = (delta*100)/ventas_mes[indice - 1]
						deltas.append(porcentaje_crecimiento)
					elif ventas_mes[indice - 1] == 0 and deltas == []:
						deltas.append(100)
					elif ventas_mes[indice] == 0 and deltas == []:
						deltas.append(-100)
					indice = indice + 1
				total_ventas = 0
				for venta in ventas_mes:
					total_ventas = total_ventas + venta
				total_ganancias = 0
				for ganancia in ganancias:
					total_ganancias = total_ganancias + ganancia
				suma_crecimiento = 0
				for valor in deltas:
					suma_crecimiento = suma_crecimiento + valor
				self.ventas_año = total_ventas
				self.ganancias_año = total_ganancias
				mom = suma_crecimiento/len(deltas)
				self.tasa_crecimiento_mensual = mom
				self.nombre = "Reporte " + self.fecha_inicio.strftime("%d %b %Y") + " al " + self.fecha_fin.strftime("%d %b %Y")
				self.save()

			elif periodo > año:
				mes_a_mes = timedelta(days=30)
				inicio_dia = inicio
				fin_dia = inicio_dia + mes_a_mes
				ventas_mes = []
				while inicio_dia <= fin:
					facturas = Factura_de_venta.objects.filter(fecha_pago__range=(inicio_dia, fin_dia), org_creadora=self.org_creadora, generado=True, anulada=False, pagada=True).order_by('fecha_emision')
					total_facturas = 0
					for factura in facturas:
						venta = factura.total_documento
						total_facturas = total_facturas + venta
					creditnotes_concep_1 = Nota_credito.objects.filter(fecha_pago__range=(inicio_dia, fin_dia), org_creadora=self.org_creadora, generado=True, pagada=True, concepto_nota_credito='1').order_by('fecha_emision')
					creditnotes_concep_3 = Nota_credito.objects.filter(fecha_pago__range=(inicio_dia, fin_dia), org_creadora=self.org_creadora, generado=True, pagada=True, concepto_nota_credito='3').order_by('fecha_emision')
					creditnotes_concep_4 = Nota_credito.objects.filter(fecha_pago__range=(inicio_dia, fin_dia), org_creadora=self.org_creadora, generado=True, pagada=True, concepto_nota_credito='4').order_by('fecha_emision')
					debitnotes = Nota_debito.objects.filter(fecha_pago__range=(inicio_dia, fin_dia), org_creadora=self.org_creadora, generado=True, pagada=True).order_by('fecha_emision')
					total_cn_1 = 0
					imp_cn_1 = 0
					for creditnote in creditnotes_concep_1:
						total = creditnote.total_documento
						total_cn_1 = total_cn_1 + total
						imp_cn_1 = imp_cn_1 + creditnote.iva_total + creditnote.ico_total
					total_cn_3 = 0
					imp_cn_3 = 0
					for creditnote in creditnotes_concep_3:
						total = creditnote.total_documento - creditnote.descuento_rebaja
						total_cn_3 = total_cn_3 + total
						imp_cn_3 = imp_cn_3 + creditnote.iva_total + creditnote.ico_total
					total_cn_4 = 0
					imp_cn_4 = 0
					for creditnote in creditnotes_concep_4:
						total = creditnote.total_documento - creditnote.descuento_rebaja
						total_cn_4 = total_cn_4 + total
						imp_cn_4 = imp_cn_4 + creditnote.iva_total + creditnote.ico_total
					total_dn = 0
					imp_dn = 0
					for debitnote in debitnotes:
						total = debitnote.total_documento + debitnote.cargo_interes
						total_dn = total_dn + total
						imp_dn = imp_dn + debitnote.iva_total + debitnote.ico_total
					total_ventas = 0
					total_ventas = total_facturas + total_cn_1 + total_cn_3 + total_cn_4 + total_dn
					ventas_mes.append(total_ventas)
					inicio_dia = inicio_dia + mes_a_mes
					fin_dia = inicio_dia + mes_a_mes
				deltas_mes = []
				indice = 1
				while indice < len(ventas_mes):
					if ventas_mes[indice] != 0 and ventas_mes[indice - 1] != 0:
						delta = ventas_mes[indice] - ventas_mes[indice - 1]
						porcentaje_crecimiento = (delta*100)/ventas_mes[indice - 1]
						deltas_mes.append(porcentaje_crecimiento)
					elif ventas_mes[indice - 1] == 0 and deltas_mes == []:
						deltas_mes.append(100)
					elif ventas_mes[indice] == 0 and deltas_mes == []:
						deltas_mes.append(-100)
					indice = indice + 1
				total_ventas = 0
				for venta in ventas_mes:
					total_ventas = total_ventas + venta
				suma_crecimiento = 0
				for valor in deltas_mes:
					suma_crecimiento = suma_crecimiento + valor
				self.ventas_año = total_ventas
				mom = suma_crecimiento/len(deltas_mes)
				self.tasa_crecimiento_mensual = mom

				año_a_año = timedelta(days=365)
				inicio_dia = inicio
				fin_dia = inicio_dia + año_a_año
				ganancias = []
				ventas_año = []
				while inicio_dia <= fin:
					facturas = Factura_de_venta.objects.filter(fecha_pago__range=(inicio_dia, fin_dia), org_creadora=self.org_creadora, generado=True, anulada=False, pagada=True).order_by('fecha_emision')
					total_facturas = 0
					total_impuestos = 0
					for factura in facturas:
						venta = factura.total_documento
						total_facturas = total_facturas + venta
						total_impuestos = total_impuestos + factura.iva_total + factura.ico_total
					creditnotes_concep_1 = Nota_credito.objects.filter(fecha_pago__range=(inicio_dia, fin_dia), org_creadora=self.org_creadora, generado=True, pagada=True, concepto_nota_credito='1').order_by('fecha_emision')
					creditnotes_concep_3 = Nota_credito.objects.filter(fecha_pago__range=(inicio_dia, fin_dia), org_creadora=self.org_creadora, generado=True, pagada=True, concepto_nota_credito='3').order_by('fecha_emision')
					creditnotes_concep_4 = Nota_credito.objects.filter(fecha_pago__range=(inicio_dia, fin_dia), org_creadora=self.org_creadora, generado=True, pagada=True, concepto_nota_credito='4').order_by('fecha_emision')
					debitnotes = Nota_debito.objects.filter(fecha_pago__range=(inicio_dia, fin_dia), org_creadora=self.org_creadora, generado=True, pagada=True).order_by('fecha_emision')
					total_cn_1 = 0
					imp_cn_1 = 0
					for creditnote in creditnotes_concep_1:
						total = creditnote.total_documento
						total_cn_1 = total_cn_1 + total
						imp_cn_1 = imp_cn_1 + creditnote.iva_total + creditnote.ico_total
					total_cn_3 = 0
					imp_cn_3 = 0
					for creditnote in creditnotes_concep_3:
						total = creditnote.total_documento - creditnote.descuento_rebaja
						total_cn_3 = total_cn_3 + total
						imp_cn_3 = imp_cn_3 + creditnote.iva_total + creditnote.ico_total
					total_cn_4 = 0
					imp_cn_4 = 0
					for creditnote in creditnotes_concep_4:
						total = creditnote.total_documento - creditnote.descuento_rebaja
						total_cn_4 = total_cn_4 + total
						imp_cn_4 = imp_cn_4 + creditnote.iva_total + creditnote.ico_total
					total_dn = 0
					imp_dn = 0
					for debitnote in debitnotes:
						total = debitnote.total_documento + debitnote.cargo_interes
						total_dn = total_dn + total
						imp_dn = imp_dn + debitnote.iva_total + debitnote.ico_total
					total_ventas = 0
					total_ventas = total_facturas + total_cn_1 + total_cn_3 + total_cn_4 + total_dn
					ventas_año.append(total_ventas)
					facturas_comp = Factura_de_compra.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=self.org_creadora, generado=True).order_by('fecha_emision')
					total_compras = 0
					for factura_c in facturas_comp:
						compra = factura_c.total_documento
						total_compras = total_compras + compra
					gastos = Gastos_registro.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=self.org_creadora).order_by('fecha_emision')
					total_gastos = 0
					for gasto in gastos:
						gasto = gasto.valor_gasto
						total_gastos = total_gastos + gasto
					total_ganancias = 0
					total_ganancias = total_facturas + total_cn_1 + total_cn_3 + total_cn_4 + total_dn - total_impuestos - imp_cn_1 - imp_cn_3 - imp_cn_4 - imp_dn - total_compras - total_gastos
					ganancias.append(total_ganancias)
					inicio_dia = inicio_dia + año_a_año
					fin_dia = inicio_dia + año_a_año
				deltas = []
				indice = 1
				while indice < len(ventas_año):
					if ventas_año[indice] != 0 and ventas_año[indice - 1] != 0:
						delta = ventas_año[indice] - ventas_año[indice - 1]
						porcentaje_crecimiento = (delta*100)/ventas_año[indice - 1]
						deltas.append(porcentaje_crecimiento)
					elif ventas_año[indice - 1] == 0 and deltas == []:
						deltas.append(100)
					elif ventas_año[indice] == 0 and deltas == []:
						deltas.append(-100)
					indice = indice + 1
				total_ventas = 0
				for venta in ventas_año:
					total_ventas = total_ventas + venta
				total_ganancias = 0
				for ganancia in ganancias:
					total_ganancias = total_ganancias + ganancia
				suma_crecimiento = 0
				for valor in deltas:
					suma_crecimiento = suma_crecimiento + valor
				self.ventas_periodo = total_ventas
				self.ganancias_periodo = total_ganancias
				yoy = suma_crecimiento/len(deltas)
				self.tasa_crecimiento_anual = yoy
				self.nombre = "Reporte " + self.fecha_inicio.strftime("%d %b %Y") + " al " + self.fecha_fin.strftime("%d %b %Y")
				self.save()

	def __str__(self):
		self.save()
		return self.nombre