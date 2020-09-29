from django import forms
from .models import Organizacion, Contacto, Categoria, Item, Insumo, Termino_de_pago, Consecutivo_documento, Cotizacion, Remision, Factura_de_venta, Nota_credito, Nota_debito, Factura_de_compra, Gastos_registro, Crecimiento

class OrganizacionForm(forms.ModelForm):
	class Meta:
		model = Organizacion
		fields = ("nombre_legal","identificacion","numero_identificacion","numero_id_adicional","activad_economica","codigo_actividad_economica",
			"descripcion","logo_organizacion","nombre_visible_cia","moneda_base","direccion","ciudad","departamento","pais","cod_postal","persona_contacto",
			"telefono","telefono_dos","email","website","numero_cuenta","tipo_cuenta","entidad_financiera","regimen_tributario","responsable_iva",
			"gran_contribuyente","declarante_impuesto_renta","compras_practicar_reterenta","compras_practicar_reteiva_proveedores_regimen_comun",
			"compras_practicar_reteiva_proveedores_regimen_simple","compras_practicar_reteica","tarifa_practicar_reteica","ventas_liquidar_reterenta",
			"ventas_liquidar_autoretencion_renta","tarifa_autoreterenta","ventas_liquidar_autorreterenta_clientes_regimen_simple","ventas_liquidar_reteica",
			"tarifa_liquidar_reteica","administrador","activa")
		widgets = {
			'codigo_actividad_economica': forms.TextInput(attrs={'placeholder': 'Código'}),
            'ciudad': forms.TextInput(attrs={'placeholder': 'Ciudad'}),
            'departamento': forms.TextInput(attrs={'placeholder': 'Departamento'}),
            'tarifa_practicar_reteica': forms.NumberInput(attrs={'placeholder': 'Tarifa Reteica (Por Mil)'}),
            'tarifa_liquidar_reteica': forms.NumberInput(attrs={'placeholder': 'Tarifa Reteica (Por Mil)'}),
            }
            
class ContactoForm(forms.ModelForm):
	class Meta:
		model = Contacto
		fields = ("naturaleza","identificacion","numero_identificacion","numero_id_adicional","nombre_legal","activad_economica",
			"codigo_actividad_economica","relacion_activa","consumidor_final","regimen_tributario","responsable_iva","gran_contribuyente",
			"ventas_liquidar_reteiva_responsable_iva_regimen_comun","ventas_liquidar_reteiva_responsable_iva_regimen_simple","ventas_liquidar_reterenta",
			"ventas_liquidar_reteica","compras_declarante_impuesto_renta","compras_autoretenedor_impuesto_renta","compras_exento_de_reterenta",
			"direccion","ciudad","departamento","pais","cod_postal","persona_contacto","persona_contacto_adicional","telefono","telefono_dos",
			"email","numero_cuenta","tipo_cuenta","entidad_financiera","org_creadora")
		widgets = {
            'ciudad': forms.TextInput(attrs={'placeholder': 'Ciudad'}),
            'departamento': forms.TextInput(attrs={'placeholder': 'Departamento'}),
            'codigo_actividad_economica': forms.TextInput(attrs={'placeholder': 'Código'}),
            }

class InsumoForm(forms.ModelForm):
	class Meta:
		model = Insumo
		fields =("imagen","categoria","codigo","tipo_item","descripcion","descripcion_detalle","codigo_barras","unidad_medida",
			"precio_compra","iva_compras","impuesto_consumo_compras","tarifa_reterenta","cantidad","org_creadora")
		
class ItemForm(forms.ModelForm):
	class Meta:
		model = Item
		fields = ("imagen","categoria","codigo","tipo_item","descripcion","descripcion_detalle","codigo_barras","unidad_medida",
			"precio_venta","iva_ventas","impuesto_consumo_ventas","tarifa_reterenta","cantidad","org_creadora")

class CategoriaForm(forms.ModelForm):
	class Meta:
		model = Categoria
		fields = ("destino_item","pre_fijo","numero","nombre","descripcion","org_creadora")

class Consecutivo_documentoForm(forms.ModelForm):
	class Meta:
		model = Consecutivo_documento
		fields = ("tipo_de_documento","pre_fijo","numero","aut_num_facturacion","num_inicio","num_final","fecha_inicio","fecha_fin","fecha_inicio_format","fecha_fin_format","codigo","org_creadora","generado")
		widgets = {'fecha_inicio': forms.TextInput(attrs={'placeholder': 'DD/MM/AAAA', 'class':'datepicker'}),
		'fecha_fin': forms.TextInput(attrs={'placeholder': 'DD/MM/AAAA', 'class':'datepicker'}),
		}
class Termino_de_pagoForm(forms.ModelForm):
	class Meta:
		model = Termino_de_pago
		fields = ("codigo","descripcion","plazo_dias","org_creadora")
		widgets = {'plazo_dias': forms.TextInput(attrs={'placeholder': 'Días'}),
		'descripcion': forms.TextInput(attrs={'placeholder': 'p.ej. Crédito a 30 Días'})}

class CotizacionForm(forms.ModelForm):
	class Meta:
		model = Cotizacion
		fields = ("consec_inter_prefijo","consec_inter_numero","consecutivo_interno","referencia_orden_compra","referencia_remision","referencia_factura","referencia_otro_documento","fecha_emision","tipo_imp1","tipo_imp2","tipo_imp3",
			"terminos_de_pago","medio_de_pago","moneda","vendedor","org_creadora","id_organizacion","numero_id_organizacion","numero_id_org_adicional","dir_organizacion","ciudad_organizacion","departamento_organizacion","pais_organizacion",
			"telefono_organizacion","cliente","nombre_cliente","id_cliente","numero_id_cliente","numero_id_cli_adicional","dir_cliente","ciudad_cliente","departamento_cliente","pais_cliente","telefono_cliente","item_1","item_2","item_3","item_4", "item_5",
			"cantidad_1","cantidad_2","cantidad_3","cantidad_4","cantidad_5","UM_1","UM_2","UM_3","UM_4","UM_5","valor_unitario_1","valor_unitario_2","valor_unitario_3","valor_unitario_4","valor_unitario_5",
			"porcentaje_descuento_1","porcentaje_descuento_2","porcentaje_descuento_3","porcentaje_descuento_4","porcentaje_descuento_5","valor_descuento_1","valor_descuento_2",
			"valor_descuento_3","valor_descuento_4","valor_descuento_5","iva_1","iva_2","iva_3","iva_4","iva_5","ico_1","ico_2","ico_3","ico_4","ico_5","valor_total_1","valor_total_2","valor_total_3",
			"valor_total_4","valor_total_5","iva_total","ico_total","reterenta","autoreterenta","reteiva","reteica","sub_total","total_impuestos","total_retenciones","total_documento","descripcion_1","descripcion_2","descripcion_3",
			"descripcion_4","descripcion_5","descripcion_detallada","observacion","cifra_total_en_palabras","anticipo","saldo_pendiente","generado")
		widgets = {'referencia_orden_compra': forms.TextInput(attrs={'placeholder': 'Número'}),
		'referencia_otro_documento': forms.TextInput(attrs={'placeholder': 'Documento: Número'}),
		}

class RemisionForm(forms.ModelForm):
	class Meta:
		model = Remision
		fields = ("consec_inter_prefijo","consec_inter_numero","consecutivo_interno","referencia_orden_compra","referencia_cotizacion","referencia_factura","referencia_otro_documento","fecha_emision","vendedor","org_creadora","id_organizacion","numero_id_organizacion","numero_id_org_adicional",
			"dir_organizacion","ciudad_organizacion","departamento_organizacion","pais_organizacion","telefono_organizacion","cliente","nombre_cliente","id_cliente","numero_id_cliente","numero_id_cli_adicional","dir_cliente","ciudad_cliente","departamento_cliente",
			"pais_cliente","telefono_cliente","item_1","item_2","item_3","item_4", "item_5","cantidad_1","cantidad_2","cantidad_3","cantidad_4","cantidad_5","UM_1","UM_2","UM_3","UM_4","UM_5","descripcion_1","descripcion_2","descripcion_3",
			"descripcion_4","descripcion_5","descripcion_detallada","observacion","datos_transportador","generado")


class Factura_de_ventaForm(forms.ModelForm):
	class Meta:
		model = Factura_de_venta
		fields = ("tipo_de_documento","consecutivo_DIAN","consec_inter_prefijo","consec_inter_numero","consecutivo_interno","referencia_orden_compra","referencia_remision","referencia_cotizacion","referencia_notacredito","referencia_notadebito","referencia_otro_documento","fecha_para_consec","fecha_emision",
			"fecha_vencimiento","fecha_pago","tipo_imp1","tipo_imp2","tipo_imp3","terminos_de_pago","medio_de_pago","moneda","vendedor","org_creadora","id_organizacion","numero_id_organizacion","numero_id_org_adicional","dir_organizacion","ciudad_organizacion","departamento_organizacion","pais_organizacion",
			"telefono_organizacion","cliente","nombre_cliente","id_cliente","numero_id_cliente","numero_id_cli_adicional","dir_cliente","ciudad_cliente","departamento_cliente","pais_cliente","telefono_cliente","item_1","item_2","item_3","item_4", "item_5",
			"cantidad_1","cantidad_2","cantidad_3","cantidad_4","cantidad_5","UM_1","UM_2","UM_3","UM_4","UM_5","valor_unitario_1","valor_unitario_2","valor_unitario_3","valor_unitario_4","valor_unitario_5",
			"porcentaje_descuento_1","porcentaje_descuento_2","porcentaje_descuento_3","porcentaje_descuento_4","porcentaje_descuento_5","valor_descuento_1","valor_descuento_2",
			"valor_descuento_3","valor_descuento_4","valor_descuento_5","iva_1","iva_2","iva_3","iva_4","iva_5","ico_1","ico_2","ico_3","ico_4","ico_5","valor_total_1","valor_total_2","valor_total_3",
			"valor_total_4","valor_total_5","iva_total","ico_total","reterenta","autoreterenta","reteiva","reteica","sub_total","total_impuestos","total_retenciones","total_documento","descripcion_1","descripcion_2","descripcion_3",
			"descripcion_4","descripcion_5","descripcion_detallada","observacion","cifra_total_en_palabras","anticipo","saldo_pendiente","generado","anulada","pagada")
		widgets = {'referencia_orden_compra': forms.TextInput(attrs={'placeholder': 'Número'}),
		'referencia_otro_documento': forms.TextInput(attrs={'placeholder': 'Documento: Número'}),
		}

class Nota_creditoForm(forms.ModelForm):
	class Meta:
		model = Nota_credito
		fields = ("tipo_de_documento","consecutivo_DIAN","consec_inter_prefijo","consec_inter_numero","consecutivo_interno","referencia_factura","referencia_factura_DIAN","referencia_orden_compra","referencia_remision","referencia_cotizacion","referencia_otro_documento",
			"fecha_emision","fecha_pago","fecha_emision_factura","tipo_imp1","tipo_imp2","tipo_imp3","terminos_de_pago","medio_de_pago","moneda","vendedor","org_creadora","id_organizacion","numero_id_organizacion","numero_id_org_adicional","dir_organizacion","ciudad_organizacion",
			"departamento_organizacion","pais_organizacion","telefono_organizacion","cliente","nombre_cliente","id_cliente","numero_id_cliente","numero_id_cli_adicional","dir_cliente","ciudad_cliente","departamento_cliente","pais_cliente","telefono_cliente","item_1","item_2","item_3","item_4", "item_5",
			"cantidad_1","cantidad_2","cantidad_3","cantidad_4","cantidad_5","UM_1","UM_2","UM_3","UM_4","UM_5","valor_unitario_1","valor_unitario_2","valor_unitario_3","valor_unitario_4","valor_unitario_5",
			"porcentaje_descuento_1","porcentaje_descuento_2","porcentaje_descuento_3","porcentaje_descuento_4","porcentaje_descuento_5","valor_descuento_1","valor_descuento_2",
			"valor_descuento_3","valor_descuento_4","valor_descuento_5","iva_1","iva_2","iva_3","iva_4","iva_5","ico_1","ico_2","ico_3","ico_4","ico_5","valor_total_1","valor_total_2","valor_total_3",
			"valor_total_4","valor_total_5","iva_total","ico_total","reterenta","autoreterenta","reteiva","reteica","sub_total","total_impuestos","total_retenciones","total_documento","descripcion_1","descripcion_2","descripcion_3",
			"descripcion_4","descripcion_5","descripcion_detallada","observacion","cifra_total_en_palabras","anticipo","saldo_pendiente","concepto_nota_credito","item_1_afec","item_2_afec","item_3_afec","item_4_afec","item_5_afec","descuento_rebaja","saldo_total","generado","pagada")

class Nota_debitoForm(forms.ModelForm):
	class Meta:
		model = Nota_debito
		fields = ("tipo_de_documento","consecutivo_DIAN","consec_inter_prefijo","consec_inter_numero","consecutivo_interno","referencia_factura","referencia_factura_DIAN","referencia_orden_compra","referencia_remision","referencia_cotizacion","referencia_otro_documento",
			"fecha_emision","fecha_pago","fecha_emision_factura","tipo_imp1","tipo_imp2","tipo_imp3","terminos_de_pago","medio_de_pago","moneda","vendedor","org_creadora","id_organizacion","numero_id_organizacion","numero_id_org_adicional","dir_organizacion","ciudad_organizacion",
			"departamento_organizacion","pais_organizacion","telefono_organizacion","cliente","nombre_cliente","id_cliente","numero_id_cliente","numero_id_cli_adicional","dir_cliente","ciudad_cliente","departamento_cliente","pais_cliente","telefono_cliente","item_1","item_2","item_3","item_4", "item_5",
			"cantidad_1","cantidad_2","cantidad_3","cantidad_4","cantidad_5","UM_1","UM_2","UM_3","UM_4","UM_5","valor_unitario_1","valor_unitario_2","valor_unitario_3","valor_unitario_4","valor_unitario_5",
			"porcentaje_descuento_1","porcentaje_descuento_2","porcentaje_descuento_3","porcentaje_descuento_4","porcentaje_descuento_5","valor_descuento_1","valor_descuento_2",
			"valor_descuento_3","valor_descuento_4","valor_descuento_5","iva_1","iva_2","iva_3","iva_4","iva_5","ico_1","ico_2","ico_3","ico_4","ico_5","valor_total_1","valor_total_2","valor_total_3",
			"valor_total_4","valor_total_5","iva_total","ico_total","reterenta","autoreterenta","reteiva","reteica","sub_total","total_impuestos","total_retenciones","total_documento","descripcion_1","descripcion_2","descripcion_3",
			"descripcion_4","descripcion_5","descripcion_detallada","observacion","cifra_total_en_palabras","anticipo","saldo_pendiente","concepto_nota_debito","cargo_interes","descripcion_cargo","saldo_total","generado","pagada")

class Factura_de_compraForm(forms.ModelForm):
	class Meta:
		model = Factura_de_compra
		fields = ("tipo_de_documento","consecutivo_DIAN","consec_inter_prefijo","consec_inter_numero","consecutivo_interno","fecha_emision","tipo_imp1","tipo_imp2","tipo_imp3",
			"medio_de_pago","moneda","comprador","org_creadora","id_organizacion","numero_id_organizacion","numero_id_org_adicional","dir_organizacion","ciudad_organizacion","departamento_organizacion","pais_organizacion",
			"telefono_organizacion","proveedor","nombre_proveedor","id_proveedor","numero_id_proveedor","numero_id_proveedor_adicional","dir_proveedor","ciudad_proveedor","departamento_proveedor","pais_proveedor","telefono_proveedor","item_1","item_2","item_3","item_4", "item_5",
			"cantidad_1","cantidad_2","cantidad_3","cantidad_4","cantidad_5","UM_1","UM_2","UM_3","UM_4","UM_5","valor_unitario_1","valor_unitario_2","valor_unitario_3","valor_unitario_4","valor_unitario_5",
			"porcentaje_descuento_1","porcentaje_descuento_2","porcentaje_descuento_3","porcentaje_descuento_4","porcentaje_descuento_5","valor_descuento_1","valor_descuento_2",
			"valor_descuento_3","valor_descuento_4","valor_descuento_5","iva_1","iva_2","iva_3","iva_4","iva_5","ico_1","ico_2","ico_3","ico_4","ico_5","valor_total_1","valor_total_2","valor_total_3",
			"valor_total_4","valor_total_5","iva_total","ico_total","reterenta","reteiva","reteica","sub_total","total_impuestos","total_retenciones","total_documento","descripcion_1","descripcion_2","descripcion_3",
			"descripcion_4","descripcion_5","descripcion_detallada","observacion","cifra_total_en_palabras","anticipo","saldo_pendiente","generado")

class Gastos_registroForm(forms.ModelForm):
	class Meta:
		model = Gastos_registro
		fields = ("numero_gasto","concepto_gasto","descripcion_gasto","valor_gasto","fecha_emision","org_creadora")

class CrecimientoForm(forms.ModelForm):
	class Meta:
		model = Crecimiento
		fields = ("nombre","metrica_crecimiento","fecha_creacion","fecha_inicio","fecha_fin","tasa_crecimiento_diaria","tasa_crecimiento_semana","tasa_crecimiento_mensual","tasa_crecimiento_anual","ventas_dia","ventas_semana","ventas_mes","ventas_año","ventas_periodo","ganancias_dia","ganancias_semana","ganancias_mes","ganancias_año","ganancias_periodo","org_creadora","guardada","mostrar")
		widgets = {'fecha_inicio': forms.TextInput(attrs={'placeholder': 'dd/mm/aaaa'}),
		'fecha_fin': forms.TextInput(attrs={'placeholder': 'dd/mm/aaaa'}),
		}