import os
import io
import math
import pytz
import locale
import numpy as np
from decimal import *
from django.conf import settings
from datetime import date
from datetime import datetime
from datetime import timedelta
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from django.conf import settings
from io import BytesIO, StringIO
from xhtml2pdf import pisa
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import OrganizacionForm, Consecutivo_documentoForm, Termino_de_pagoForm, CotizacionForm, RemisionForm, Factura_de_ventaForm, Nota_creditoForm, Nota_debitoForm, Factura_de_compraForm, ContactoForm, ItemForm, InsumoForm, CategoriaForm, CrecimientoForm, Gastos_registroForm
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Organizacion, Consecutivo_documento, Termino_de_pago, Factura_de_venta, Nota_credito, Nota_debito, Cotizacion, Remision, Factura_de_compra, Contacto, Categoria, Item, Insumo, Crecimiento, Gastos_registro
from .models import DOCUMENTOS_IDENTIDAD, REGIMEN_TRIBUTARIO,NATURALEZA,RELACIONES,TIPO_CUENTA,UNIDADES_MEDIDA,TIPO_ITEM,TIPO_DE_DOCUMENTO,MONEDAS,MEDIOS_DE_PAGO,TIPO_IMPUESTO,CONCEPTO_NOTA_DEBITO,CONCEPTO_NOTA_CREDITO,DESTINO_ITEM,METRICA_CRECIMIENTO,CONCEPTO_GASTO,PAISES
from django.http import HttpResponse
from django.views.generic import View
from django.template.loader import get_template

# Funciones útiles para las vistas


def moneyfmt(value, places=2, curr='', sep=',', dp='.', pos='', neg='-', trailneg=''):
    q = Decimal(10) ** -places      # 2 places --> '0.01'
    sign, digits, exp = value.quantize(q).as_tuple()
    result = []
    digits = list(map(str, digits))
    build, next = result.append, digits.pop
    if sign:
        build(trailneg)
    for i in range(places):
        build(next() if digits else '0')
    if places:
        build(dp)
    if not digits:
        build('0')
    i = 0
    while digits:
        build(next())
        i += 1
        if i == 3 and digits:
            i = 0
            build(sep)
    build(curr)
    build(neg if sign else pos)
    return ''.join(reversed(result))

def reemplazardatos_organizacion(objeto):
	if objeto.persona_contacto == None:
		objeto.persona_contacto = "No Registrado"
	if objeto.cod_postal == None:
		objeto.cod_postal = "No Registrado"
	if objeto.telefono_dos == None:
		objeto.telefono_dos = "No Registrado"
	if objeto.email == None:
		objeto.email = "No Registrado"
	if objeto.website == None:
		objeto.website = "No Registrado"
	if objeto.descripcion == None or objeto.descripcion == "":
		objeto.descripcion = "No Registrado"
	if objeto.numero_cuenta == None:
		objeto.numero_cuenta = "No Registrado"
	if objeto.tipo_cuenta == None:
		objeto.tipo_cuenta = "No Registrado"
	if objeto.entidad_financiera == None:
		objeto.entidad_financiera = "No Registrado"
	if objeto.gran_contribuyente == True:
		objeto.gran_contribuyente = "Aplica"
	else:
		objeto.gran_contribuyente = "No Aplica"
	if objeto.declarante_impuesto_renta == True:
		objeto.declarante_impuesto_renta = "Aplica"
	else:
		objeto.declarante_impuesto_renta = "No Aplica"
	if objeto.compras_practicar_reterenta == True:
		objeto.compras_practicar_reterenta = "Aplica"
	else:
		objeto.compras_practicar_reterenta = "No Aplica"
	if objeto.compras_consumidor_final == True:
		objeto.compras_consumidor_final = "Aplica"
	else:
		objeto.compras_consumidor_final = "No Aplica"
	if objeto.compras_practicar_reteiva == True:
		objeto.compras_practicar_reteiva = "Aplica"
	else:
		objeto.compras_practicar_reteiva = "No Aplica"
	if objeto.compras_practicar_reteica == True:
		objeto.compras_practicar_reteica = "Aplica"
	else:
		objeto.compras_practicar_reteica = "No Aplica"
	if objeto.ventas_liquidar_reterenta == True:
		objeto.ventas_liquidar_reterenta = "Aplica"
	else:
		objeto.ventas_liquidar_reterenta = "No Aplica"
	if objeto.ventas_liquidar_autoretencion_renta == True:
		objeto.ventas_liquidar_autoretencion_renta = "Aplica"
	else:
		objeto.ventas_liquidar_autoretencion_renta = "No Aplica"
	if objeto.ventas_liquidar_reteica == True:
		objeto.ventas_liquidar_reteica = "Aplica"
	else:
		objeto.ventas_liquidar_reteica = "No Aplica"
	for llave, valor in DOCUMENTOS_IDENTIDAD:
		if objeto.identificacion == llave:
			objeto.identificacion = valor
	for llave, valor in NATURALEZA:
		if objeto.naturaleza == llave:
			objeto.naturaleza = valor
	for llave, valor in REGIMEN_TRIBUTARIO:
		if objeto.regimen_tributario == llave:
			objeto.regimen_tributario = valor
	for llave, valor in PAISES:
		if objeto.pais == llave:
			objeto.pais = valor
	return objeto
def reemplazardatos_organizaciones(lista):
	for objeto in lista:
		objeto = reemplazardatos_organizacion(objeto)
	return lista

def reemplazardatos_contacto(objeto):
	if objeto.persona_contacto == None:
		objeto.persona_contacto = "No Registrado"
	if objeto.persona_contacto_adicional == None:
		objeto.persona_contacto_adicional = "No Registrado"
	if objeto.cod_postal == None:
		objeto.cod_postal = "No Registrado"
	if objeto.telefono_dos == None:
		objeto.telefono_dos = "No Registrado"
	if objeto.email == None:
		objeto.email = "No Registrado"
	if objeto.numero_cuenta == None:
		objeto.numero_cuenta = "No Registrado"
	if objeto.tipo_cuenta == None:
		objeto.tipo_cuenta = "No Registrado"
	if objeto.entidad_financiera == None:
		objeto.entidad_financiera = "No Registrado"
	if objeto.consumidor_final == True:
		objeto.consumidor_final = "Aplica"
	else:
		objeto.consumidor_final = "No Aplica"
	if objeto.gran_contribuyente == True:
		objeto.gran_contribuyente = "Aplica"
	else:
		objeto.gran_contribuyente = "No Aplica"
	if objeto.liquidar_reterenta == True:
		objeto.liquidar_reterenta = "Aplica"
	else:
		objeto.liquidar_reterenta = "No Aplica"
	if objeto.liquidar_reteica == True:
		objeto.liquidar_reteica = "Aplica"
	else:
		objeto.liquidar_reteica = "No Aplica"
	if objeto.declarante_impuesto_renta == True:
		objeto.declarante_impuesto_renta = "Aplica"
	else:
		objeto.declarante_impuesto_renta = "No Aplica"
	if objeto.declarante_impuesto_ICA == True:
		objeto.declarante_impuesto_ICA = "Aplica"
	else:
		objeto.declarante_impuesto_ICA = "No Aplica"
	if objeto.autoretenedor_impuesto_renta == True:
		objeto.autoretenedor_impuesto_renta = "Aplica"
	else:
		objeto.autoretenedor_impuesto_renta = "No Aplica"
	if objeto.exento_de_reterenta == True:
		objeto.exento_de_reterenta = "Aplica"
	else:
		objeto.exento_de_reterenta = "No Aplica"
	for llave, valor in DOCUMENTOS_IDENTIDAD:
		if objeto.identificacion == llave:
			objeto.identificacion = valor
	for llave, valor in NATURALEZA:
		if objeto.naturaleza == llave:
			objeto.naturaleza = valor
	for llave, valor in REGIMEN_TRIBUTARIO:
		if objeto.regimen_tributario == llave:
			objeto.regimen_tributario = valor
	for llave, valor in RELACIONES:
		if objeto.relacion_activa == llave:
			objeto.relacion_activa = valor
	for llave, valor in PAISES:
		if objeto.pais == llave:
			objeto.pais = valor
	return objeto
def reemplazardatos_contactos(lista):
	for objeto in lista:
		objeto = reemplazardatos_contacto(objeto)
	return lista

def reemplazardatos_categoria(objeto):
	if objeto.descripcion == None or objeto.descripcion == "":
		objeto.descripcion = "No Registrado"
	for llave, valor in DESTINO_ITEM:
		if objeto.destino_item == llave:
			objeto.destino_item = valor
	return objeto
def reemplazardatos_categorias(lista):
	for objeto in lista:
		objeto = reemplazardatos_categoria(objeto)
	return lista

def reemplazardatos_insumo(objeto):
	if objeto.codigo_barras == None:
		objeto.codigo_barras = "No Registrado"
	if objeto.cantidad == None:
		objeto.cantidad = "No Registrado"
	if objeto.imagen == None or objeto.imagen == "":
		objeto.imagen = "No Registrado"
	if objeto.descripcion_detalle == None or objeto.descripcion_detalle == "":
		objeto.descripcion_detalle = "No Registrado"
	objeto.precio_compra = moneyfmt(objeto.precio_compra)
	for llave, valor in TIPO_ITEM:
		if objeto.tipo_item == llave:
			objeto.tipo_item = valor
	return objeto
def reemplazardatos_insumos(lista):
	for objeto in lista:
		objeto = reemplazardatos_insumo(objeto)
	return lista

def reemplazardatos_item(objeto):
	if objeto.codigo_barras == None:
		objeto.codigo_barras = "No Registrado"
	if objeto.cantidad == None:
		objeto.cantidad = "No Registrado"
	if objeto.imagen == None or objeto.imagen == "":
		objeto.imagen = "No Registrado"
	if objeto.descripcion_detalle == None or objeto.descripcion_detalle == "":
		objeto.descripcion_detalle = "No Registrado"
	objeto.precio_venta = moneyfmt(objeto.precio_venta)
	for llave, valor in TIPO_ITEM:
		if objeto.tipo_item == llave:
			objeto.tipo_item = valor
	return objeto
def reemplazardatos_items(lista):
	for objeto in lista:
		objeto = reemplazardatos_item(objeto)
	return lista

def reemplazardatos_consecutivo(objeto):
	for llave, valor in TIPO_DE_DOCUMENTO:
		if objeto.tipo_de_documento == llave:
			objeto.tipo_de_documento = valor
	return objeto
def reemplazardatos_consecutivos(lista):
	for objeto in lista:
		objeto = reemplazardatos_consecutivo(objeto)
	return lista

def reemplazardatos_terminopago(objeto):
	if objeto.descripcion == None:
		objeto.descripcion = "No Registrado"
	return objeto
def reemplazardatos_terminospago(lista):
	for objeto in lista:
		objeto = reemplazardatos_terminopago(objeto)
	return lista

def reemplazardatos_cotizacion(objeto):
	if objeto.referencia_otro_documento == None or objeto.referencia_otro_documento == "":
		objeto.referencia_otro_documento = "No Registrado"
	if objeto.referencia_orden_compra == None or objeto.referencia_orden_compra == "":
		objeto.referencia_orden_compra = "No Registrado"
	if objeto.referencia_remision == None or objeto.referencia_remision == "":
		objeto.referencia_remision = "No Registrado"
	if objeto.referencia_factura == None or objeto.referencia_factura == "":
		objeto.referencia_factura = "No Registrado"
	if objeto.descripcion_detallada == None or objeto.descripcion_detallada == "":
		objeto.descripcion_detallada = "No Registrado"
	if objeto.observacion == None or objeto.observacion == "":
		objeto.observacion = "No Registrado"
	for llave, valor in MEDIOS_DE_PAGO:
		if objeto.medio_de_pago == llave:
			objeto.medio_de_pago = valor
	for llave, valor in TIPO_IMPUESTO:
		if objeto.tipo_imp1 == llave:
			objeto.tipo_imp1 = valor
	for llave, valor in TIPO_IMPUESTO:
		if objeto.tipo_imp2 == llave:
			objeto.tipo_imp2 = valor
	for llave, valor in TIPO_IMPUESTO:
		if objeto.tipo_imp3 == llave:
			objeto.tipo_imp3 = valor
	for llave, valor in DOCUMENTOS_IDENTIDAD:
		if objeto.id_cliente == llave:
			objeto.id_cliente = valor
	for llave, valor in DOCUMENTOS_IDENTIDAD:
		if objeto.id_organizacion == llave:
			objeto.id_organizacion = valor
	for llave, valor in PAISES:
		if objeto.pais_cliente == llave:
			objeto.pais_cliente = valor
	for llave, valor in PAISES:
		if objeto.pais_organizacion == llave:
			objeto.pais_organizacion = valor
	if objeto.valor_unitario_1:
		objeto.valor_unitario_1 = moneyfmt(objeto.valor_unitario_1)
	if objeto.valor_unitario_2:
		objeto.valor_unitario_2 = moneyfmt(objeto.valor_unitario_2)
	if objeto.valor_unitario_3:
		objeto.valor_unitario_3 = moneyfmt(objeto.valor_unitario_3)
	if objeto.valor_unitario_4:
		objeto.valor_unitario_4 = moneyfmt(objeto.valor_unitario_4)
	if objeto.valor_unitario_5:
		objeto.valor_unitario_5 = moneyfmt(objeto.valor_unitario_5)
	if objeto.valor_descuento_1:
		objeto.valor_descuento_1 = moneyfmt(objeto.valor_descuento_1)
	if objeto.valor_descuento_2:
		objeto.valor_descuento_2 = moneyfmt(objeto.valor_descuento_2)
	if objeto.valor_descuento_3:
		objeto.valor_descuento_3 = moneyfmt(objeto.valor_descuento_3)
	if objeto.valor_descuento_4:
		objeto.valor_descuento_4 = moneyfmt(objeto.valor_descuento_4)
	if objeto.valor_descuento_5:
		objeto.valor_descuento_5 = moneyfmt(objeto.valor_descuento_5)
	if objeto.iva_1:
		objeto.iva_1 = moneyfmt(objeto.iva_1)
	if objeto.iva_2:
		objeto.iva_2 = moneyfmt(objeto.iva_2)
	if objeto.iva_3:
		objeto.iva_3 = moneyfmt(objeto.iva_3)
	if objeto.iva_4:
		objeto.iva_4 = moneyfmt(objeto.iva_4)
	if objeto.iva_5:
		objeto.iva_5 = moneyfmt(objeto.iva_5)
	if objeto.ico_1:
		objeto.ico_1 = moneyfmt(objeto.ico_1)
	if objeto.ico_2:
		objeto.ico_2 = moneyfmt(objeto.ico_2)
	if objeto.ico_3:
		objeto.ico_3 = moneyfmt(objeto.ico_3)
	if objeto.ico_4:
		objeto.ico_4 = moneyfmt(objeto.ico_4)
	if objeto.ico_5:
		objeto.ico_5 = moneyfmt(objeto.ico_5)
	if objeto.valor_total_1:
		objeto.valor_total_1 = moneyfmt(objeto.valor_total_1)
	if objeto.valor_total_2:
		objeto.valor_total_2 = moneyfmt(objeto.valor_total_2)
	if objeto.valor_total_3:
		objeto.valor_total_3 = moneyfmt(objeto.valor_total_3)
	if objeto.valor_total_4:
		objeto.valor_total_4 = moneyfmt(objeto.valor_total_4)
	if objeto.valor_total_5:
		objeto.valor_total_5 = moneyfmt(objeto.valor_total_5)
	if objeto.iva_total:
		objeto.iva_total = moneyfmt(objeto.iva_total)
	if objeto.ico_total:
		objeto.ico_total = moneyfmt(objeto.ico_total)
	if objeto.reterenta:
		objeto.reterenta = moneyfmt(objeto.reterenta)
	if objeto.reteiva:
		objeto.reteiva = moneyfmt(objeto.reteiva)
	if objeto.reteica:
		objeto.reteica = moneyfmt(objeto.reteica)
	if objeto.sub_total:
		objeto.sub_total = moneyfmt(objeto.sub_total)
	if objeto.total_impuestos:
		objeto.total_impuestos = moneyfmt(objeto.total_impuestos)
	if objeto.total_retenciones:
		objeto.total_retenciones = moneyfmt(objeto.total_retenciones)
	if objeto.total_documento:
		objeto.total_documento = moneyfmt(objeto.total_documento)
	if objeto.anticipo:
		objeto.anticipo = moneyfmt(objeto.anticipo)
	if objeto.saldo_pendiente:
		objeto.saldo_pendiente = moneyfmt(objeto.saldo_pendiente)
	return objeto
def reemplazardatos_cotizaciones(lista):
	for objeto in lista:
		objeto = reemplazardatos_cotizacion(objeto)
	return lista

def reemplazardatos_factura(objeto):
	if objeto.referencia_otro_documento == None or objeto.referencia_otro_documento == "":
		objeto.referencia_otro_documento = "No Registrado"
	if objeto.referencia_orden_compra == None or objeto.referencia_orden_compra == "":
		objeto.referencia_orden_compra = "No Registrado"
	if objeto.referencia_remision == None or objeto.referencia_remision == "":
		objeto.referencia_remision = "No Registrado"
	if objeto.referencia_cotizacion == None or objeto.referencia_cotizacion == "":
		objeto.referencia_cotizacion = "No Registrado"
	if objeto.referencia_notacredito == None or objeto.referencia_notacredito == "":
		objeto.referencia_notacredito = "No Registrado"
	if objeto.referencia_notadebito == None or objeto.referencia_notadebito == "":
		objeto.referencia_notadebito = "No Registrado"
	if objeto.descripcion_detallada == None or objeto.descripcion_detallada == "":
		objeto.descripcion_detallada = "No Registrado"
	if objeto.observacion == None or objeto.observacion == "":
		objeto.observacion = "No Registrado"
	for llave, valor in MEDIOS_DE_PAGO:
		if objeto.medio_de_pago == llave:
			objeto.medio_de_pago = valor
	for llave, valor in TIPO_IMPUESTO:
		if objeto.tipo_imp1 == llave:
			objeto.tipo_imp1 = valor
	for llave, valor in TIPO_IMPUESTO:
		if objeto.tipo_imp2 == llave:
			objeto.tipo_imp2 = valor
	for llave, valor in TIPO_IMPUESTO:
		if objeto.tipo_imp3 == llave:
			objeto.tipo_imp3 = valor
	for llave, valor in DOCUMENTOS_IDENTIDAD:
		if objeto.id_cliente == llave:
			objeto.id_cliente = valor
	for llave, valor in DOCUMENTOS_IDENTIDAD:
		if objeto.id_organizacion == llave:
			objeto.id_organizacion = valor
	for llave, valor in PAISES:
		if objeto.pais_cliente == llave:
			objeto.pais_cliente = valor
	for llave, valor in PAISES:
		if objeto.pais_organizacion == llave:
			objeto.pais_organizacion = valor
	if objeto.valor_unitario_1:
		objeto.valor_unitario_1 = moneyfmt(objeto.valor_unitario_1)
	if objeto.valor_unitario_2:
		objeto.valor_unitario_2 = moneyfmt(objeto.valor_unitario_2)
	if objeto.valor_unitario_3:
		objeto.valor_unitario_3 = moneyfmt(objeto.valor_unitario_3)
	if objeto.valor_unitario_4:
		objeto.valor_unitario_4 = moneyfmt(objeto.valor_unitario_4)
	if objeto.valor_unitario_5:
		objeto.valor_unitario_5 = moneyfmt(objeto.valor_unitario_5)
	if objeto.valor_descuento_1:
		objeto.valor_descuento_1 = moneyfmt(objeto.valor_descuento_1)
	if objeto.valor_descuento_2:
		objeto.valor_descuento_2 = moneyfmt(objeto.valor_descuento_2)
	if objeto.valor_descuento_3:
		objeto.valor_descuento_3 = moneyfmt(objeto.valor_descuento_3)
	if objeto.valor_descuento_4:
		objeto.valor_descuento_4 = moneyfmt(objeto.valor_descuento_4)
	if objeto.valor_descuento_5:
		objeto.valor_descuento_5 = moneyfmt(objeto.valor_descuento_5)
	if objeto.iva_1:
		objeto.iva_1 = moneyfmt(objeto.iva_1)
	if objeto.iva_2:
		objeto.iva_2 = moneyfmt(objeto.iva_2)
	if objeto.iva_3:
		objeto.iva_3 = moneyfmt(objeto.iva_3)
	if objeto.iva_4:
		objeto.iva_4 = moneyfmt(objeto.iva_4)
	if objeto.iva_5:
		objeto.iva_5 = moneyfmt(objeto.iva_5)
	if objeto.ico_1:
		objeto.ico_1 = moneyfmt(objeto.ico_1)
	if objeto.ico_2:
		objeto.ico_2 = moneyfmt(objeto.ico_2)
	if objeto.ico_3:
		objeto.ico_3 = moneyfmt(objeto.ico_3)
	if objeto.ico_4:
		objeto.ico_4 = moneyfmt(objeto.ico_4)
	if objeto.ico_5:
		objeto.ico_5 = moneyfmt(objeto.ico_5)
	if objeto.valor_total_1:
		objeto.valor_total_1 = moneyfmt(objeto.valor_total_1)
	if objeto.valor_total_2:
		objeto.valor_total_2 = moneyfmt(objeto.valor_total_2)
	if objeto.valor_total_3:
		objeto.valor_total_3 = moneyfmt(objeto.valor_total_3)
	if objeto.valor_total_4:
		objeto.valor_total_4 = moneyfmt(objeto.valor_total_4)
	if objeto.valor_total_5:
		objeto.valor_total_5 = moneyfmt(objeto.valor_total_5)
	if objeto.iva_total:
		objeto.iva_total = moneyfmt(objeto.iva_total)
	if objeto.ico_total:
		objeto.ico_total = moneyfmt(objeto.ico_total)
	if objeto.reterenta:
		objeto.reterenta = moneyfmt(objeto.reterenta)
	if objeto.reteiva:
		objeto.reteiva = moneyfmt(objeto.reteiva)
	if objeto.reteica:
		objeto.reteica = moneyfmt(objeto.reteica)
	if objeto.sub_total:
		objeto.sub_total = moneyfmt(objeto.sub_total)
	if objeto.total_impuestos:
		objeto.total_impuestos = moneyfmt(objeto.total_impuestos)
	if objeto.total_retenciones:
		objeto.total_retenciones = moneyfmt(objeto.total_retenciones)
	if objeto.total_documento:
		objeto.total_documento = moneyfmt(objeto.total_documento)
	if objeto.anticipo:
		objeto.anticipo = moneyfmt(objeto.anticipo)
	if objeto.saldo_pendiente:
		objeto.saldo_pendiente = moneyfmt(objeto.saldo_pendiente)
	return objeto
def reemplazardatos_facturas(lista):
	for objeto in lista:
		objeto = reemplazardatos_factura(objeto)
	return lista

def reemplazardatos_factura_comp(objeto):
	if objeto.descripcion_detallada == None or objeto.descripcion_detallada == "":
		objeto.descripcion_detallada = "No Registrado"
	if objeto.observacion == None or objeto.observacion == "":
		objeto.observacion = "No Registrado"
	for llave, valor in MEDIOS_DE_PAGO:
		if objeto.medio_de_pago == llave:
			objeto.medio_de_pago = valor
	for llave, valor in TIPO_IMPUESTO:
		if objeto.tipo_imp1 == llave:
			objeto.tipo_imp1 = valor
	for llave, valor in TIPO_IMPUESTO:
		if objeto.tipo_imp2 == llave:
			objeto.tipo_imp2 = valor
	for llave, valor in TIPO_IMPUESTO:
		if objeto.tipo_imp3 == llave:
			objeto.tipo_imp3 = valor
	for llave, valor in DOCUMENTOS_IDENTIDAD:
		if objeto.id_proveedor == llave:
			objeto.id_proveedor = valor
	for llave, valor in DOCUMENTOS_IDENTIDAD:
		if objeto.id_organizacion == llave:
			objeto.id_organizacion = valor
	for llave, valor in PAISES:
		if objeto.pais_proveedor == llave:
			objeto.pais_proveedor = valor
	for llave, valor in PAISES:
		if objeto.pais_organizacion == llave:
			objeto.pais_organizacion = valor
	if objeto.valor_unitario_1:
		objeto.valor_unitario_1 = moneyfmt(objeto.valor_unitario_1)
	if objeto.valor_unitario_2:
		objeto.valor_unitario_2 = moneyfmt(objeto.valor_unitario_2)
	if objeto.valor_unitario_3:
		objeto.valor_unitario_3 = moneyfmt(objeto.valor_unitario_3)
	if objeto.valor_unitario_4:
		objeto.valor_unitario_4 = moneyfmt(objeto.valor_unitario_4)
	if objeto.valor_unitario_5:
		objeto.valor_unitario_5 = moneyfmt(objeto.valor_unitario_5)
	if objeto.valor_descuento_1:
		objeto.valor_descuento_1 = moneyfmt(objeto.valor_descuento_1)
	if objeto.valor_descuento_2:
		objeto.valor_descuento_2 = moneyfmt(objeto.valor_descuento_2)
	if objeto.valor_descuento_3:
		objeto.valor_descuento_3 = moneyfmt(objeto.valor_descuento_3)
	if objeto.valor_descuento_4:
		objeto.valor_descuento_4 = moneyfmt(objeto.valor_descuento_4)
	if objeto.valor_descuento_5:
		objeto.valor_descuento_5 = moneyfmt(objeto.valor_descuento_5)
	if objeto.iva_1:
		objeto.iva_1 = moneyfmt(objeto.iva_1)
	if objeto.iva_2:
		objeto.iva_2 = moneyfmt(objeto.iva_2)
	if objeto.iva_3:
		objeto.iva_3 = moneyfmt(objeto.iva_3)
	if objeto.iva_4:
		objeto.iva_4 = moneyfmt(objeto.iva_4)
	if objeto.iva_5:
		objeto.iva_5 = moneyfmt(objeto.iva_5)
	if objeto.ico_1:
		objeto.ico_1 = moneyfmt(objeto.ico_1)
	if objeto.ico_2:
		objeto.ico_2 = moneyfmt(objeto.ico_2)
	if objeto.ico_3:
		objeto.ico_3 = moneyfmt(objeto.ico_3)
	if objeto.ico_4:
		objeto.ico_4 = moneyfmt(objeto.ico_4)
	if objeto.ico_5:
		objeto.ico_5 = moneyfmt(objeto.ico_5)
	if objeto.valor_total_1:
		objeto.valor_total_1 = moneyfmt(objeto.valor_total_1)
	if objeto.valor_total_2:
		objeto.valor_total_2 = moneyfmt(objeto.valor_total_2)
	if objeto.valor_total_3:
		objeto.valor_total_3 = moneyfmt(objeto.valor_total_3)
	if objeto.valor_total_4:
		objeto.valor_total_4 = moneyfmt(objeto.valor_total_4)
	if objeto.valor_total_5:
		objeto.valor_total_5 = moneyfmt(objeto.valor_total_5)
	if objeto.iva_total:
		objeto.iva_total = moneyfmt(objeto.iva_total)
	if objeto.ico_total:
		objeto.ico_total = moneyfmt(objeto.ico_total)
	if objeto.reterenta:
		objeto.reterenta = moneyfmt(objeto.reterenta)
	if objeto.reteiva:
		objeto.reteiva = moneyfmt(objeto.reteiva)
	if objeto.reteica:
		objeto.reteica = moneyfmt(objeto.reteica)
	if objeto.sub_total:
		objeto.sub_total = moneyfmt(objeto.sub_total)
	if objeto.total_impuestos:
		objeto.total_impuestos = moneyfmt(objeto.total_impuestos)
	if objeto.total_retenciones:
		objeto.total_retenciones = moneyfmt(objeto.total_retenciones)
	if objeto.total_documento:
		objeto.total_documento = moneyfmt(objeto.total_documento)
	if objeto.anticipo:
		objeto.anticipo = moneyfmt(objeto.anticipo)
	if objeto.saldo_pendiente:
		objeto.saldo_pendiente = moneyfmt(objeto.saldo_pendiente)
	return objeto
def reemplazardatos_facturas_comp(lista):
	for objeto in lista:
		objeto = reemplazardatos_factura_comp(objeto)
	return lista

def reemplazardatos_credit_note(objeto):
	if objeto.referencia_factura == None or objeto.referencia_factura == "":
		objeto.referencia_factura = "No Registrado"
	if objeto.referencia_factura_DIAN == None or objeto.referencia_factura_DIAN == "":
		objeto.referencia_factura_DIAN = "No Registrado"
	if objeto.referencia_cotizacion == None or objeto.referencia_cotizacion == "":
		objeto.referencia_cotizacion = "No Registrado"
	if objeto.referencia_remision == None or objeto.referencia_remision == "":
		objeto.referencia_remision = "No Registrado"
	if objeto.referencia_orden_compra == None or objeto.referencia_orden_compra == "":
		objeto.referencia_orden_compra = "No Registrado"
	if objeto.referencia_otro_documento == None or objeto.referencia_otro_documento == "":
		objeto.referencia_otro_documento = "No Registrado"
	if objeto.descripcion_detallada == None or objeto.descripcion_detallada == "":
		objeto.descripcion_detallada = "No Registrado"
	if objeto.observacion == None or objeto.observacion == "":
		objeto.observacion = "No Registrado"
	for llave, valor in MEDIOS_DE_PAGO:
		if objeto.medio_de_pago == llave:
			objeto.medio_de_pago = valor
	for llave, valor in TIPO_IMPUESTO:
		if objeto.tipo_imp1 == llave:
			objeto.tipo_imp1 = valor
	for llave, valor in TIPO_IMPUESTO:
		if objeto.tipo_imp2 == llave:
			objeto.tipo_imp2 = valor
	for llave, valor in TIPO_IMPUESTO:
		if objeto.tipo_imp3 == llave:
			objeto.tipo_imp3 = valor
	for llave, valor in DOCUMENTOS_IDENTIDAD:
		if objeto.id_cliente == llave:
			objeto.id_cliente = valor
	for llave, valor in DOCUMENTOS_IDENTIDAD:
		if objeto.id_organizacion == llave:
			objeto.id_organizacion = valor
	for llave, valor in CONCEPTO_NOTA_CREDITO:
		if objeto.concepto_nota_credito == llave:
			objeto.concepto_nota_credito = valor
	for llave, valor in PAISES:
		if objeto.pais_cliente == llave:
			objeto.pais_cliente = valor
	for llave, valor in PAISES:
		if objeto.pais_organizacion == llave:
			objeto.pais_organizacion = valor
	if objeto.valor_unitario_1:
		objeto.valor_unitario_1 = moneyfmt(objeto.valor_unitario_1)
	if objeto.valor_unitario_2:
		objeto.valor_unitario_2 = moneyfmt(objeto.valor_unitario_2)
	if objeto.valor_unitario_3:
		objeto.valor_unitario_3 = moneyfmt(objeto.valor_unitario_3)
	if objeto.valor_unitario_4:
		objeto.valor_unitario_4 = moneyfmt(objeto.valor_unitario_4)
	if objeto.valor_unitario_5:
		objeto.valor_unitario_5 = moneyfmt(objeto.valor_unitario_5)
	if objeto.valor_descuento_1:
		objeto.valor_descuento_1 = moneyfmt(objeto.valor_descuento_1)
	if objeto.valor_descuento_2:
		objeto.valor_descuento_2 = moneyfmt(objeto.valor_descuento_2)
	if objeto.valor_descuento_3:
		objeto.valor_descuento_3 = moneyfmt(objeto.valor_descuento_3)
	if objeto.valor_descuento_4:
		objeto.valor_descuento_4 = moneyfmt(objeto.valor_descuento_4)
	if objeto.valor_descuento_5:
		objeto.valor_descuento_5 = moneyfmt(objeto.valor_descuento_5)
	if objeto.iva_1:
		objeto.iva_1 = moneyfmt(objeto.iva_1)
	if objeto.iva_2:
		objeto.iva_2 = moneyfmt(objeto.iva_2)
	if objeto.iva_3:
		objeto.iva_3 = moneyfmt(objeto.iva_3)
	if objeto.iva_4:
		objeto.iva_4 = moneyfmt(objeto.iva_4)
	if objeto.iva_5:
		objeto.iva_5 = moneyfmt(objeto.iva_5)
	if objeto.ico_1:
		objeto.ico_1 = moneyfmt(objeto.ico_1)
	if objeto.ico_2:
		objeto.ico_2 = moneyfmt(objeto.ico_2)
	if objeto.ico_3:
		objeto.ico_3 = moneyfmt(objeto.ico_3)
	if objeto.ico_4:
		objeto.ico_4 = moneyfmt(objeto.ico_4)
	if objeto.ico_5:
		objeto.ico_5 = moneyfmt(objeto.ico_5)
	if objeto.valor_total_1:
		objeto.valor_total_1 = moneyfmt(objeto.valor_total_1)
	if objeto.valor_total_2:
		objeto.valor_total_2 = moneyfmt(objeto.valor_total_2)
	if objeto.valor_total_3:
		objeto.valor_total_3 = moneyfmt(objeto.valor_total_3)
	if objeto.valor_total_4:
		objeto.valor_total_4 = moneyfmt(objeto.valor_total_4)
	if objeto.valor_total_5:
		objeto.valor_total_5 = moneyfmt(objeto.valor_total_5)
	if objeto.iva_total:
		objeto.iva_total = moneyfmt(objeto.iva_total)
	if objeto.ico_total:
		objeto.ico_total = moneyfmt(objeto.ico_total)
	if objeto.reterenta:
		objeto.reterenta = moneyfmt(objeto.reterenta)
	if objeto.reteiva:
		objeto.reteiva = moneyfmt(objeto.reteiva)
	if objeto.reteica:
		objeto.reteica = moneyfmt(objeto.reteica)
	if objeto.sub_total:
		objeto.sub_total = moneyfmt(objeto.sub_total)
	if objeto.total_impuestos:
		objeto.total_impuestos = moneyfmt(objeto.total_impuestos)
	if objeto.total_retenciones:
		objeto.total_retenciones = moneyfmt(objeto.total_retenciones)
	if objeto.total_documento:
		objeto.total_documento = moneyfmt(objeto.total_documento)
	if objeto.anticipo:
		objeto.anticipo = moneyfmt(objeto.anticipo)
	if objeto.saldo_pendiente:
		objeto.saldo_pendiente = moneyfmt(objeto.saldo_pendiente)
	if objeto.descuento_rebaja:
		objeto.descuento_rebaja = moneyfmt(objeto.descuento_rebaja)
	if objeto.saldo_total:
		objeto.saldo_total = moneyfmt(objeto.saldo_total)
	return objeto
def reemplazardatos_credits_notes(lista):
	for objeto in lista:
		objeto = reemplazardatos_credit_note(objeto)
	return lista

def reemplazardatos_debit_note(objeto):
	if objeto.referencia_factura == None or objeto.referencia_factura == "":
		objeto.referencia_factura = "No Registrado"
	if objeto.referencia_factura_DIAN == None or objeto.referencia_factura_DIAN == "":
		objeto.referencia_factura_DIAN = "No Registrado"
	if objeto.referencia_cotizacion == None or objeto.referencia_cotizacion == "":
		objeto.referencia_cotizacion = "No Registrado"
	if objeto.referencia_remision == None or objeto.referencia_remision == "":
		objeto.referencia_remision = "No Registrado"
	if objeto.referencia_orden_compra == None or objeto.referencia_orden_compra == "":
		objeto.referencia_orden_compra = "No Registrado"
	if objeto.referencia_otro_documento == None or objeto.referencia_otro_documento == "":
		objeto.referencia_otro_documento = "No Registrado"
	if objeto.descripcion_detallada == None or objeto.descripcion_detallada == "":
		objeto.descripcion_detallada = "No Registrado"
	if objeto.observacion == None or objeto.observacion == "":
		objeto.observacion = "No Registrado"
	for llave, valor in MEDIOS_DE_PAGO:
		if objeto.medio_de_pago == llave:
			objeto.medio_de_pago = valor
	for llave, valor in TIPO_IMPUESTO:
		if objeto.tipo_imp1 == llave:
			objeto.tipo_imp1 = valor
	for llave, valor in TIPO_IMPUESTO:
		if objeto.tipo_imp2 == llave:
			objeto.tipo_imp2 = valor
	for llave, valor in TIPO_IMPUESTO:
		if objeto.tipo_imp3 == llave:
			objeto.tipo_imp3 = valor
	for llave, valor in DOCUMENTOS_IDENTIDAD:
		if objeto.id_cliente == llave:
			objeto.id_cliente = valor
	for llave, valor in DOCUMENTOS_IDENTIDAD:
		if objeto.id_organizacion == llave:
			objeto.id_organizacion = valor
	for llave, valor in CONCEPTO_NOTA_DEBITO:
		if objeto.concepto_nota_debito == llave:
			objeto.concepto_nota_debito = valor
	for llave, valor in PAISES:
		if objeto.pais_cliente == llave:
			objeto.pais_cliente = valor
	for llave, valor in PAISES:
		if objeto.pais_organizacion == llave:
			objeto.pais_organizacion = valor
	if objeto.valor_unitario_1:
		objeto.valor_unitario_1 = moneyfmt(objeto.valor_unitario_1)
	if objeto.valor_unitario_2:
		objeto.valor_unitario_2 = moneyfmt(objeto.valor_unitario_2)
	if objeto.valor_unitario_3:
		objeto.valor_unitario_3 = moneyfmt(objeto.valor_unitario_3)
	if objeto.valor_unitario_4:
		objeto.valor_unitario_4 = moneyfmt(objeto.valor_unitario_4)
	if objeto.valor_unitario_5:
		objeto.valor_unitario_5 = moneyfmt(objeto.valor_unitario_5)
	if objeto.valor_descuento_1:
		objeto.valor_descuento_1 = moneyfmt(objeto.valor_descuento_1)
	if objeto.valor_descuento_2:
		objeto.valor_descuento_2 = moneyfmt(objeto.valor_descuento_2)
	if objeto.valor_descuento_3:
		objeto.valor_descuento_3 = moneyfmt(objeto.valor_descuento_3)
	if objeto.valor_descuento_4:
		objeto.valor_descuento_4 = moneyfmt(objeto.valor_descuento_4)
	if objeto.valor_descuento_5:
		objeto.valor_descuento_5 = moneyfmt(objeto.valor_descuento_5)
	if objeto.iva_1:
		objeto.iva_1 = moneyfmt(objeto.iva_1)
	if objeto.iva_2:
		objeto.iva_2 = moneyfmt(objeto.iva_2)
	if objeto.iva_3:
		objeto.iva_3 = moneyfmt(objeto.iva_3)
	if objeto.iva_4:
		objeto.iva_4 = moneyfmt(objeto.iva_4)
	if objeto.iva_5:
		objeto.iva_5 = moneyfmt(objeto.iva_5)
	if objeto.ico_1:
		objeto.ico_1 = moneyfmt(objeto.ico_1)
	if objeto.ico_2:
		objeto.ico_2 = moneyfmt(objeto.ico_2)
	if objeto.ico_3:
		objeto.ico_3 = moneyfmt(objeto.ico_3)
	if objeto.ico_4:
		objeto.ico_4 = moneyfmt(objeto.ico_4)
	if objeto.ico_5:
		objeto.ico_5 = moneyfmt(objeto.ico_5)
	if objeto.valor_total_1:
		objeto.valor_total_1 = moneyfmt(objeto.valor_total_1)
	if objeto.valor_total_2:
		objeto.valor_total_2 = moneyfmt(objeto.valor_total_2)
	if objeto.valor_total_3:
		objeto.valor_total_3 = moneyfmt(objeto.valor_total_3)
	if objeto.valor_total_4:
		objeto.valor_total_4 = moneyfmt(objeto.valor_total_4)
	if objeto.valor_total_5:
		objeto.valor_total_5 = moneyfmt(objeto.valor_total_5)
	if objeto.iva_total:
		objeto.iva_total = moneyfmt(objeto.iva_total)
	if objeto.ico_total:
		objeto.ico_total = moneyfmt(objeto.ico_total)
	if objeto.reterenta:
		objeto.reterenta = moneyfmt(objeto.reterenta)
	if objeto.reteiva:
		objeto.reteiva = moneyfmt(objeto.reteiva)
	if objeto.reteica:
		objeto.reteica = moneyfmt(objeto.reteica)
	if objeto.sub_total:
		objeto.sub_total = moneyfmt(objeto.sub_total)
	if objeto.total_impuestos:
		objeto.total_impuestos = moneyfmt(objeto.total_impuestos)
	if objeto.total_retenciones:
		objeto.total_retenciones = moneyfmt(objeto.total_retenciones)
	if objeto.total_documento:
		objeto.total_documento = moneyfmt(objeto.total_documento)
	if objeto.anticipo:
		objeto.anticipo = moneyfmt(objeto.anticipo)
	if objeto.saldo_pendiente:
		objeto.saldo_pendiente = moneyfmt(objeto.saldo_pendiente)
	if objeto.cargo_interes:
		objeto.cargo_interes = moneyfmt(objeto.cargo_interes)
	if objeto.saldo_total:
		objeto.saldo_total = moneyfmt(objeto.saldo_total)
	return objeto
def reemplazardatos_debits_notes(lista):
	for objeto in lista:
		objeto = reemplazardatos_debit_note(objeto)
	return lista

def reemplazardatos_remision(objeto):
	if objeto.referencia_otro_documento == None or objeto.referencia_otro_documento == "":
		objeto.referencia_otro_documento = "No Registrado"
	if objeto.referencia_orden_compra == None or objeto.referencia_orden_compra == "":
		objeto.referencia_orden_compra = "No Registrado"
	if objeto.referencia_cotizacion == None or objeto.referencia_cotizacion == "":
		objeto.referencia_cotizacion = "No Registrado"
	if objeto.referencia_factura == None or objeto.referencia_factura == "":
		objeto.referencia_factura = "No Registrado"
	if objeto.descripcion_detallada == None or objeto.descripcion_detallada == "":
		objeto.descripcion_detallada = "No Registrado"
	if objeto.datos_transportador == None or objeto.datos_transportador == "":
		objeto.datos_transportador = "No Registrado"
	if objeto.observacion == None or objeto.observacion == "":
		objeto.observacion = "No Registrado"
	for llave, valor in DOCUMENTOS_IDENTIDAD:
		if objeto.id_cliente == llave:
			objeto.id_cliente = valor
	for llave, valor in DOCUMENTOS_IDENTIDAD:
		if objeto.id_organizacion == llave:
			objeto.id_organizacion = valor
	for llave, valor in PAISES:
		if objeto.pais_cliente == llave:
			objeto.pais_cliente = valor
	for llave, valor in PAISES:
		if objeto.pais_organizacion == llave:
			objeto.pais_organizacion = valor
	return objeto
def reemplazardatos_remisiones(lista):
	for objeto in lista:
		objeto = reemplazardatos_remision(objeto)
	return lista

def reemplazardatos_reporte(objeto):
	for llave, valor in METRICA_CRECIMIENTO:
		if objeto.metrica_crecimiento == llave:
			objeto.metrica_crecimiento = valor
	if objeto.ventas_dia:
		objeto.ventas_dia = moneyfmt(objeto.ventas_dia)
	if objeto.ventas_semana:
		objeto.ventas_semana = moneyfmt(objeto.ventas_semana)
	if objeto.ventas_mes:
		objeto.ventas_mes = moneyfmt(objeto.ventas_mes)
	if objeto.ventas_año:
		objeto.ventas_año = moneyfmt(objeto.ventas_año)
	if objeto.ventas_periodo:
		objeto.ventas_periodo = moneyfmt(objeto.ventas_periodo)
	if objeto.ganancias_dia:
		objeto.ganancias_dia = moneyfmt(objeto.ganancias_dia)
	if objeto.ganancias_semana:
		objeto.ganancias_semana = moneyfmt(objeto.ganancias_semana)
	if objeto.ganancias_mes:
		objeto.ganancias_mes = moneyfmt(objeto.ganancias_mes)
	if objeto.ganancias_año:
		objeto.ganancias_año = moneyfmt(objeto.ganancias_año)
	if objeto.ganancias_periodo:
		objeto.ganancias_periodo = moneyfmt(objeto.ganancias_periodo)
	return objeto
def reemplazardatos_reportes(lista):
	for objeto in lista:
		objeto = reemplazardatos_reporte(objeto)
	return lista

def reemplazardatos_gasto(objeto):
	for llave, valor in CONCEPTO_GASTO:
		if objeto.concepto_gasto == llave:
			objeto.concepto_gasto = valor
	if objeto.descripcion_gasto == None or objeto.descripcion_gasto == "":
		objeto.descripcion_gasto = "No Registrado"
	if objeto.valor_gasto:
		objeto.valor_gasto = moneyfmt(objeto.valor_gasto)
	return objeto
def reemplazardatos_gastos(lista):
	for objeto in lista:
		objeto = reemplazardatos_gasto(objeto)
	return lista

def fetch_resources(uri, rel):
	sUrl = settings.STATIC_URL
	sRoot = settings.STATIC_ROOT
	mUrl = settings.MEDIA_URL
	mRoot = settings.MEDIA_ROOT
	if uri.startswith(mUrl):
		path = os.path.join(mRoot, uri.replace(mUrl, ""))
	elif uri.startswith(sUrl):
		path = os.path.join(sRoot, uri.replace(sUrl, ""))
	else:
		return uri

	if not os.path.isfile(path):
		raise Exception('media URI must start with %s or %s' % (sUrl, mUrl))
	return path

def last_three_objects(objetos):
	tamaño = len(objetos)
	objetos_recientes = []
	indice = 1
	while indice <= tamaño and indice <= 3:
		recent_obj = objetos[tamaño - indice]
		objetos_recientes.append(recent_obj)
		indice = indice + 1
	return objetos_recientes

# FUNCIONES DE VISTA

def home_page(request):
	return render(request, 'groway/home_page.html', {})

def caracteristicas(request):
	return render(request, 'groway/caracteristicas.html', {})

def nuevo_usuario(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('login')
	else:
		form = UserCreationForm()
	return render(request, 'groway/nuevo_usuario.html', {'form':form})

@login_required
def dashboard(request):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayfacturas = Factura_de_venta.objects.filter(org_creadora=orgactivas, generado=True).count()
	solo_fac_anuladas = Factura_de_venta.objects.filter(org_creadora=orgactivas, generado=True, anulada=False).count()
	facturas = Factura_de_venta.objects.filter(org_creadora=orgactivas, generado=True, anulada=False).order_by('fecha_emision')
	nohaycotizaciones = Cotizacion.objects.filter(org_creadora=orgactivas, generado=True).count()
	cotizaciones = Cotizacion.objects.filter(org_creadora=orgactivas, generado=True).order_by('fecha_emision')
	nohayremisiones = Remision.objects.filter(org_creadora=orgactivas).count()
	remisiones = Remision.objects.filter(org_creadora=orgactivas).order_by('fecha_emision')
	nohayreportes = Crecimiento.objects.filter(org_creadora=orgactivas, guardada=True).count()
	reportes = Crecimiento.objects.filter(org_creadora=orgactivas, guardada=True).order_by('nombre')
	if facturas:
		facturas = last_three_objects(facturas)
		facturas = reemplazardatos_facturas(facturas)
	if cotizaciones:
		cotizaciones = last_three_objects(cotizaciones)
		cotizaciones = reemplazardatos_cotizaciones(cotizaciones)
	if remisiones:
		remisiones = last_three_objects(remisiones)
		remisiones = reemplazardatos_remisiones(remisiones)
	if reportes:
		reportes = last_three_objects(reportes)
		reportes = reemplazardatos_reportes(reportes)
	return render(request, 'groway/dashboard.html', {'orgactivas':orgactivas, 'facturas':facturas, 'cotizaciones':cotizaciones, 'remisiones':remisiones, 'reportes':reportes,
	 'nohayfacturas':nohayfacturas, 'nohaycotizaciones':nohaycotizaciones, 'nohayremisiones':nohayremisiones, 'nohayreportes':nohayreportes, 'solo_fac_anuladas':solo_fac_anuladas})

@login_required
def organizacion(request):
	lista ="valor"
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayorganizacion = Organizacion.objects.filter(administrador=request.user).count()
	if request.method == "POST":
			dic = request.POST
			busqueda = dic["buscar"]
			orden = dic["ordenar"]
			buscarxnombre = Organizacion.objects.filter(nombre_legal__contains=busqueda, administrador=request.user)
			buscarxnumid = Organizacion.objects.filter(numero_identificacion__contains=busqueda, administrador=request.user)
			if buscarxnombre:
				lista = buscarxnombre.order_by(orden)
				lista = reemplazardatos_organizaciones(lista)
			elif buscarxnumid:
				lista = buscarxnumid.order_by(orden)
				lista = reemplazardatos_organizaciones(lista)
			else:
				lista = Organizacion.objects.filter(administrador=request.user).order_by('nombre_legal')
				lista = reemplazardatos_organizaciones(lista)
	organizaciones = Organizacion.objects.filter(administrador=request.user).order_by('nombre_legal')
	organizaciones = reemplazardatos_organizaciones(organizaciones)
	return render(request, 'groway/organizacion.html', {'orgactivas':orgactivas, 'organizaciones':organizaciones, 'lista':lista, 'nohayorganizacion':nohayorganizacion})

def nueva_organizacion(request):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayorganizacion = Organizacion.objects.filter(administrador=request.user).count()
	if request.method == "POST":
		form = OrganizacionForm(request.POST, request.FILES)
		if form.is_valid():
			organizacion = form.save(commit=False)
			organizacion.administrador = request.user
			if orgactivas:
				organizacion.save()
			else:
				organizacion.activa = True
				organizacion.save()
			return redirect('detalle_organizacion', pk=organizacion.pk)
	else:
		form = OrganizacionForm()
	organizaciones = Organizacion.objects.filter(administrador=request.user).order_by('nombre_legal')
	organizaciones = reemplazardatos_organizaciones(organizaciones)
	return render(request, 'groway/nueva_organizacion.html', {'form':form, 'orgactivas':orgactivas, 'organizaciones':organizaciones, 'nohayorganizacion':nohayorganizacion})

def editar_organizacion(request, pk):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayorganizacion = Organizacion.objects.filter(administrador=request.user).count()
	organizacion = get_object_or_404(Organizacion, pk=pk)
	admin_org = organizacion.administrador
	estado = organizacion.activa
	if request.method == "POST":
		form = OrganizacionForm(request.POST, request.FILES, instance=organizacion)
		if form.is_valid():
			organizacion = form.save(commit=False)
			organizacion.administrador = admin_org
			organizacion.activa = estado
			organizacion.sesion_cerrada = False
			organizacion.save()
			return redirect('detalle_organizacion', pk=organizacion.pk)
	else:
		form = OrganizacionForm(instance=organizacion)
	organizaciones = Organizacion.objects.filter(administrador=request.user).order_by('nombre_legal')
	organizaciones = reemplazardatos_organizaciones(organizaciones)
	return render(request, 'groway/nueva_organizacion.html', {'form':form, 'orgactivas':orgactivas, 'organizacion':organizacion, 'organizaciones':organizaciones, 'nohayorganizacion':nohayorganizacion})

def eliminar_organizacion(request, pk):
	organizacion = get_object_or_404(Organizacion, pk=pk)
	organizacion.delete()
	return redirect('organizacion')

def estado_org(request, pk):
	organizacion = get_object_or_404(Organizacion, pk=pk)
	if organizacion.activa == True:
		organizacion.activa = False
		organizacion.save()
	else:
		org = Organizacion.objects.filter(activa=True, administrador=request.user)
		if org:
			org = org.get(activa=True, administrador=request.user)
			org.activa = False
			org.save()
		organizacion.activa = True
		organizacion.save()
	return redirect('detalle_organizacion', pk=organizacion.pk)

def detalle_organizacion(request, pk):
	lista ="valor"
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayorganizacion = Organizacion.objects.filter(administrador=request.user).count()
	if request.method == "POST":
			dic = request.POST
			busqueda = dic["buscar"]
			orden = dic["ordenar"]
			buscarxnombre = Organizacion.objects.filter(nombre_legal__contains=busqueda, administrador=request.user)
			buscarxnumid = Organizacion.objects.filter(numero_identificacion__contains=busqueda, administrador=request.user)
			if buscarxnombre:
				lista = buscarxnombre.order_by(orden)
				lista = reemplazardatos_organizaciones(lista)
			elif buscarxnumid:
				lista = buscarxnumid.order_by(orden)
				lista = reemplazardatos_organizaciones(lista)
			else:
				lista = Organizacion.objects.filter(administrador=request.user).order_by('nombre_legal')
				lista = reemplazardatos_organizaciones(lista)
	organizaciones = Organizacion.objects.filter(administrador=request.user).order_by('nombre_legal')
	organizaciones = reemplazardatos_organizaciones(organizaciones)
	organizacion = get_object_or_404(Organizacion, pk=pk)
	organizacion = reemplazardatos_organizacion(organizacion)
	return render(request, 'groway/detalle_organizacion.html', {'orgactivas':orgactivas, 'organizacion':organizacion, 'organizaciones':organizaciones, 'lista':lista, 'nohayorganizacion':nohayorganizacion})


@login_required
def clientes(request):
	lista ="valor"
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayclientes = Contacto.objects.filter(relacion_activa="CL", org_creadora=orgactivas).count()
	if request.method == "POST":
			dic = request.POST
			busqueda = dic["buscar"]
			orden = dic["ordenar"]
			buscarxnombre = Contacto.objects.filter(nombre_legal__contains=busqueda, relacion_activa="CL", org_creadora=orgactivas)
			buscarxnumid = Contacto.objects.filter(numero_identificacion__contains=busqueda, relacion_activa="CL", org_creadora=orgactivas)
			if buscarxnombre:
				lista = buscarxnombre.order_by(orden)
				lista = reemplazardatos_contactos(lista)
			elif buscarxnumid:
				lista = buscarxnumid.order_by(orden)
				lista = reemplazardatos_contactos(lista)
			else:
				lista = Contacto.objects.filter(relacion_activa="CL", org_creadora=orgactivas).order_by('nombre_legal')
				lista = reemplazardatos_contactos(lista)
	contactos = Contacto.objects.filter(relacion_activa="CL", org_creadora=orgactivas).order_by('nombre_legal')
	contactos = reemplazardatos_contactos(contactos)
	return render(request, 'groway/clientes.html', {'orgactivas':orgactivas, 'contactos':contactos, 'lista':lista, 'nohayclientes':nohayclientes})

def nuevo_cliente(request):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayclientes = Contacto.objects.filter(relacion_activa="CL", org_creadora=orgactivas).count()
	if request.method == "POST":
		form = ContactoForm(request.POST)
		if form.is_valid():
			contacto = form.save(commit=False)
			contacto.relacion_activa = 'CL'
			contacto.activa = True
			contacto.org_creadora = orgactivas
			contacto.save()
			return redirect('detalle_cliente', pk=contacto.pk)
	else:
		form = ContactoForm()
	contactos = Contacto.objects.filter(relacion_activa="CL", org_creadora=orgactivas).order_by('nombre_legal')
	contactos = reemplazardatos_contactos(contactos)
	return render(request, 'groway/nuevo_cliente.html', {'form':form, 'orgactivas':orgactivas, 'contactos':contactos, 'nohayclientes':nohayclientes})

def editar_contacto(request, pk):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayclientes = Contacto.objects.filter(relacion_activa="CL", org_creadora=orgactivas).count()
	nohayproveedores = Contacto.objects.filter(relacion_activa="PD", org_creadora=orgactivas).count()
	contacto = get_object_or_404(Contacto, pk=pk)
	org_contacto = contacto.org_creadora
	relacion_contacto = contacto.relacion_activa
	if request.method == "POST":
		form = ContactoForm(request.POST, instance=contacto)
		if form.is_valid():
			contacto = form.save(commit=False)
			contacto.relacion_activa = relacion_contacto
			contacto.activa = True
			contacto.org_creadora = org_contacto
			contacto.save()
			if contacto.relacion_activa == 'CL':
				return redirect('detalle_cliente', pk=contacto.pk)
			elif contacto.relacion_activa == 'PD':
				return redirect('detalle_proveedor', pk=contacto.pk)
	else:
		form = ContactoForm(instance=contacto)
	if contacto.relacion_activa == "CL":
		contactos = Contacto.objects.filter(relacion_activa="CL", org_creadora=orgactivas).order_by('nombre_legal')
		contactos = reemplazardatos_contactos(contactos)
		return render(request, 'groway/nuevo_cliente.html', {'form':form, 'orgactivas':orgactivas, 'contactos':contactos, 'contacto':contacto, 'nohayclientes':nohayclientes})
	elif contacto.relacion_activa == "PD":
		contactos = Contacto.objects.filter(relacion_activa="PD", org_creadora=orgactivas).order_by('nombre_legal')
		contactos = reemplazardatos_contactos(contactos)
		return render(request, 'groway/nuevo_proveedor.html', {'form':form, 'orgactivas':orgactivas, 'contactos':contactos, 'contacto':contacto, 'nohayproveedores':nohayproveedores})

def eliminar_contacto(request, pk):
	contacto = get_object_or_404(Contacto, pk=pk)
	if contacto.relacion_activa == "CL":
		contacto.delete()
		return redirect('clientes')
	elif contacto.relacion_activa == "PD":
		contacto.delete()
		return redirect('proveedores')


def detalle_cliente(request, pk):
	lista ="valor"
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayclientes = Contacto.objects.filter(relacion_activa="CL", org_creadora=orgactivas).count()
	if request.method == "POST":
			dic = request.POST
			busqueda = dic["buscar"]
			orden = dic["ordenar"]
			buscarxnombre = Contacto.objects.filter(nombre_legal__contains=busqueda, relacion_activa="CL", org_creadora=orgactivas)
			buscarxnumid = Contacto.objects.filter(numero_identificacion__contains=busqueda, relacion_activa="CL", org_creadora=orgactivas)
			if buscarxnombre:
				lista = buscarxnombre.order_by(orden)
				lista = reemplazardatos_contactos(lista)
			elif buscarxnumid:
				lista = buscarxnumid.order_by(orden)
				lista = reemplazardatos_contactos(lista)
			else:
				lista = Contacto.objects.filter(relacion_activa="CL", org_creadora=orgactivas).order_by('nombre_legal')
				lista = reemplazardatos_contactos(lista)
	contactos = Contacto.objects.filter(relacion_activa="CL", org_creadora=orgactivas).order_by('nombre_legal')
	contactos = reemplazardatos_contactos(contactos)
	contacto = get_object_or_404(Contacto, pk=pk)
	contacto = reemplazardatos_contacto(contacto)
	return render(request, 'groway/detalle_cliente.html', {'orgactivas':orgactivas, 'contacto':contacto, 'contactos':contactos, 'lista':lista, 'nohayclientes':nohayclientes})


@login_required
def proveedores(request):
	lista ="valor"
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayproveedores = Contacto.objects.filter(relacion_activa="PD", org_creadora=orgactivas).count()
	if request.method == "POST":
			dic = request.POST
			busqueda = dic["buscar"]
			orden = dic["ordenar"]
			buscarxnombre = Contacto.objects.filter(nombre_legal__contains=busqueda,  relacion_activa="PD", org_creadora=orgactivas)
			buscarxnumid = Contacto.objects.filter(numero_identificacion__contains=busqueda,  relacion_activa="PD", org_creadora=orgactivas)
			if buscarxnombre:
				lista = buscarxnombre.order_by(orden)
				lista = reemplazardatos_contactos(lista)
			elif buscarxnumid:
				lista = buscarxnumid.order_by(orden)
				lista = reemplazardatos_contactos(lista)
			else:
				lista = Contacto.objects.filter(relacion_activa="PD", org_creadora=orgactivas).order_by('nombre_legal')
				lista = reemplazardatos_contactos(lista)
	contactos = Contacto.objects.filter(relacion_activa="PD", org_creadora=orgactivas).order_by('nombre_legal')
	contactos = reemplazardatos_contactos(contactos)
	return render(request, 'groway/proveedores.html', {'orgactivas':orgactivas, 'contactos':contactos, 'lista':lista, 'nohayproveedores':nohayproveedores})

def nuevo_proveedor(request):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayproveedores = Contacto.objects.filter(relacion_activa="PD", org_creadora=orgactivas).count()
	if request.method == "POST":
		form = ContactoForm(request.POST)
		if form.is_valid():
			contacto = form.save(commit=False)
			contacto.relacion_activa = 'PD'
			contacto.activa = True
			contacto.org_creadora = orgactivas
			contacto.save()
			return redirect('detalle_proveedor', pk=contacto.pk)
	else:
		form = ContactoForm()
	contactos = Contacto.objects.filter(relacion_activa="PD", org_creadora=orgactivas).order_by('nombre_legal')
	contactos = reemplazardatos_contactos(contactos)
	return render(request, 'groway/nuevo_proveedor.html', {'form':form, 'orgactivas':orgactivas, 'contactos':contactos, 'nohayproveedores':nohayproveedores})

def detalle_proveedor(request, pk):
	lista ="valor"
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayproveedores = Contacto.objects.filter(relacion_activa="PD", org_creadora=orgactivas).count()
	if request.method == "POST":
			dic = request.POST
			busqueda = dic["buscar"]
			orden = dic["ordenar"]
			buscarxnombre = Contacto.objects.filter(nombre_legal__contains=busqueda,  relacion_activa="PD", org_creadora=orgactivas)
			buscarxnumid = Contacto.objects.filter(numero_identificacion__contains=busqueda,  relacion_activa="PD", org_creadora=orgactivas)
			if buscarxnombre:
				lista = buscarxnombre.order_by(orden)
				lista = reemplazardatos_contactos(lista)
			elif buscarxnumid:
				lista = buscarxnumid.order_by(orden)
				lista = reemplazardatos_contactos(lista)
			else:
				lista = Contacto.objects.filter(relacion_activa="PD", org_creadora=orgactivas).order_by('nombre_legal')
				lista = reemplazardatos_contactos(lista)
	contactos =  Contacto.objects.filter(relacion_activa="PD", org_creadora=orgactivas).order_by('nombre_legal')
	contactos = reemplazardatos_contactos(contactos)
	contacto = get_object_or_404(Contacto, pk=pk)
	contacto = reemplazardatos_contacto(contacto)
	return render(request, 'groway/detalle_proveedor.html', {'orgactivas':orgactivas, 'contacto':contacto, 'contactos':contactos, 'lista':lista, 'nohayproveedores':nohayproveedores})

@login_required
def categorias(request):
	lista ="valor"
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohaycategoria = Categoria.objects.filter(org_creadora=orgactivas).count()
	if request.method == "POST":
			dic = request.POST
			busqueda = dic["buscar"]
			orden = dic["ordenar"]
			buscarxnombre = Categoria.objects.filter(nombre__contains=busqueda, org_creadora=orgactivas)
			buscarxprefijo = Categoria.objects.filter(pre_fijo__contains=busqueda, org_creadora=orgactivas)
			buscarxdestitem = Categoria.objects.filter(destino_item__contains=busqueda, org_creadora=orgactivas)
			if buscarxnombre:
				lista = buscarxnombre.order_by(orden)
				lista = reemplazardatos_categorias(lista)
			elif buscarxprefijo:
				lista = buscarxprefijo.order_by(orden)
				lista = reemplazardatos_categorias(lista)
			elif buscarxdestitem:
				lista = buscarxdestitem.order_by(orden)
				lista = reemplazardatos_categorias(lista)
			else:
				lista = Categoria.objects.filter(org_creadora=orgactivas).order_by('nombre')
				lista = reemplazardatos_categorias(lista)
	categorias = Categoria.objects.filter(org_creadora=orgactivas).order_by('nombre')
	categorias = reemplazardatos_categorias(categorias)
	return render(request, 'groway/categorias.html', {'orgactivas':orgactivas, 'categorias':categorias, 'lista':lista, 'nohaycategoria':nohaycategoria})

def nueva_categoria(request):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohaycategoria = Categoria.objects.filter(org_creadora=orgactivas).count()
	if request.method == "POST":
		form = CategoriaForm(request.POST)
		if form.is_valid():
			categoria = form.save(commit=False)
			categoria.activa = True
			categoria.org_creadora = orgactivas
			categoria.save()
			return redirect('detalle_categoria', pk=categoria.pk)
	else:
		form = CategoriaForm()
	categorias = Categoria.objects.filter(org_creadora=orgactivas).order_by('nombre')
	categorias = reemplazardatos_categorias(categorias)
	return render(request, 'groway/nueva_categoria.html', {'form':form, 'orgactivas':orgactivas, 'categorias':categorias, 'nohaycategoria':nohaycategoria})

def editar_categoria(request, pk):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohaycategoria = Categoria.objects.filter(org_creadora=orgactivas).count()
	categoria = get_object_or_404(Categoria, pk=pk)
	org_categoria = categoria.org_creadora
	if request.method == "POST":
		form = CategoriaForm(request.POST, instance=categoria)
		if form.is_valid():
			categoria = form.save(commit=False)
			categoria.activa = True
			categoria.org_creadora = org_categoria
			categoria.save()
			return redirect('detalle_categoria', pk=categoria.pk)
	else:
		form = CategoriaForm(instance=categoria)
	categorias = Categoria.objects.filter(org_creadora=orgactivas).order_by('nombre')
	categorias = reemplazardatos_categorias(categorias)
	return render(request, 'groway/nueva_categoria.html', {'form':form, 'orgactivas':orgactivas, 'categoria':categoria, 'categorias':categorias, 'nohaycategoria':nohaycategoria})

def eliminar_categoria(request, pk):
	categoria = get_object_or_404(Categoria, pk=pk)
	categoria.delete()
	return redirect('categorias')

def detalle_categoria(request, pk):
	lista ="valor"
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohaycategoria = Categoria.objects.filter(org_creadora=orgactivas).count()
	if request.method == "POST":
			dic = request.POST
			busqueda = dic["buscar"]
			orden = dic["ordenar"]
			buscarxnombre = Categoria.objects.filter(nombre__contains=busqueda, org_creadora=orgactivas)
			buscarxprefijo = Categoria.objects.filter(pre_fijo__contains=busqueda, org_creadora=orgactivas)
			buscarxdestitem = Categoria.objects.filter(destino_item__contains=busqueda, org_creadora=orgactivas)
			if buscarxnombre:
				lista = buscarxnombre.order_by(orden)
				lista = reemplazardatos_categorias(lista)
			elif buscarxprefijo:
				lista = buscarxprefijo.order_by(orden)
				lista = reemplazardatos_categorias(lista)
			elif buscarxdestitem:
				lista = buscarxdestitem.order_by(orden)
				lista = reemplazardatos_categorias(lista)
			else:
				lista = Categoria.objects.filter(org_creadora=orgactivas).order_by('nombre')
				lista = reemplazardatos_categorias(lista)
	categorias = Categoria.objects.filter(org_creadora=orgactivas).order_by('nombre')
	categorias = reemplazardatos_categorias(categorias)
	categoria = get_object_or_404(Categoria, pk=pk)
	categoria = reemplazardatos_categoria(categoria)
	return render(request, 'groway/detalle_categoria.html', {'orgactivas':orgactivas, 'categoria':categoria, 'categorias':categorias, 'lista':lista, 'nohaycategoria':nohaycategoria})

@login_required
def items(request):
	lista ="valor"
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayitems = Item.objects.filter(org_creadora=orgactivas).count()
	nohaycategoria = Categoria.objects.filter(destino_item='IV', org_creadora=orgactivas).count()
	if request.method == "POST":
			dic = request.POST
			busqueda = dic["buscar"]
			orden = dic["ordenar"]
			buscarxcodigo = Item.objects.filter(codigo__contains=busqueda, org_creadora=orgactivas)
			buscarxdescrip = Item.objects.filter(descripcion__contains=busqueda, org_creadora=orgactivas)
			buscarxprecio = Item.objects.filter(precio_venta__contains=busqueda, org_creadora=orgactivas)
			if buscarxcodigo:
				lista = buscarxcodigo.order_by(orden)
				lista = reemplazardatos_items(lista)
			elif buscarxdescrip:
				lista = buscarxdescrip.order_by(orden)
				lista = reemplazardatos_items(lista)
			elif buscarxprecio:
				lista = buscarxprecio.order_by(orden)
				lista = reemplazardatos_items(lista)
			else:
				lista = Item.objects.filter(org_creadora=orgactivas).order_by('-codigo')
				lista = reemplazardatos_items(lista)
	items = Item.objects.filter(org_creadora=orgactivas).order_by('-codigo')
	items = reemplazardatos_items(items)
	return render(request, 'groway/items.html', {'orgactivas':orgactivas, 'items':items, 'lista':lista, 'nohayitems':nohayitems, 'nohaycategoria':nohaycategoria})

def nuevo_item(request):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayitems = Item.objects.filter(org_creadora=orgactivas).count()
	nohaycategoria = Categoria.objects.filter(destino_item='IV', org_creadora=orgactivas).count()
	categorias_item = Categoria.objects.filter(destino_item='IV', org_creadora=orgactivas).order_by('nombre')
	if request.method == "POST":
		form = ItemForm(request.POST, request.FILES)
		dic = request.POST
		categ = dic["categoria_item"]
		if form.is_valid():
			item = form.save(commit=False)
			item.activa = True
			item.categoria = categ
			item.org_creadora = orgactivas
			item.save()
			item.auto_codigo()
			return redirect('detalle_item', pk=item.pk)
	else:
		form = ItemForm()
	items = Item.objects.filter(org_creadora=orgactivas).order_by('-codigo')
	items = reemplazardatos_items(items)
	return render(request, 'groway/nuevo_item.html', {'form':form, 'orgactivas':orgactivas, 'categorias_item':categorias_item, 'items':items, 'nohayitems':nohayitems, 'nohaycategoria':nohaycategoria})

def editar_item(request, pk):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayitems = Item.objects.filter(org_creadora=orgactivas).count()
	nohaycategoria = Categoria.objects.filter(destino_item='IV', org_creadora=orgactivas).count()
	categorias_item = Categoria.objects.filter(destino_item='IV', org_creadora=orgactivas)
	item = get_object_or_404(Item, pk=pk)
	if request.method == "POST":
		form = ItemForm(request.POST, request.FILES, instance=item)
		dic = request.POST
		categ = dic["categoria_item"]
		if form.is_valid():
			item = form.save(commit=False)
			item.activa = True
			item.categoria = categ
			item.org_creadora = orgactivas
			item.auto_codigo()
			item.save()
			return redirect('detalle_item', pk=item.pk)
	else:
		form = ItemForm(instance=item)
	items = Item.objects.filter(org_creadora=orgactivas).order_by('-codigo')
	items = reemplazardatos_items(items)
	return render(request, 'groway/nuevo_item.html', {'form':form, 'orgactivas':orgactivas, 'categorias_item':categorias_item, 'item':item, 'items':items, 'nohayitems':nohayitems, 'nohaycategoria':nohaycategoria})


def eliminar_item(request, pk):
	item = get_object_or_404(Item, pk=pk)
	item.delete()
	return redirect('items')

def detalle_item(request, pk):
	lista ="valor"
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayitems = Item.objects.filter(org_creadora=orgactivas).count()
	nohaycategoria = Categoria.objects.filter(destino_item='IV', org_creadora=orgactivas).count()
	if request.method == "POST":
			dic = request.POST
			busqueda = dic["buscar"]
			orden = dic["ordenar"]
			buscarxcodigo = Item.objects.filter(codigo__contains=busqueda, org_creadora=orgactivas)
			buscarxdescrip = Item.objects.filter(descripcion__contains=busqueda, org_creadora=orgactivas)
			buscarxprecio = Item.objects.filter(precio_venta__contains=busqueda, org_creadora=orgactivas)
			if buscarxcodigo:
				lista = buscarxcodigo.order_by(orden)
				lista = reemplazardatos_items(lista)
			elif buscarxdescrip:
				lista = buscarxdescrip.order_by(orden)
				lista = reemplazardatos_items(lista)
			elif buscarxprecio:
				lista = buscarxprecio.order_by(orden)
				lista = reemplazardatos_items(lista)
			else:
				lista = Item.objects.filter(org_creadora=orgactivas).order_by('-codigo')
				lista = reemplazardatos_items(lista)
	items = Item.objects.filter(org_creadora=orgactivas).order_by('-codigo')
	items = reemplazardatos_items(items)
	item = get_object_or_404(Item, pk=pk)
	item = reemplazardatos_item(item)
	return render(request, 'groway/detalle_item.html', {'orgactivas':orgactivas, 'item':item, 'items':items, 'lista':lista, 'nohayitems':nohayitems, 'nohaycategoria':nohaycategoria})

@login_required
def insumos(request):
	lista ="valor"
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayinsumo = Insumo.objects.filter(org_creadora=orgactivas).count()
	nohaycategoria = Categoria.objects.filter(destino_item='IM', org_creadora=orgactivas).count()
	if request.method == "POST":
			dic = request.POST
			busqueda = dic["buscar"]
			orden = dic["ordenar"]
			buscarxcodigo = Insumo.objects.filter(codigo__contains=busqueda, org_creadora=orgactivas)
			buscarxdescrip = Insumo.objects.filter(descripcion__contains=busqueda, org_creadora=orgactivas)
			buscarxprecio = Insumo.objects.filter(precio_compra__contains=busqueda, org_creadora=orgactivas)
			if buscarxcodigo:
				lista = buscarxcodigo.order_by(orden)
				lista = reemplazardatos_insumos(lista)
			elif buscarxdescrip:
				lista = buscarxdescrip.order_by(orden)
				lista = reemplazardatos_insumos(lista)
			elif buscarxprecio:
				lista = buscarxprecio.order_by(orden)
				lista = reemplazardatos_insumos(lista)
			else:
				lista = Insumo.objects.filter(org_creadora=orgactivas).order_by('-codigo')
				lista = reemplazardatos_contactos(lista)
	insumos = Insumo.objects.filter(org_creadora=orgactivas).order_by('-codigo')
	insumos = reemplazardatos_insumos(insumos)
	return render(request, 'groway/insumos.html', {'orgactivas':orgactivas, 'insumos':insumos, 'lista':lista, 'nohayinsumo':nohayinsumo, 'nohaycategoria':nohaycategoria})

def nuevo_insumo(request):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayinsumo = Insumo.objects.filter(org_creadora=orgactivas).count()
	nohaycategoria = Categoria.objects.filter(destino_item='IM', org_creadora=orgactivas).count()
	categorias_insumo = Categoria.objects.filter(destino_item='IM', org_creadora=orgactivas).order_by('nombre')
	if request.method == "POST":
		form = InsumoForm(request.POST, request.FILES)
		dic = request.POST
		categ = dic["categoria_insumo"]
		if form.is_valid():
			insumo = form.save(commit=False)
			insumo.activa = True
			insumo.categoria = categ
			insumo.org_creadora = orgactivas
			insumo.save()
			insumo.auto_codigo()
			return redirect('detalle_insumo', pk=insumo.pk)
	else:
		form = InsumoForm()
	insumos = Insumo.objects.filter(org_creadora=orgactivas).order_by('-codigo')
	insumos = reemplazardatos_insumos(insumos)
	return render(request, 'groway/nuevo_insumo.html', {'form':form, 'orgactivas':orgactivas, 'categorias_insumo':categorias_insumo, 'insumos':insumos, 'nohayinsumo':nohayinsumo, 'nohaycategoria':nohaycategoria})

def editar_insumo(request, pk):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayinsumo = Insumo.objects.filter(org_creadora=orgactivas).count()
	nohaycategoria = Categoria.objects.filter(destino_item='IM', org_creadora=orgactivas).count()
	categorias_insumo = Categoria.objects.filter(destino_item='IM', org_creadora=orgactivas).order_by('nombre')
	insumo = get_object_or_404(Insumo, pk=pk)
	if request.method == "POST":
		form = InsumoForm(request.POST, request.FILES, instance=insumo)
		dic = request.POST
		categ = dic["categoria_insumo"]
		if form.is_valid():
			insumo = form.save(commit=False)
			insumo.activa = True
			insumo.categoria = categ
			insumo.org_creadora = orgactivas
			insumo.auto_codigo()
			insumo.save()
			return redirect('detalle_insumo', pk=insumo.pk)
	else:
		form = InsumoForm(instance=insumo)
	insumos = Insumo.objects.filter(org_creadora=orgactivas).order_by('-codigo')
	insumos = reemplazardatos_insumos(insumos)
	return render(request, 'groway/nuevo_insumo.html', {'form':form, 'orgactivas':orgactivas, 'categorias_insumo':categorias_insumo, 'insumo':insumo, 'insumos':insumos, 'nohayinsumo':nohayinsumo, 'nohaycategoria':nohaycategoria})

def eliminar_insumo(request, pk):
	insumo = get_object_or_404(Insumo, pk=pk)
	insumo.delete()
	return redirect('insumos')

def detalle_insumo(request, pk):
	lista ="valor"
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayinsumo = Insumo.objects.filter(org_creadora=orgactivas).count()
	nohaycategoria = Categoria.objects.filter(org_creadora=orgactivas).count()
	if request.method == "POST":
			dic = request.POST
			busqueda = dic["buscar"]
			orden = dic["ordenar"]
			buscarxcodigo = Insumo.objects.filter(codigo__contains=busqueda, org_creadora=orgactivas)
			buscarxdescrip = Insumo.objects.filter(descripcion__contains=busqueda, org_creadora=orgactivas)
			buscarxprecio = Insumo.objects.filter(precio_compra__contains=busqueda, org_creadora=orgactivas)
			if buscarxcodigo:
				lista = buscarxcodigo.order_by(orden)
				lista = reemplazardatos_insumos(lista)
			elif buscarxdescrip:
				lista = buscarxdescrip.order_by(orden)
				lista = reemplazardatos_insumos(lista)
			elif buscarxprecio:
				lista = buscarxprecio.order_by(orden)
				lista = reemplazardatos_insumos(lista)
			else:
				lista = Insumo.objects.filter(org_creadora=orgactivas).order_by('-codigo')
				lista = reemplazardatos_insumos(lista)
	insumos = Insumo.objects.filter(org_creadora=orgactivas).order_by('-codigo')
	insumos = reemplazardatos_insumos(insumos)
	insumo = get_object_or_404(Insumo, pk=pk)
	insumo = reemplazardatos_insumo(insumo)
	return render(request, 'groway/detalle_insumo.html', {'orgactivas':orgactivas, 'insumo':insumo, 'insumos':insumos, 'lista':lista, 'nohayinsumo':nohayinsumo, 'nohaycategoria':nohaycategoria})

@login_required
def consecutivos(request):
	lista ="valor"
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayconsecutivo = Consecutivo_documento.objects.filter(org_creadora=orgactivas, generado=True).count()
	if request.method == "POST":
			dic = request.POST
			busqueda = dic["buscar"]
			orden = dic["ordenar"]
			buscarxprefijo = Consecutivo_documento.objects.filter(pre_fijo__contains=busqueda, org_creadora=orgactivas, generado=True)
			buscarxtipodoc = Consecutivo_documento.objects.filter(tipo_de_documento__contains=busqueda, org_creadora=orgactivas, generado=True)
			if buscarxprefijo:
				lista = buscarxprefijo.order_by(orden)
				lista = reemplazardatos_consecutivos(lista)
			elif buscarxtipodoc:
				lista = buscarxtipodoc.order_by(orden)
				lista = reemplazardatos_consecutivos(lista)
			else:
				lista = Consecutivo_documento.objects.filter(org_creadora=orgactivas, generado=True).order_by('pre_fijo')
				lista = reemplazardatos_consecutivos(lista)
	consecutivos = Consecutivo_documento.objects.filter(org_creadora=orgactivas, generado=True).order_by('pre_fijo')
	consecutivos = reemplazardatos_consecutivos(consecutivos)
	return render(request, 'groway/consecutivos.html', {'orgactivas':orgactivas, 'consecutivos':consecutivos, 'lista':lista, 'nohayconsecutivo':nohayconsecutivo})

def nuevo_consecutivo_ing(request):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayconsecutivo = Consecutivo_documento.objects.filter(org_creadora=orgactivas, generado=True).count()
	edit_form = False
	consecutivoborrador = Consecutivo_documento.objects.filter(org_creadora=orgactivas, generado=False).last()
	if request.method == "POST":
		if consecutivoborrador:
			form = Consecutivo_documentoForm(request.POST, instance=consecutivoborrador)
		else:
			form = Consecutivo_documentoForm(request.POST)
		if form.is_valid():
			consecutivo = form.save(commit=False)
			consecutivo.save()
			if Consecutivo_documento.objects.filter(tipo_de_documento=consecutivo.tipo_de_documento, org_creadora=orgactivas, generado=True).count() < 1:
				consecutivo.save()
				return redirect('nuevo_consecutivo_fin', pk=consecutivo.pk)
			else:
				consecutivo.delete()
				return redirect('nuevo_consecutivo_ing')
	else:
		form = Consecutivo_documentoForm()
	consecutivos = Consecutivo_documento.objects.filter(org_creadora=orgactivas, generado=True).order_by('pre_fijo')
	consecutivos = reemplazardatos_consecutivos(consecutivos)
	return render(request, 'groway/nuevo_consecutivo.html', {'form':form, 'orgactivas':orgactivas, 'edit_form':edit_form, 'consecutivos':consecutivos, 'nohayconsecutivo':nohayconsecutivo})

def nuevo_consecutivo_fin(request, pk):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayconsecutivo = Consecutivo_documento.objects.filter(org_creadora=orgactivas, generado=True).count()
	consecutivo = get_object_or_404(Consecutivo_documento, pk=pk)
	edit_form = False
	if request.method == "POST":
		form = Consecutivo_documentoForm(request.POST, instance=consecutivo)
		if form.is_valid():
			consecutivo = form.save(commit=False)
			consecutivo.generado = True
			consecutivo.org_creadora = orgactivas
			if consecutivo.tipo_de_documento == 'FVE':
				if consecutivo.numero == 1:
					consecutivo.numero = consecutivo.num_inicio
			consecutivo.auto_codigo()
			consecutivo.save()
			return redirect('detalle_consecutivo', pk=consecutivo.pk)
	else:
		form = Consecutivo_documentoForm(instance=consecutivo)
	consecutivos = Consecutivo_documento.objects.filter(org_creadora=orgactivas, generado=True).order_by('pre_fijo')
	consecutivos = reemplazardatos_consecutivos(consecutivos)
	return render(request, 'groway/nuevo_consecutivo.html', {'form':form, 'orgactivas':orgactivas, 'edit_form':edit_form, 'consecutivo':consecutivo, 'consecutivos':consecutivos, 'nohayconsecutivo':nohayconsecutivo})

def editar_consecutivo(request, pk):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayconsecutivo = Consecutivo_documento.objects.filter(org_creadora=orgactivas, generado=True).count()
	consecutivo = get_object_or_404(Consecutivo_documento, pk=pk)
	edit_form = True
	if request.method == "POST":
		form = Consecutivo_documentoForm(request.POST, instance=consecutivo)
		if form.is_valid():
			consecutivo = form.save(commit=False)
			consecutivo.activa = True
			consecutivo.generado = True
			if consecutivo.tipo_de_documento == 'FVE':
				if consecutivo.numero == 1:
					consecutivo.numero = consecutivo.num_inicio
			consecutivo.save()
			if Consecutivo_documento.objects.filter(tipo_de_documento=consecutivo.tipo_de_documento, org_creadora=orgactivas, generado=True).count() <= 1:
				consecutivo.org_creadora = orgactivas
				consecutivo.auto_codigo()
				consecutivo.save()
				return redirect('detalle_consecutivo', pk=consecutivo.pk)
			else:
				consecutivo.delete()
				return redirect('nuevo_consecutivo_ing')
	else:
		form = Consecutivo_documentoForm(instance=consecutivo)
	consecutivos = Consecutivo_documento.objects.filter(org_creadora=orgactivas, generado=True).order_by('pre_fijo')
	consecutivos = reemplazardatos_consecutivos(consecutivos)
	consecutivo = get_object_or_404(Consecutivo_documento, pk=pk)
	consecutivo = reemplazardatos_consecutivo(consecutivo)
	return render(request, 'groway/nuevo_consecutivo.html', {'form':form, 'orgactivas':orgactivas, 'edit_form':edit_form, 'consecutivo':consecutivo, 'consecutivos':consecutivos, 'nohayconsecutivo':nohayconsecutivo})

def eliminar_consecutivo(request, pk):
	consecutivo = get_object_or_404(Consecutivo_documento, pk=pk)
	consecutivo.delete()
	return redirect('consecutivos')


def detalle_consecutivo(request, pk):
	lista ="valor"
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayconsecutivo = Consecutivo_documento.objects.filter(org_creadora=orgactivas, generado=True).count()
	if request.method == "POST":
		dic = request.POST
		busqueda = dic["buscar"]
		orden = dic["ordenar"]
		buscarxprefijo = Consecutivo_documento.objects.filter(pre_fijo__contains=busqueda, org_creadora=orgactivas, generado=True)
		buscarxtipodoc = Consecutivo_documento.objects.filter(tipo_de_documento__contains=busqueda, org_creadora=orgactivas, generado=True)
		if buscarxprefijo:
			lista = buscarxprefijo.order_by(orden)
			lista = reemplazardatos_consecutivos(lista)
		elif buscarxtipodoc:
			lista = buscarxtipodoc.order_by(orden)
			lista = reemplazardatos_consecutivos(lista)
		else:
			lista = Consecutivo_documento.objects.filter(org_creadora=orgactivas, generado=True).order_by('pre_fijo')
			lista = reemplazardatos_consecutivos(lista)
	consecutivos = Consecutivo_documento.objects.filter(org_creadora=orgactivas, generado=True).order_by('pre_fijo')
	consecutivos = reemplazardatos_consecutivos(consecutivos)
	consecutivo = get_object_or_404(Consecutivo_documento, pk=pk)
	consecutivo = reemplazardatos_consecutivo(consecutivo)
	return render(request, 'groway/detalle_consecutivo.html', {'orgactivas':orgactivas, 'consecutivo':consecutivo, 'consecutivos':consecutivos, 'lista':lista, 'nohayconsecutivo':nohayconsecutivo})

@login_required
def terminos_de_pago(request):
	lista ="valor"
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayterminospago = Termino_de_pago.objects.filter(org_creadora=orgactivas).count()
	if request.method == "POST":
			dic = request.POST
			busqueda = dic["buscar"]
			orden = dic["ordenar"]
			buscarxcodigo = Termino_de_pago.objects.filter(codigo__contains=busqueda, org_creadora=orgactivas)
			buscarxdescrip = Termino_de_pago.objects.filter(descripcion__contains=busqueda, org_creadora=orgactivas)
			if buscarxcodigo:
				lista = buscarxcodigo.order_by(orden)
				lista = reemplazardatos_terminospago(lista)
			elif buscarxdescrip:
				lista = buscarxdescrip.order_by(orden)
				lista = reemplazardatos_terminospago(lista)
			else:
				lista = Termino_de_pago.objects.filter(org_creadora=orgactivas).order_by('plazo_dias')
				lista = reemplazardatos_terminospago(lista)
	terminospago = Termino_de_pago.objects.filter(org_creadora=orgactivas).order_by('plazo_dias')
	terminospago = reemplazardatos_terminospago(terminospago)
	return render(request, 'groway/terminos_de_pago.html', {'orgactivas':orgactivas, 'terminospago':terminospago, 'lista':lista, 'nohayterminospago':nohayterminospago})

def nuevo_termino_de_pago(request):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayterminospago = Termino_de_pago.objects.filter(org_creadora=orgactivas).count()
	if request.method == "POST":
		form = Termino_de_pagoForm(request.POST)
		if form.is_valid():
			terminopago = form.save(commit=False)
			terminopago.activa = True
			terminopago.org_creadora = orgactivas
			terminopago.save()
			terminopago.auto_codigo()
			return redirect('detalle_termino_de_pago', pk=terminopago.pk)
	else:
		form = Termino_de_pagoForm()
	terminospago = Termino_de_pago.objects.filter(org_creadora=orgactivas).order_by('plazo_dias')
	terminospago = reemplazardatos_terminospago(terminospago)
	return render(request, 'groway/nuevo_termino_de_pago.html', {'form':form, 'orgactivas':orgactivas, 'terminospago':terminospago, 'nohayterminospago':nohayterminospago})

def editar_termino_de_pago(request, pk):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayterminospago = Termino_de_pago.objects.filter(org_creadora=orgactivas).count()
	terminopago = get_object_or_404(Termino_de_pago, pk=pk)
	codigo_termino = terminopago.codigo
	org_terminopago = terminopago.org_creadora
	if request.method == "POST":
		form = Termino_de_pagoForm(request.POST, instance=terminopago)
		if form.is_valid():
			terminopago = form.save(commit=False)
			terminopago.activa = True
			terminopago.codigo = codigo_termino
			terminopago.org_creadora = org_terminopago
			terminopago.save()
			return redirect('detalle_termino_de_pago', pk=terminopago.pk)
	else:
		form = Termino_de_pagoForm(instance=terminopago)
	terminospago = Termino_de_pago.objects.filter(org_creadora=orgactivas).order_by('plazo_dias')
	terminospago = reemplazardatos_terminospago(terminospago)
	return render(request, 'groway/nuevo_termino_de_pago.html', {'form':form, 'orgactivas':orgactivas, 'terminopago':terminopago, 'terminospago':terminospago, 'nohayterminospago':nohayterminospago})

def eliminar_termino_de_pago(request, pk):
	terminopago = get_object_or_404(Termino_de_pago, pk=pk)
	terminopago.delete()
	return redirect('terminos_de_pago')

def detalle_termino_de_pago(request, pk):
	lista ="valor"
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayterminospago = Termino_de_pago.objects.filter(org_creadora=orgactivas).count()
	if request.method == "POST":
			dic = request.POST
			busqueda = dic["buscar"]
			orden = dic["ordenar"]
			buscarxcodigo = Termino_de_pago.objects.filter(codigo__contains=busqueda, org_creadora=orgactivas)
			buscarxdescrip = Termino_de_pago.objects.filter(descripcion__contains=busqueda, org_creadora=orgactivas)
			if buscarxcodigo:
				lista = buscarxcodigo.order_by(orden)
				lista = reemplazardatos_terminospago(lista)
			elif buscarxdescrip:
				lista = buscarxdescrip.order_by(orden)
				lista = reemplazardatos_terminospago(lista)
			else:
				lista = Termino_de_pago.objects.filter(org_creadora=orgactivas).order_by('plazo_dias')
				lista = reemplazardatos_terminospago(lista)
	terminospago = Termino_de_pago.objects.filter(org_creadora=orgactivas).order_by('plazo_dias')
	terminospago = reemplazardatos_terminospago(terminospago)
	terminopago = get_object_or_404(Termino_de_pago, pk=pk)
	terminopago = reemplazardatos_terminopago(terminopago)
	return render(request, 'groway/detalle_termino_de_pago.html', {'orgactivas':orgactivas, 'terminopago':terminopago, 'terminospago':terminospago, 'lista':lista, 'nohayterminospago':nohayterminospago})


@login_required
def cotizaciones(request):
	lista ="valor"
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayclientes = Contacto.objects.filter(relacion_activa="CL", org_creadora=orgactivas).count()
	nohayitems = Item.objects.filter(org_creadora=orgactivas).count()
	nohayconsecutivo = Consecutivo_documento.objects.filter(tipo_de_documento='CZN', org_creadora=orgactivas).count()
	nohayterminospago = Termino_de_pago.objects.filter(org_creadora=orgactivas).count()
	nohaycotizaciones = Cotizacion.objects.filter(org_creadora=orgactivas, generado=True).count()
	if request.method == "POST":
			dic = request.POST
			busqueda = dic["buscar"]
			orden = dic["ordenar"]
			buscarxfecha = Cotizacion.objects.filter(fecha_emision__contains=busqueda, org_creadora=orgactivas, generado=True)
			buscarxconsec = Cotizacion.objects.filter(consecutivo_interno__contains=busqueda, org_creadora=orgactivas, generado=True)
			buscarxcliente = Cotizacion.objects.filter(nombre_cliente__contains=busqueda, org_creadora=orgactivas, generado=True)
			buscarxtotal = Cotizacion.objects.filter(total_documento__contains=busqueda, org_creadora=orgactivas, generado=True)
			if buscarxfecha:
				lista = buscarxfecha.order_by(orden)
				lista = reemplazardatos_cotizaciones(lista)
			elif buscarxconsec:
				lista = buscarxconsec.order_by(orden)
				lista = reemplazardatos_cotizaciones(lista)
			elif buscarxcliente:
				lista = buscarxcliente.order_by(orden)
				lista = reemplazardatos_cotizaciones(lista)
			elif buscarxtotal:
				lista = buscarxtotal.order_by(orden)
				lista = reemplazardatos_cotizaciones(lista)
			else:
				lista = Cotizacion.objects.filter(org_creadora=orgactivas, generado=True).order_by('-consecutivo_interno')
				lista = reemplazardatos_cotizaciones(lista)
	cotizaciones = Cotizacion.objects.filter(org_creadora=orgactivas, generado=True).order_by('-consecutivo_interno')
	cotizaciones = reemplazardatos_cotizaciones(cotizaciones)
	return render(request, 'groway/cotizaciones.html', {'orgactivas':orgactivas, 'cotizaciones':cotizaciones, 'lista':lista, 'nohaycotizaciones':nohaycotizaciones, 'nohayterminospago':nohayterminospago, 'nohayconsecutivo':nohayconsecutivo,
		'nohayitems':nohayitems, 'nohayclientes':nohayclientes})

def nueva_cotizacion_ing(request):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	terminospago_cotiz = Termino_de_pago.objects.filter(org_creadora=orgactivas).order_by('plazo_dias')
	clientes_cotiz = Contacto.objects.filter(relacion_activa="CL", org_creadora=orgactivas).order_by('nombre_legal')
	items_cotiz = Item.objects.filter(org_creadora=orgactivas).order_by('codigo')
	nohayclientes = Contacto.objects.filter(relacion_activa="CL", org_creadora=orgactivas).count()
	nohayitems = Item.objects.filter(org_creadora=orgactivas).count()
	nohayconsecutivo = Consecutivo_documento.objects.filter(tipo_de_documento='CZN', org_creadora=orgactivas).count()
	nohayterminospago = Termino_de_pago.objects.filter(org_creadora=orgactivas).count()
	nohaycotizaciones = Cotizacion.objects.filter(org_creadora=orgactivas, generado=True).count()
	documentoborrador = Cotizacion.objects.filter(org_creadora=orgactivas, generado=False).last()
	if request.method == "POST":
		if documentoborrador:
			form = CotizacionForm(request.POST, instance=documentoborrador)
		else:
			form = CotizacionForm(request.POST)
		dic = request.POST
		termin = dic["terminospago_cotiz"]
		client = dic["clientes_cotiz"]
		item_1 = dic["items_1"]
		item_2 = dic["items_2"]
		item_3 = dic["items_3"]
		item_4 = dic["items_4"]
		item_5 = dic["items_5"]
		if form.is_valid():
			cotizacion = form.save(commit=False)
			cotizacion.org_creadora = orgactivas
			cotizacion.vendedor = request.user
			cotizacion.terminos_de_pago = termin
			cotizacion.cliente = client
			if item_1 != '0':
				cotizacion.item_1 = item_1
			if item_2 != '0':
				cotizacion.item_2 = item_2
			if item_3 != '0':
				cotizacion.item_3 = item_3
			if item_4 != '0':
				cotizacion.item_4 = item_4
			if item_5 != '0':
				cotizacion.item_5 = item_5
			cotizacion.auto_info_organizacion()
			cotizacion.auto_info_cliente()
			cotizacion.info_item()
			cotizacion.save()
			return redirect('nueva_cotizacion_cal', pk=cotizacion.pk)
	else:
		form = CotizacionForm()
	cotizaciones = Cotizacion.objects.filter(org_creadora=orgactivas, generado=True).order_by('-consecutivo_interno')
	cotizaciones = reemplazardatos_cotizaciones(cotizaciones)
	return render(request, 'groway/nueva_cotizacion.html', {'form':form, 'orgactivas':orgactivas, 'cotizaciones':cotizaciones, 'nohaycotizaciones':nohaycotizaciones, 'nohayterminospago':nohayterminospago, 'nohayconsecutivo':nohayconsecutivo,
		'items_cotiz':items_cotiz, 'clientes_cotiz':clientes_cotiz, 'terminospago_cotiz':terminospago_cotiz, 'nohayitems':nohayitems, 'nohayclientes':nohayclientes})

def nueva_cotizacion_cal(request, pk):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	terminospago_cotiz = Termino_de_pago.objects.filter(org_creadora=orgactivas).order_by('plazo_dias')
	clientes_cotiz = Contacto.objects.filter(relacion_activa="CL", org_creadora=orgactivas).order_by('nombre_legal')
	items_cotiz = Item.objects.filter(org_creadora=orgactivas).order_by('codigo')
	nohayclientes = Contacto.objects.filter(relacion_activa="CL", org_creadora=orgactivas).count()
	nohayitems = Item.objects.filter(org_creadora=orgactivas).count()
	nohayconsecutivo = Consecutivo_documento.objects.filter(tipo_de_documento='CZN', org_creadora=orgactivas).count()
	nohayterminospago = Termino_de_pago.objects.filter(org_creadora=orgactivas).count()
	nohaycotizaciones = Cotizacion.objects.filter(org_creadora=orgactivas, generado=True).count()
	cotizacion = get_object_or_404(Cotizacion, pk=pk)
	if request.method == "POST":
		form = CotizacionForm(request.POST, instance=cotizacion)
		dic = request.POST
		termin = dic["terminospago_cotiz"]
		client = dic["clientes_cotiz"]
		item_1 = dic["items_1"]
		item_2 = dic["items_2"]
		item_3 = dic["items_3"]
		item_4 = dic["items_4"]
		item_5 = dic["items_5"]
		if form.is_valid():
			cotizacion = form.save(commit=False)
			if cotizacion.cantidad_1:
				cotizacion.org_creadora = orgactivas
				cotizacion.fecha_emision = timezone.now()
				cotizacion.vendedor = request.user
				cotizacion.terminos_de_pago = termin
				cotizacion.cliente = client
				if item_1 != '0':
					cotizacion.item_1 = item_1
				if item_2 != '0':
					cotizacion.item_2 = item_2
				if item_3 != '0':
					cotizacion.item_3 = item_3
				if item_4 != '0':
					cotizacion.item_4 = item_4
				if item_5 != '0':
					cotizacion.item_5 = item_5
				cotizacion.info_item()
				cotizacion.auto_info_organizacion()
				cotizacion.auto_info_cliente()
				cotizacion.calculo_item()
				cotizacion.calculo_total_cotizacion()
				cotizacion.save()
				return redirect('nueva_cotizacion_cal', pk=cotizacion.pk)
			else:
				return redirect('nueva_cotizacion_cal', pk=cotizacion.pk)
	else:
		form = CotizacionForm(instance=cotizacion)
	cotizaciones = Cotizacion.objects.filter(org_creadora=orgactivas, generado=True).order_by('-consecutivo_interno')
	cotizaciones = reemplazardatos_cotizaciones(cotizaciones)
	return render(request, 'groway/nueva_cotizacion.html', {'form':form, 'orgactivas':orgactivas, 'cotizaciones':cotizaciones, 'cotizacion':cotizacion, 'nohaycotizaciones':nohaycotizaciones, 'nohayterminospago':nohayterminospago, 'nohayconsecutivo':nohayconsecutivo,
		'items_cotiz':items_cotiz, 'clientes_cotiz':clientes_cotiz, 'terminospago_cotiz':terminospago_cotiz, 'nohayitems':nohayitems, 'nohayclientes':nohayclientes})

def nueva_cotizacion_fin(request, pk):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	cotizacion = get_object_or_404(Cotizacion, pk=pk)
	cotizacion.org_creadora = orgactivas
	cotizacion.fecha_emision = timezone.now()
	cotizacion.save()
	cotizacion.tipo_impuestodoc()
	cotizacion.auto_consecutivo()
	cotizacion.generado = True
	cotizacion.save()
	return redirect('detalle_cotizacion', pk=pk)

def atras_cotizacion(request, pk):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	terminospago_cotiz = Termino_de_pago.objects.filter(org_creadora=orgactivas).order_by('plazo_dias')
	clientes_cotiz = Contacto.objects.filter(relacion_activa="CL", org_creadora=orgactivas).order_by('nombre_legal')
	items_cotiz = Item.objects.filter(org_creadora=orgactivas).order_by('codigo')
	nohayclientes = Contacto.objects.filter(relacion_activa="CL", org_creadora=orgactivas).count()
	nohayitems = Item.objects.filter(org_creadora=orgactivas).count()
	nohayconsecutivo = Consecutivo_documento.objects.filter(tipo_de_documento='CZN', org_creadora=orgactivas).count()
	nohayterminospago = Termino_de_pago.objects.filter(org_creadora=orgactivas).count()
	nohaycotizaciones = Cotizacion.objects.filter(org_creadora=orgactivas, generado=True).count()
	cotizacion = get_object_or_404(Cotizacion, pk=pk)
	if request.method == "POST":
		form = CotizacionForm(request.POST, instance=cotizacion)
		dic = request.POST
		termin = dic["terminospago_cotiz"]
		client = dic["clientes_cotiz"]
		item_1 = dic["items_1"]
		item_2 = dic["items_2"]
		item_3 = dic["items_3"]
		item_4 = dic["items_4"]
		item_5 = dic["items_5"]
		if form.is_valid():
			cotizacion = form.save(commit=False)
			cotizacion.vendedor = request.user
			cotizacion.org_creadora = orgactivas
			cotizacion.terminos_de_pago = termin
			cotizacion.cliente = client
			if item_1 != '0':
				cotizacion.item_1 = item_1
			if item_2 != '0':
				cotizacion.item_2 = item_2
			if item_3 != '0':
				cotizacion.item_3 = item_3
			if item_4 != '0':
				cotizacion.item_4 = item_4
			if item_5 != '0':
				cotizacion.item_5 = item_5
			cotizacion.auto_info_organizacion()
			cotizacion.auto_info_cliente()
			cotizacion.info_item()
			cotizacion.save()
			return redirect('nueva_cotizacion_cal', pk=cotizacion.pk)
	else:
		form = CotizacionForm(instance=cotizacion)
	cotizaciones = Cotizacion.objects.filter(org_creadora=orgactivas, generado=True).order_by('-consecutivo_interno')
	cotizaciones = reemplazardatos_cotizaciones(cotizaciones)
	return render(request, 'groway/nueva_cotizacion.html', {'form':form, 'orgactivas':orgactivas, 'cotizaciones':cotizaciones, 'nohaycotizaciones':nohaycotizaciones, 'nohayterminospago':nohayterminospago, 'nohayconsecutivo':nohayconsecutivo,
		'items_cotiz':items_cotiz, 'clientes_cotiz':clientes_cotiz, 'terminospago_cotiz':terminospago_cotiz, 'nohayitems':nohayitems, 'nohayclientes':nohayclientes})


def editar_cotizacion(request, pk):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	terminospago_cotiz = Termino_de_pago.objects.filter(org_creadora=orgactivas).order_by('plazo_dias')
	clientes_cotiz = Contacto.objects.filter(relacion_activa="CL", org_creadora=orgactivas).order_by('nombre_legal')
	items_cotiz = Item.objects.filter(org_creadora=orgactivas).order_by('codigo')
	nohayclientes = Contacto.objects.filter(relacion_activa="CL", org_creadora=orgactivas).count()
	nohayitems = Item.objects.filter(org_creadora=orgactivas).count()
	nohayconsecutivo = Consecutivo_documento.objects.filter(tipo_de_documento='CZN', org_creadora=orgactivas).count()
	nohayterminospago = Termino_de_pago.objects.filter(org_creadora=orgactivas).count()
	nohaycotizaciones = Cotizacion.objects.filter(org_creadora=orgactivas, generado=True).count()
	cotizacion = get_object_or_404(Cotizacion, pk=pk)
	consecutivo_cotizacion = cotizacion.consecutivo_interno
	consecutivo_prefijo = cotizacion.consec_inter_prefijo
	consecutivo_numero = cotizacion.consec_inter_numero
	fecha_creacion = cotizacion.fecha_emision
	vendedor = cotizacion.vendedor
	if request.method == "POST":
		form = CotizacionForm(request.POST, instance=cotizacion)
		dic = request.POST
		termin = dic["terminospago_cotiz"]
		client = dic["clientes_cotiz"]
		item_1 = dic["items_1"]
		item_2 = dic["items_2"]
		item_3 = dic["items_3"]
		item_4 = dic["items_4"]
		item_5 = dic["items_5"]
		if form.is_valid():
			cotizacion = form.save(commit=False)
			cotizacion.fecha_emision = fecha_creacion
			cotizacion.consecutivo_interno = consecutivo_cotizacion
			cotizacion.consec_inter_prefijo = consecutivo_prefijo
			cotizacion.consec_inter_numero = consecutivo_numero
			cotizacion.vendedor = vendedor
			cotizacion.org_creadora = orgactivas
			cotizacion.generado = True
			cotizacion.terminos_de_pago = termin
			cotizacion.cliente = client
			if item_1 != '0':
				cotizacion.item_1 = item_1
			if item_2 != '0':
				cotizacion.item_2 = item_2
			if item_3 != '0':
				cotizacion.item_3 = item_3
			if item_4 != '0':
				cotizacion.item_4 = item_4
			if item_5 != '0':
				cotizacion.item_5 = item_5
			cotizacion.info_item()
			cotizacion.auto_info_organizacion()
			cotizacion.auto_info_cliente()
			cotizacion.calculo_item()
			cotizacion.calculo_total_cotizacion()
			cotizacion.tipo_impuestodoc()
			cotizacion.save()
			return redirect('detalle_cotizacion', pk=cotizacion.pk)
	else:
		form = CotizacionForm(instance=cotizacion)
	cotizaciones = Cotizacion.objects.filter(org_creadora=orgactivas, generado=True).order_by('-consecutivo_interno')
	cotizaciones = reemplazardatos_cotizaciones(cotizaciones)
	return render(request, 'groway/editar_cotizacion.html', {'form':form, 'orgactivas':orgactivas, 'cotizaciones':cotizaciones, 'cotizacion':cotizacion, 'nohaycotizaciones':nohaycotizaciones, 'nohayterminospago':nohayterminospago, 'nohayconsecutivo':nohayconsecutivo,
		'items_cotiz':items_cotiz, 'clientes_cotiz':clientes_cotiz, 'terminospago_cotiz':terminospago_cotiz, 'nohayitems':nohayitems, 'nohayclientes':nohayclientes})

def detalle_cotizacion(request, pk):
	lista ="valor"
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayclientes = Contacto.objects.filter(relacion_activa="CL", org_creadora=orgactivas).count()
	nohayitems = Item.objects.filter(org_creadora=orgactivas).count()
	nohayconsecutivo_rsm = Consecutivo_documento.objects.filter(tipo_de_documento='RSN', org_creadora=orgactivas).count()
	nohayconsecutivo_fve = Consecutivo_documento.objects.filter(tipo_de_documento='FVE', org_creadora=orgactivas, generado=True).count()
	nohayconsecutivo = Consecutivo_documento.objects.filter(tipo_de_documento='CZN', org_creadora=orgactivas).count()
	nohayterminospago = Termino_de_pago.objects.filter(org_creadora=orgactivas).count()
	nohaycotizaciones = Cotizacion.objects.filter(org_creadora=orgactivas, generado=True).count()
	cotizacion = get_object_or_404(Cotizacion, pk=pk)
	cotizacion = reemplazardatos_cotizacion(cotizacion)
	remisionesgeneradas = Remision.objects.filter(referencia_cotizacion=cotizacion.consecutivo_interno, org_creadora=orgactivas).count()
	if remisionesgeneradas:
		remisionesgeneradas = Remision.objects.get(referencia_cotizacion=cotizacion.consecutivo_interno, org_creadora=orgactivas)
	else:
		remisionesgeneradas = 0
	facturasgeneradas = Factura_de_venta.objects.filter(referencia_cotizacion=cotizacion.consecutivo_interno, org_creadora=orgactivas).count()
	if facturasgeneradas:
		facturasgeneradas = Factura_de_venta.objects.get(referencia_cotizacion=cotizacion.consecutivo_interno, org_creadora=orgactivas)
	else:
		facturasgeneradas = 0
	if request.method == "POST":
		dic = request.POST
		busqueda = dic["buscar"]
		orden = dic["ordenar"]
		buscarxfecha = Cotizacion.objects.filter(fecha_emision__contains=busqueda, org_creadora=orgactivas, generado=True)
		buscarxconsec = Cotizacion.objects.filter(consecutivo_interno__contains=busqueda, org_creadora=orgactivas, generado=True)
		buscarxcliente = Cotizacion.objects.filter(nombre_cliente__contains=busqueda, org_creadora=orgactivas, generado=True)
		buscarxtotal = Cotizacion.objects.filter(total_documento__contains=busqueda, org_creadora=orgactivas, generado=True)
		if buscarxfecha:
			lista = buscarxfecha.order_by(orden)
			lista = reemplazardatos_cotizaciones(lista)
		elif buscarxconsec:
			lista = buscarxconsec.order_by(orden)
			lista = reemplazardatos_cotizaciones(lista)
		elif buscarxcliente:
			lista = buscarxcliente.order_by(orden)
			lista = reemplazardatos_cotizaciones(lista)
		elif buscarxtotal:
			lista = buscarxtotal.order_by(orden)
			lista = reemplazardatos_cotizaciones(lista)
		else:
			lista = Cotizacion.objects.filter(org_creadora=orgactivas, generado=True).order_by('-consecutivo_interno')
			lista = reemplazardatos_cotizaciones(lista)
	cotizaciones = Cotizacion.objects.filter(org_creadora=orgactivas, generado=True).order_by('-consecutivo_interno')
	cotizaciones = reemplazardatos_cotizaciones(cotizaciones)
	return render(request, 'groway/detalle_cotizacion.html', {'orgactivas':orgactivas, 'cotizacion':cotizacion, 'cotizaciones':cotizaciones, 'lista':lista, 'nohaycotizaciones':nohaycotizaciones, 'nohayterminospago':nohayterminospago, 'nohayconsecutivo':nohayconsecutivo,
	 'nohayconsecutivo_rsm':nohayconsecutivo_rsm, 'nohayconsecutivo_fve':nohayconsecutivo_fve, 'remisionesgeneradas':remisionesgeneradas, 'facturasgeneradas':facturasgeneradas, 'nohayitems':nohayitems, 'nohayclientes':nohayclientes})

def pdf_cotizacion(request, pk):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	consecutivo_fac = Consecutivo_documento.objects.filter(tipo_de_documento='FVE', org_creadora=orgactivas)
	if consecutivo_fac:
		consecutivo_fac = consecutivo_fac.get(tipo_de_documento='FVE', org_creadora=orgactivas)
	else:
		consecutivo_fac = None
	cotizacion = get_object_or_404(Cotizacion, pk=pk)
	cotizacion = reemplazardatos_cotizacion(cotizacion)
	template = get_template('groway/pdf_cotizacion.html')
	consec = cotizacion.consecutivo_interno
	context = {'cotizacion':cotizacion, 'consecutivo_fac':consecutivo_fac, 'orgactivas':orgactivas}
	html = template.render(context)
	result = BytesIO()
	pdf = pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=result, link_callback=fetch_resources)
	if pdf:
		response = HttpResponse(result.getvalue(), content_type='application/pdf')
		filename = "Cotización %s.pdf"%(consec)
		content = "inline; filename = %s"%(filename)
		response['Content-Disposition'] = content
		return response
	return HttpResponse("Not found")


def generar_remision_cotiz(request, pk):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	cotizacion = get_object_or_404(Cotizacion, pk=pk)
	nueva_remision = cotizacion.generar_remision()
	nueva_remision.fecha_emision = timezone.now()
	nueva_remision.auto_info_organizacion()
	nueva_remision.auto_info_cliente()
	nueva_remision.auto_consecutivo()
	nueva_remision.generado = True
	nueva_remision.save()
	cotizacion.referencia_remision = nueva_remision.consecutivo_interno
	cotizacion.save()
	facturasgeneradas = Factura_de_venta.objects.filter(referencia_cotizacion=cotizacion.consecutivo_interno, org_creadora=orgactivas).count()
	if facturasgeneradas:
		facturasgeneradas = Factura_de_venta.objects.get(referencia_cotizacion=cotizacion.consecutivo_interno, org_creadora=orgactivas)
		facturasgeneradas.referencia_remision = nueva_remision.consecutivo_interno
		facturasgeneradas.save()
	return redirect('detalle_remision', pk=nueva_remision.pk)

def generar_factura_cotiz(request, pk):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	cotizacion = get_object_or_404(Cotizacion, pk=pk)
	nueva_factura = cotizacion.generar_factura_venta()
	nueva_factura.fecha_para_consec = date.today()
	nueva_factura.fecha_emision = timezone.now()
	nueva_factura.save()
	nueva_factura.auto_vencimiento()
	nueva_factura.auto_info_organizacion()
	nueva_factura.auto_info_cliente()
	nueva_factura.info_item()
	nueva_factura.calculo_item()
	nueva_factura.calculo_total_factura()
	nueva_factura.auto_consecutivo()
	nueva_factura.tipo_impuestodoc()
	if nueva_factura.consecutivo_interno == 'vencido':
		nueva_factura.generado = False
		nueva_factura.save()
		return redirect('consecutivos')
	else:
		nueva_factura.generado = True
	nueva_factura.save()
	cotizacion.referencia_factura = nueva_factura.consecutivo_interno
	cotizacion.save()
	remisionesgeneradas = Remision.objects.filter(referencia_cotizacion=cotizacion.consecutivo_interno, org_creadora=orgactivas).count()
	if remisionesgeneradas:
		remisionesgeneradas = Remision.objects.get(referencia_cotizacion=cotizacion.consecutivo_interno, org_creadora=orgactivas)
		remisionesgeneradas.referencia_factura = nueva_factura.consecutivo_interno
		remisionesgeneradas.save()
	return redirect('detalle_factura_venta', pk=nueva_factura.pk)


@login_required
def remisiones(request):
	lista ="valor"
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayconsecutivo = Consecutivo_documento.objects.filter(tipo_de_documento='RSN', org_creadora=orgactivas).count()
	nohayremisiones = Remision.objects.filter(org_creadora=orgactivas).count()
	if request.method == "POST":
			dic = request.POST
			busqueda = dic["buscar"]
			orden = dic["ordenar"]
			buscarxfecha = Remision.objects.filter(fecha_emision__contains=busqueda, org_creadora=orgactivas)
			buscarxconsec = Remision.objects.filter(consecutivo_interno__contains=busqueda, org_creadora=orgactivas)
			buscarxcliente = Remision.objects.filter(nombre_cliente__contains=busqueda, org_creadora=orgactivas)
			if buscarxfecha:
				lista = buscarxfecha.order_by(orden)
				lista = reemplazardatos_remisiones(lista)
			elif buscarxconsec:
				lista = buscarxconsec.order_by(orden)
				lista = reemplazardatos_remisiones(lista)
			elif buscarxcliente:
				lista = buscarxcliente.order_by(orden)
				lista = reemplazardatos_remisiones(lista)
			else:
				lista = Remision.objects.filter(org_creadora=orgactivas).order_by('-consecutivo_interno')
				lista = reemplazardatos_remisiones(lista)
	remisiones = Remision.objects.filter(org_creadora=orgactivas).order_by('-consecutivo_interno')
	remisiones = reemplazardatos_remisiones(remisiones)
	return render(request, 'groway/remisiones.html', {'orgactivas':orgactivas, 'remisiones':remisiones, 'lista':lista, 'nohayremisiones':nohayremisiones, 'nohayconsecutivo':nohayconsecutivo})

def detalle_remision(request, pk):
	lista ="valor"
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayconsecutivo = Consecutivo_documento.objects.filter(tipo_de_documento='RSN', org_creadora=orgactivas).count()
	nohayremisiones = Remision.objects.filter(org_creadora=orgactivas).count()
	remision = get_object_or_404(Remision, pk=pk)
	remision = reemplazardatos_remision(remision)
	cotizacion_generadora = Cotizacion.objects.filter(referencia_remision=remision.consecutivo_interno, org_creadora=orgactivas)
	if cotizacion_generadora:
		cotizacion_generadora = cotizacion_generadora.get(referencia_remision=remision.consecutivo_interno, org_creadora=orgactivas)
	else:
		cotizacion_generadora = None
	factura_relacionada = Factura_de_venta.objects.filter(referencia_remision=remision.consecutivo_interno, org_creadora=orgactivas)
	if factura_relacionada:
		factura_relacionada = factura_relacionada.get(referencia_remision=remision.consecutivo_interno, org_creadora=orgactivas)
	else:
		factura_relacionada = None
	if request.method == "POST":
			dic = request.POST
			busqueda = dic["buscar"]
			orden = dic["ordenar"]
			buscarxfecha = Remision.objects.filter(fecha_emision__contains=busqueda, org_creadora=orgactivas)
			buscarxconsec = Remision.objects.filter(consecutivo_interno__contains=busqueda, org_creadora=orgactivas)
			buscarxcliente = Remision.objects.filter(nombre_cliente__contains=busqueda, org_creadora=orgactivas)
			if buscarxfecha:
				lista = buscarxfecha.order_by(orden)
				lista = reemplazardatos_remisiones(lista)
			elif buscarxconsec:
				lista = buscarxconsec.order_by(orden)
				lista = reemplazardatos_remisiones(lista)
			elif buscarxcliente:
				lista = buscarxcliente.order_by(orden)
				lista = reemplazardatos_remisiones(lista)
			else:
				lista = Remision.objects.filter(org_creadora=orgactivas).order_by('-consecutivo_interno')
				lista = reemplazardatos_remisiones(lista)
	remisiones = Remision.objects.filter(org_creadora=orgactivas).order_by('-consecutivo_interno')
	remisiones = reemplazardatos_remisiones(remisiones)
	return render(request, 'groway/detalle_remision.html', {'orgactivas':orgactivas, 'remision':remision, 'remisiones':remisiones, 'lista':lista, 'nohayremisiones':nohayremisiones, 'nohayconsecutivo':nohayconsecutivo, 'cotizacion_generadora':cotizacion_generadora, 'factura_relacionada':factura_relacionada})

def agregar_datos_remision(request, pk):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayconsecutivo = Consecutivo_documento.objects.filter(tipo_de_documento='RSN', org_creadora=orgactivas).count()
	nohayremisiones = Remision.objects.filter(org_creadora=orgactivas).count()
	remision = get_object_or_404(Remision, pk=pk)
	remision = reemplazardatos_remision(remision)
	cliente_remision = remision.cliente
	fecha_creacion = remision.fecha_emision
	consecutivo_remision = remision.consecutivo_interno
	vendedor = remision.vendedor
	org_remision = remision.org_creadora
	if request.method == "POST":
		datos_remision = request.POST
		transport = datos_remision["transport_data"]
		orden_comp = datos_remision["orden_compra"]
		otro_doc = datos_remision["otro_documento"]
		if transport:
			remision.datos_transportador = transport
		if orden_comp:
			remision.referencia_orden_compra = orden_comp
		if otro_doc:
			remision.referencia_otro_documento = otro_doc
		remision.save()
		return redirect('detalle_remision', pk=remision.pk)
	remisiones = Remision.objects.filter(org_creadora=orgactivas).order_by('-consecutivo_interno')
	remisiones = reemplazardatos_remisiones(remisiones)
	return render(request, 'groway/editar_remision.html', {'orgactivas':orgactivas, 'remisiones':remisiones, 'remision':remision, 'nohayremisiones':nohayremisiones, 'nohayconsecutivo':nohayconsecutivo})

def pdf_remision(request, pk):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	consecutivo_fac = Consecutivo_documento.objects.filter(tipo_de_documento='FVE', org_creadora=orgactivas)
	if consecutivo_fac:
		consecutivo_fac = consecutivo_fac.get(tipo_de_documento='FVE', org_creadora=orgactivas)
	else:
		consecutivo_fac = None
	remision = get_object_or_404(Remision, pk=pk)
	remision = reemplazardatos_remision(remision)
	template = get_template('groway/pdf_remision.html')
	consec = remision.consecutivo_interno
	context = {'remision':remision, 'consecutivo_fac':consecutivo_fac, 'orgactivas':orgactivas}
	html = template.render(context)
	result = BytesIO()
	pdf = pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=result, link_callback=fetch_resources)
	if pdf:
		response = HttpResponse(result.getvalue(), content_type='application/pdf')
		filename = "Remisión %s.pdf"%(consec)
		content = "inline; filename = %s"%(filename)
		response['Content-Disposition'] = content
		return response
	return HttpResponse("Not found")


@login_required
def facturas_venta(request):
	lista ="valor"
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayclientes = Contacto.objects.filter(relacion_activa="CL", org_creadora=orgactivas).count()
	nohayitems = Item.objects.filter(org_creadora=orgactivas).count()
	nohayconsecutivo = Consecutivo_documento.objects.filter(tipo_de_documento='FVE', org_creadora=orgactivas, generado=True).count()
	nohayterminospago = Termino_de_pago.objects.filter(org_creadora=orgactivas).count()
	nohayfacturas = Factura_de_venta.objects.filter(org_creadora=orgactivas, generado=True).count()
	solo_fac_anuladas = Factura_de_venta.objects.filter(org_creadora=orgactivas, generado=True, anulada=False).count()
	if request.method == "POST":
		dic = request.POST
		busqueda = dic["buscar"]
		orden = dic["ordenar"]
		buscarxfecha = Factura_de_venta.objects.filter(fecha_emision__contains=busqueda, org_creadora=orgactivas, generado=True)
		buscarxconsec = Factura_de_venta.objects.filter(consecutivo_interno__contains=busqueda, org_creadora=orgactivas, generado=True)
		buscarxcliente = Factura_de_venta.objects.filter(nombre_cliente__contains=busqueda, org_creadora=orgactivas, generado=True)
		buscarxtotal = Factura_de_venta.objects.filter(total_documento__contains=busqueda, org_creadora=orgactivas, generado=True)
		if buscarxfecha:
			if orden == "anulada":
				lista = buscarxfecha.filter(anulada=True).order_by('-consecutivo_interno')
				lista = reemplazardatos_facturas(lista)
			else:
				lista = buscarxfecha.filter(anulada=False).order_by(orden)
				lista = reemplazardatos_facturas(lista)
		elif buscarxconsec:
			if orden == "anulada":
				lista = buscarxconsec.filter(anulada=True).order_by('-consecutivo_interno')
				lista = reemplazardatos_facturas(lista)
			else:
				lista = buscarxconsec.filter(anulada=False).order_by(orden)
				lista = reemplazardatos_facturas(lista)
		elif buscarxcliente:
			if orden == "anulada":
				lista = buscarxcliente.filter(anulada=True).order_by('-consecutivo_interno')
				lista = reemplazardatos_facturas(lista)
			else:
				lista = buscarxcliente.filter(anulada=False).order_by(orden)
				lista = reemplazardatos_facturas(lista)
		elif buscarxtotal:
			if orden == "anulada":
				lista = buscarxtotal.order_by(anulada=True).order_by('-consecutivo_interno')
				lista = reemplazardatos_facturas(lista)
			else:
				lista = buscarxtotal.filter(anulada=False).order_by(orden)
				lista = reemplazardatos_facturas(lista)
		else:
			lista = Factura_de_venta.objects.filter(org_creadora=orgactivas, generado=True, anulada=False).order_by('-consecutivo_interno')
			lista = reemplazardatos_facturas(lista)
	facturas = Factura_de_venta.objects.filter(org_creadora=orgactivas, generado=True, anulada=False).order_by('-consecutivo_interno')
	facturas = reemplazardatos_facturas(facturas)
	return render(request, 'groway/facturas_venta.html', {'orgactivas':orgactivas, 'facturas':facturas, 'lista':lista, 'nohayfacturas':nohayfacturas, 'nohayterminospago':nohayterminospago, 'nohayconsecutivo':nohayconsecutivo,
		'solo_fac_anuladas':solo_fac_anuladas, 'nohayitems':nohayitems, 'nohayclientes':nohayclientes})


def nueva_fac_ven_ing(request):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	terminospago_fac = Termino_de_pago.objects.filter(org_creadora=orgactivas).order_by('plazo_dias')
	clientes_fac = Contacto.objects.filter(relacion_activa="CL", org_creadora=orgactivas).order_by('nombre_legal')
	items_fac = Item.objects.filter(org_creadora=orgactivas).order_by('codigo')
	nohayclientes = Contacto.objects.filter(relacion_activa="CL", org_creadora=orgactivas).count()
	nohayitems = Item.objects.filter(org_creadora=orgactivas).count()
	nohayconsecutivo = Consecutivo_documento.objects.filter(tipo_de_documento='FVE', org_creadora=orgactivas, generado=True).count()
	nohayterminospago = Termino_de_pago.objects.filter(org_creadora=orgactivas).count()
	nohayfacturas = Factura_de_venta.objects.filter(org_creadora=orgactivas, generado=True).count()
	documentoborrador = Factura_de_venta.objects.filter(org_creadora=orgactivas, generado=False).last()
	if request.method == "POST":
		if documentoborrador:
			form = Factura_de_ventaForm(request.POST, instance=documentoborrador)
		else:
			form = Factura_de_ventaForm(request.POST)
		dic = request.POST
		termin = dic["terminospago_fac"]
		client = dic["clientes_fac"]
		item_1 = dic["items_1"]
		item_2 = dic["items_2"]
		item_3 = dic["items_3"]
		item_4 = dic["items_4"]
		item_5 = dic["items_5"]
		if form.is_valid():
			factura = form.save(commit=False)
			factura.org_creadora = orgactivas
			factura.vendedor = request.user
			factura.terminos_de_pago = termin
			factura.cliente = client
			if item_1 != '0':
				factura.item_1 = item_1
			if item_2 != '0':
				factura.item_2 = item_2
			if item_3 != '0':
				factura.item_3 = item_3
			if item_4 != '0':
				factura.item_4 = item_4
			if item_5 != '0':
				factura.item_5 = item_5
			factura.auto_info_organizacion()
			factura.auto_info_cliente()
			factura.info_item()
			factura.save()
			return redirect('nueva_fac_ven_cal', pk=factura.pk)
	else:
		form = Factura_de_ventaForm()
	facturas = Factura_de_venta.objects.filter(org_creadora=orgactivas, generado=True, anulada=False).order_by('-consecutivo_interno')
	facturas = reemplazardatos_facturas(facturas)
	return render(request, 'groway/nueva_factura_venta.html', {'form':form, 'orgactivas':orgactivas, 'facturas':facturas, 'nohayfacturas':nohayfacturas, 'nohayterminospago':nohayterminospago, 'nohayconsecutivo':nohayconsecutivo,
		'terminospago_fac':terminospago_fac, 'clientes_fac':clientes_fac, 'items_fac':items_fac, 'nohayitems':nohayitems, 'nohayclientes':nohayclientes})

def nueva_fac_ven_cal(request, pk):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	terminospago_fac = Termino_de_pago.objects.filter(org_creadora=orgactivas).order_by('plazo_dias')
	clientes_fac = Contacto.objects.filter(relacion_activa="CL", org_creadora=orgactivas).order_by('nombre_legal')
	items_fac = Item.objects.filter(org_creadora=orgactivas).order_by('codigo')
	nohayclientes = Contacto.objects.filter(relacion_activa="CL", org_creadora=orgactivas).count()
	nohayitems = Item.objects.filter(org_creadora=orgactivas).count()
	nohayconsecutivo = Consecutivo_documento.objects.filter(tipo_de_documento='FVE', org_creadora=orgactivas, generado=True).count()
	nohayterminospago = Termino_de_pago.objects.filter(org_creadora=orgactivas).count()
	nohayfacturas = Factura_de_venta.objects.filter(org_creadora=orgactivas, generado=True).count()
	factura = get_object_or_404(Factura_de_venta, pk=pk)
	if request.method == "POST":
		form = Factura_de_ventaForm(request.POST, instance=factura)
		dic = request.POST
		termin = dic["terminospago_fac"]
		client = dic["clientes_fac"]
		item_1 = dic["items_1"]
		item_2 = dic["items_2"]
		item_3 = dic["items_3"]
		item_4 = dic["items_4"]
		item_5 = dic["items_5"]
		if form.is_valid():
			factura = form.save(commit=False)
			if factura.cantidad_1:
				factura.org_creadora = orgactivas
				factura.fecha_para_consec = timezone.now()
				factura.fecha_emision = timezone.now()
				factura.vendedor = request.user
				factura.terminos_de_pago = termin
				factura.cliente = client
				if item_1 != '0':
					factura.item_1 = item_1
				if item_2 != '0':
					factura.item_2 = item_2
				if item_3 != '0':
					factura.item_3 = item_3
				if item_4 != '0':
					factura.item_4 = item_4
				if item_5 != '0':
					factura.item_5 = item_5
				factura.auto_vencimiento()
				factura.info_item()
				factura.auto_info_organizacion()
				factura.auto_info_cliente()
				factura.calculo_item()
				factura.calculo_total_factura()
				factura.save()
				return redirect('nueva_fac_ven_cal', pk=factura.pk)
			else:
				return redirect('nueva_fac_ven_cal', pk=factura.pk)
	else:
		form = Factura_de_ventaForm(instance=factura)
	facturas = Factura_de_venta.objects.filter(org_creadora=orgactivas, generado=True, anulada=False).order_by('-consecutivo_interno')
	facturas = reemplazardatos_facturas(facturas)
	return render(request, 'groway/nueva_factura_venta.html', {'form':form, 'orgactivas':orgactivas, 'facturas':facturas, 'factura':factura, 'nohayfacturas':nohayfacturas, 'nohayterminospago':nohayterminospago, 'nohayconsecutivo':nohayconsecutivo,
		'terminospago_fac':terminospago_fac, 'clientes_fac':clientes_fac, 'items_fac':items_fac, 'nohayitems':nohayitems, 'nohayclientes':nohayclientes})

def nueva_fac_ven_fin(request, pk):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	factura = get_object_or_404(Factura_de_venta, pk=pk)
	factura.org_creadora = orgactivas
	factura.fecha_para_consec = date.today()
	factura.fecha_emision = timezone.now()
	factura.save()
	factura.auto_vencimiento()
	factura.tipo_impuestodoc()
	factura.auto_consecutivo()
	if factura.consecutivo_interno == 'vencido':
		factura.generado = False
		factura.save()
		return redirect('consecutivos')
	else:
		factura.generado = True
	factura.save()
	return redirect('detalle_factura_venta', pk=pk)


def atras_fac_ven(request, pk):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	terminospago_fac = Termino_de_pago.objects.filter(org_creadora=orgactivas).order_by('plazo_dias')
	clientes_fac = Contacto.objects.filter(relacion_activa="CL", org_creadora=orgactivas).order_by('nombre_legal')
	items_fac = Item.objects.filter(org_creadora=orgactivas).order_by('codigo')
	nohayclientes = Contacto.objects.filter(relacion_activa="CL", org_creadora=orgactivas).count()
	nohayitems = Item.objects.filter(org_creadora=orgactivas).count()
	nohayconsecutivo = Consecutivo_documento.objects.filter(tipo_de_documento='FVE', org_creadora=orgactivas, generado=True).count()
	nohayterminospago = Termino_de_pago.objects.filter(org_creadora=orgactivas).count()
	nohayfacturas = Factura_de_venta.objects.filter(org_creadora=orgactivas, generado=True).count()
	factura = get_object_or_404(Factura_de_venta, pk=pk)
	if request.method == "POST":
		form = Factura_de_ventaForm(request.POST, instance=factura)
		dic = request.POST
		termin = dic["terminospago_fac"]
		client = dic["clientes_fac"]
		item_1 = dic["items_1"]
		item_2 = dic["items_2"]
		item_3 = dic["items_3"]
		item_4 = dic["items_4"]
		item_5 = dic["items_5"]
		if form.is_valid():
			factura = form.save(commit=False)
			factura.vendedor = request.user
			factura.org_creadora = orgactivas
			factura.terminos_de_pago = termin
			factura.cliente = client
			if item_1 != '0':
				factura.item_1 = item_1
			if item_2 != '0':
				factura.item_2 = item_2
			if item_3 != '0':
				factura.item_3 = item_3
			if item_4 != '0':
				factura.item_4 = item_4
			if item_5 != '0':
				factura.item_5 = item_5
			factura.auto_info_organizacion()
			factura.auto_info_cliente()
			factura.info_item()
			factura.save()
			return redirect('nueva_fac_ven_cal', pk=factura.pk)
	else:
		form = Factura_de_ventaForm(instance=factura)
	facturas = Factura_de_venta.objects.filter(org_creadora=orgactivas, generado=True, anulada=False).order_by('-consecutivo_interno')
	facturas = reemplazardatos_facturas(facturas)
	return render(request, 'groway/nueva_factura_venta.html', {'form':form, 'orgactivas':orgactivas, 'facturas':facturas, 'nohayfacturas':nohayfacturas, 'nohayterminospago':nohayterminospago, 'nohayconsecutivo':nohayconsecutivo,
		'terminospago_fac':terminospago_fac, 'clientes_fac':clientes_fac, 'items_fac':items_fac, 'nohayitems':nohayitems, 'nohayclientes':nohayclientes})

def detalle_factura_venta(request, pk):
	lista ="valor"
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayclientes = Contacto.objects.filter(relacion_activa="CL", org_creadora=orgactivas).count()
	nohayitems = Item.objects.filter(org_creadora=orgactivas).count()
	nohayconsecutivo_rsm = Consecutivo_documento.objects.filter(tipo_de_documento='RSN', org_creadora=orgactivas).count()
	nohayconsecutivo_ncred = Consecutivo_documento.objects.filter(tipo_de_documento='NCT', org_creadora=orgactivas).count()
	nohayconsecutivo_ndeb = Consecutivo_documento.objects.filter(tipo_de_documento='NDT', org_creadora=orgactivas).count()
	nohayconsecutivo = Consecutivo_documento.objects.filter(tipo_de_documento='FVE', org_creadora=orgactivas, generado=True).count()
	nohayterminospago = Termino_de_pago.objects.filter(org_creadora=orgactivas).count()
	nohayfacturas = Factura_de_venta.objects.filter(org_creadora=orgactivas, generado=True).count()
	solo_fac_anuladas = Factura_de_venta.objects.filter(org_creadora=orgactivas, generado=True, anulada=False).count()
	factura = get_object_or_404(Factura_de_venta, pk=pk)
	factura = reemplazardatos_factura(factura)
	cotizacion_generadora = Cotizacion.objects.filter(referencia_factura=factura.consecutivo_interno, org_creadora=orgactivas)
	if cotizacion_generadora:
		cotizacion_generadora = cotizacion_generadora.get(referencia_factura=factura.consecutivo_interno, org_creadora=orgactivas)
	else:
		cotizacion_generadora = None
	remisionesgeneradas = Remision.objects.filter(referencia_factura=factura.consecutivo_interno, org_creadora=orgactivas).count()
	if remisionesgeneradas:
		remisionesgeneradas = Remision.objects.get(referencia_factura=factura.consecutivo_interno, org_creadora=orgactivas)
	else:
		remisionesgeneradas = 0
	notascreditogeneradas = Nota_credito.objects.filter(referencia_factura=factura.consecutivo_interno, org_creadora=orgactivas).count()
	if notascreditogeneradas:
		notascreditogeneradas = Nota_credito.objects.get(referencia_factura=factura.consecutivo_interno, org_creadora=orgactivas)
	else:
		notascreditogeneradas = 0
	notasdebitogeneradas = Nota_debito.objects.filter(referencia_factura=factura.consecutivo_interno, org_creadora=orgactivas).count()
	if notasdebitogeneradas:
		notasdebitogeneradas = Nota_debito.objects.get(referencia_factura=factura.consecutivo_interno, org_creadora=orgactivas)
	else:
		notasdebitogeneradas = 0
	if request.method == "POST":
		dic = request.POST
		busqueda = dic["buscar"]
		orden = dic["ordenar"]
		buscarxfecha = Factura_de_venta.objects.filter(fecha_emision__contains=busqueda, org_creadora=orgactivas, generado=True)
		buscarxconsec = Factura_de_venta.objects.filter(consecutivo_interno__contains=busqueda, org_creadora=orgactivas, generado=True)
		buscarxcliente = Factura_de_venta.objects.filter(nombre_cliente__contains=busqueda, org_creadora=orgactivas, generado=True)
		buscarxtotal = Factura_de_venta.objects.filter(total_documento__contains=busqueda, org_creadora=orgactivas, generado=True)
		if buscarxfecha:
			if orden == "anulada":
				lista = buscarxfecha.filter(anulada=True).order_by('-consecutivo_interno')
				lista = reemplazardatos_facturas(lista)
			else:
				lista = buscarxfecha.filter(anulada=False).order_by(orden)
				lista = reemplazardatos_facturas(lista)
		elif buscarxconsec:
			if orden == "anulada":
				lista = buscarxconsec.filter(anulada=True).order_by('-consecutivo_interno')
				lista = reemplazardatos_facturas(lista)
			else:
				lista = buscarxconsec.filter(anulada=False).order_by(orden)
				lista = reemplazardatos_facturas(lista)
		elif buscarxcliente:
			if orden == "anulada":
				lista = buscarxcliente.filter(anulada=True).order_by('-consecutivo_interno')
				lista = reemplazardatos_facturas(lista)
			else:
				lista = buscarxcliente.filter(anulada=False).order_by(orden)
				lista = reemplazardatos_facturas(lista)
		elif buscarxtotal:
			if orden == "anulada":
				lista = buscarxtotal.order_by(anulada=True).order_by('-consecutivo_interno')
				lista = reemplazardatos_facturas(lista)
			else:
				lista = buscarxtotal.filter(anulada=False).order_by(orden)
				lista = reemplazardatos_facturas(lista)
		else:
			lista = Factura_de_venta.objects.filter(org_creadora=orgactivas, generado=True, anulada=False).order_by('-consecutivo_interno')
			lista = reemplazardatos_facturas(lista)
	facturas = Factura_de_venta.objects.filter(org_creadora=orgactivas, generado=True, anulada=False).order_by('-consecutivo_interno')
	facturas = reemplazardatos_facturas(facturas)
	return render(request, 'groway/detalle_factura_venta.html', {'orgactivas':orgactivas, 'factura':factura, 'facturas':facturas, 'lista':lista, 'nohayfacturas':nohayfacturas, 'nohayterminospago':nohayterminospago, 'nohayconsecutivo':nohayconsecutivo,
		'nohayconsecutivo_rsm':nohayconsecutivo_rsm, 'nohayconsecutivo_ncred':nohayconsecutivo_ncred, 'nohayconsecutivo_ndeb':nohayconsecutivo_ndeb,
		'remisionesgeneradas':remisionesgeneradas, 'notascreditogeneradas':notascreditogeneradas, 'notasdebitogeneradas':notasdebitogeneradas, 'cotizacion_generadora':cotizacion_generadora, 'solo_fac_anuladas':solo_fac_anuladas, 'nohayitems':nohayitems, 'nohayclientes':nohayclientes})

def pdf_factura_venta(request, pk):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	consecutivo_fac = Consecutivo_documento.objects.filter(tipo_de_documento='FVE', org_creadora=orgactivas)
	if consecutivo_fac:
		consecutivo_fac = consecutivo_fac.get(tipo_de_documento='FVE', org_creadora=orgactivas)
	else:
		consecutivo_fac = None
	factura = get_object_or_404(Factura_de_venta, pk=pk)
	factura = reemplazardatos_factura(factura)
	template = get_template('groway/pdf_factura_venta.html')
	consec = factura.consecutivo_interno
	context = {'factura':factura, 'consecutivo_fac':consecutivo_fac, 'orgactivas':orgactivas}
	html = template.render(context)
	result = BytesIO()
	pdf = pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=result, link_callback=fetch_resources)
	if pdf:
		response = HttpResponse(result.getvalue(), content_type='application/pdf')
		filename = "Factura de venta %s.pdf"%(consec)
		content = "inline; filename = %s"%(filename)
		response['Content-Disposition'] = content
		return response
	return HttpResponse("Not found")

def generar_remision_fac_ven(request, pk):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	factura = get_object_or_404(Factura_de_venta, pk=pk)
	nueva_remision = factura.generar_remision()
	nueva_remision.fecha_emision = timezone.now()
	nueva_remision.save()
	nueva_remision.auto_info_organizacion()
	nueva_remision.auto_info_cliente()
	nueva_remision.auto_consecutivo()
	nueva_remision.generado = True
	nueva_remision.save()
	factura.referencia_remision = nueva_remision.consecutivo_interno
	factura.save()
	cotizacion_generadora = Cotizacion.objects.filter(referencia_factura=factura.consecutivo_interno, org_creadora=orgactivas)
	if cotizacion_generadora:
		cotizacion_generadora = cotizacion_generadora.get(referencia_factura=factura.consecutivo_interno, org_creadora=orgactivas)
		cotizacion_generadora.referencia_remision = nueva_remision.consecutivo_interno
		cotizacion_generadora.save()
	notascreditogeneradas = Nota_credito.objects.filter(referencia_factura=factura.consecutivo_interno, org_creadora=orgactivas)
	if notascreditogeneradas:
		notascreditogeneradas = Nota_credito.objects.get(referencia_factura=factura.consecutivo_interno, org_creadora=orgactivas)
		notascreditogeneradas.referencia_remision = nueva_remision.consecutivo_interno
		notascreditogeneradas.save()
	notasdebitogeneradas = Nota_debito.objects.filter(referencia_factura=factura.consecutivo_interno, org_creadora=orgactivas)
	if notasdebitogeneradas:
		notasdebitogeneradas = Nota_debito.objects.get(referencia_factura=factura.consecutivo_interno, org_creadora=orgactivas)
		notasdebitogeneradas.referencia_remision = nueva_remision.consecutivo_interno
		notasdebitogeneradas.save()
	return redirect('detalle_remision', pk=nueva_remision.pk)

def generar_nota_credito(request, pk):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayclientes = Contacto.objects.filter(relacion_activa="CL", org_creadora=orgactivas).count()
	nohayitems = Item.objects.filter(org_creadora=orgactivas).count()
	nohayconsecutivo = Consecutivo_documento.objects.filter(tipo_de_documento='FVE', org_creadora=orgactivas).count()
	nohayterminospago = Termino_de_pago.objects.filter(org_creadora=orgactivas).count()
	nohayfacturas = Factura_de_venta.objects.filter(org_creadora=orgactivas, generado=True).count()
	factura = get_object_or_404(Factura_de_venta, pk=pk)
	nueva_creditnote = factura.generar_nota_credito()
	if request.method == "POST":
		concepto_creditnote = request.POST
		concepto = concepto_creditnote["note-concept"]
		descuento_creditnote = concepto_creditnote["descuento_rebaja"]
		if concepto == "1":
			nueva_creditnote.concepto_nota_credito = concepto
			item_1_afec = concepto_creditnote["item_1"]
			if item_1_afec == '1':
				nueva_creditnote.item_1_afec = nueva_creditnote.item_1
				nueva_creditnote.cantidad_1 = nueva_creditnote.cantidad_1 * (0)
			if factura.item_2:
				item_2_afec = concepto_creditnote["item_2"]
				if item_2_afec == '1':
					nueva_creditnote.item_2_afec = nueva_creditnote.item_2
					nueva_creditnote.cantidad_2 = nueva_creditnote.cantidad_2 * (0)
			if factura.item_3:
				item_3_afec = concepto_creditnote["item_3"]
				if item_3_afec == '1':
					nueva_creditnote.item_3_afec = nueva_creditnote.item_3
					nueva_creditnote.cantidad_3 = nueva_creditnote.cantidad_3 * (0)
			if factura.item_4:
				item_4_afec = concepto_creditnote["item_4"]
				if item_4_afec == '1':
					nueva_creditnote.item_4_afec = nueva_creditnote.item_4
					nueva_creditnote.cantidad_4 = nueva_creditnote.cantidad_4 * (0)
			if factura.item_5:
				item_5_afec = concepto_creditnote["item_5"]
				if item_5_afec == '1':
					nueva_creditnote.item_5_afec = nueva_creditnote.item_5
					nueva_creditnote.cantidad_5 = nueva_creditnote.cantidad_5 * (0)
			nueva_creditnote.fecha_emision = timezone.now()
			nueva_creditnote.save()
			nueva_creditnote.calculo_item()
			nueva_creditnote.calculo_total_creditnote()
			nueva_creditnote.auto_consecutivo()
			nueva_creditnote.generado = True
			nueva_creditnote.save()
			factura.referencia_notacredito = nueva_creditnote.consecutivo_interno
			factura.anulada = True
			factura.save()
			return redirect('detalle_nota_credito', pk=nueva_creditnote.pk)

		elif concepto == "3" or concepto == "4":
			nueva_creditnote.concepto_nota_credito = concepto
			nueva_creditnote.descuento_rebaja = int(descuento_creditnote)
			nueva_creditnote.saldo_total = nueva_creditnote.saldo_pendiente - nueva_creditnote.descuento_rebaja
			nueva_creditnote.fecha_emision = timezone.now()
			nueva_creditnote.save()
			nueva_creditnote.auto_consecutivo()
			nueva_creditnote.generado = True
			nueva_creditnote.save()
			factura.referencia_notacredito = nueva_creditnote.consecutivo_interno
			factura.anulada = True
			factura.save()
			return redirect('detalle_nota_credito', pk=nueva_creditnote.pk)
		
		elif concepto == "2" or concepto == "5" or concepto == "6":
			nueva_creditnote.concepto_nota_credito = concepto
			nueva_creditnote.cantidad_1 = nueva_creditnote.cantidad_1 * (-1)
			nueva_creditnote.cantidad_2 = nueva_creditnote.cantidad_2 * (-1)
			nueva_creditnote.cantidad_3 = nueva_creditnote.cantidad_3 * (-1)
			nueva_creditnote.cantidad_4 = nueva_creditnote.cantidad_4 * (-1)
			nueva_creditnote.cantidad_5 = nueva_creditnote.cantidad_5 * (-1)
			nueva_creditnote.anticipo = nueva_creditnote.anticipo * (-1)
			nueva_creditnote.fecha_emision = timezone.now()
			nueva_creditnote.save()
			nueva_creditnote.calculo_item()
			nueva_creditnote.calculo_total_creditnote()
			nueva_creditnote.auto_consecutivo()
			nueva_creditnote.generado = True
			nueva_creditnote.save()
			factura.referencia_notacredito = nueva_creditnote.consecutivo_interno
			factura.anulada = True
			factura.save()
			return redirect('detalle_nota_credito', pk=nueva_creditnote.pk)

		else:
			return redirect('generar_nota_credito', pk=pk)
	facturas = Factura_de_venta.objects.filter(org_creadora=orgactivas, generado=True, anulada=False).order_by('-consecutivo_interno')
	facturas = reemplazardatos_facturas(facturas)
	return render(request, 'groway/nueva_nota_credito.html', {'orgactivas':orgactivas, 'factura':factura, 'facturas':facturas, 'nohayfacturas':nohayfacturas, 'nohayterminospago':nohayterminospago, 'nohayconsecutivo':nohayconsecutivo,
		 'nohayitems':nohayitems, 'nohayclientes':nohayclientes})

def generar_nota_debito(request, pk):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayclientes = Contacto.objects.filter(relacion_activa="CL", org_creadora=orgactivas).count()
	nohayitems = Item.objects.filter(org_creadora=orgactivas).count()
	nohayconsecutivo = Consecutivo_documento.objects.filter(tipo_de_documento='FVE', org_creadora=orgactivas).count()
	nohayterminospago = Termino_de_pago.objects.filter(org_creadora=orgactivas).count()
	nohayfacturas = Factura_de_venta.objects.filter(org_creadora=orgactivas, generado=True).count()
	factura = get_object_or_404(Factura_de_venta, pk=pk)
	nueva_debitnote = factura.generar_nota_debito()
	if request.method == "POST":
		concepto_debitnote = request.POST
		concepto = concepto_debitnote["note-concept"]
		cargos_debitnote = concepto_debitnote["intereses_gastos"]
		descripcion_cargos = concepto_debitnote["descripcion_cargo_interes"]
		if concepto:
			nueva_debitnote.concepto_nota_debito = concepto
			nueva_debitnote.cargo_interes = int(cargos_debitnote)
			nueva_debitnote.descripcion_cargo = descripcion_cargos
			nueva_debitnote.saldo_total = nueva_debitnote.saldo_pendiente + nueva_debitnote.cargo_interes
			nueva_debitnote.fecha_emision = timezone.now()
			nueva_debitnote.save()
			nueva_debitnote.auto_consecutivo()
			nueva_debitnote.generado = True
			nueva_debitnote.save()
			factura.referencia_notadebito = nueva_debitnote.consecutivo_interno
			factura.anulada = True
			factura.save()
			return redirect('detalle_nota_debito', pk=nueva_debitnote.pk)
		else:
			return redirect('generar_nota_debito', pk=pk)
	facturas = Factura_de_venta.objects.filter(org_creadora=orgactivas, generado=True, anulada=False).order_by('-consecutivo_interno')
	facturas = reemplazardatos_facturas(facturas)
	return render(request, 'groway/nueva_nota_debito.html', {'orgactivas':orgactivas, 'factura':factura, 'facturas':facturas, 'nohayfacturas':nohayfacturas, 'nohayterminospago':nohayterminospago, 'nohayconsecutivo':nohayconsecutivo,
		'nohayitems':nohayitems, 'nohayclientes':nohayclientes})



@login_required
def notas_credito(request):
	lista ="valor"
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayconsecutivo = Consecutivo_documento.objects.filter(tipo_de_documento='NCT', org_creadora=orgactivas).count()
	nohaynotas = Nota_credito.objects.filter(org_creadora=orgactivas, generado=True).count()
	if request.method == "POST":
			dic = request.POST
			busqueda = dic["buscar"]
			orden = dic["ordenar"]
			buscarxfecha = Nota_credito.objects.filter(fecha_emision__contains=busqueda, org_creadora=orgactivas, generado=True)
			buscarxconsec = Nota_credito.objects.filter(consecutivo_interno__contains=busqueda, org_creadora=orgactivas, generado=True)
			buscarxcliente = Nota_credito.objects.filter(nombre_cliente__contains=busqueda, org_creadora=orgactivas, generado=True)
			buscarxtotal = Nota_credito.objects.filter(total_documento__contains=busqueda, org_creadora=orgactivas, generado=True)
			if buscarxfecha:
				lista = buscarxfecha.order_by(orden)
				lista = reemplazardatos_credits_notes(lista)
			elif buscarxconsec:
				lista = buscarxconsec.order_by(orden)
				lista = reemplazardatos_credits_notes(lista)
			elif buscarxcliente:
				lista = buscarxcliente.order_by(orden)
				lista = reemplazardatos_credits_notes(lista)
			elif buscarxtotal:
				lista = buscarxtotal.order_by(orden)
				lista = reemplazardatos_credits_notes(lista)
			else:
				lista = Nota_credito.objects.filter(org_creadora=orgactivas, generado=True).order_by('-consecutivo_interno')
				lista = reemplazardatos_credits_notes(lista)
	creditnotes = Nota_credito.objects.filter(org_creadora=orgactivas, generado=True).order_by('-consecutivo_interno')
	creditnotes = reemplazardatos_credits_notes(creditnotes)
	return render(request, 'groway/notas_credito.html', {'orgactivas':orgactivas, 'creditnotes':creditnotes, 'lista':lista, 'nohaynotas':nohaynotas, 'nohayconsecutivo':nohayconsecutivo})


def detalle_nota_credito(request, pk):
	lista ="valor"
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayconsecutivo = Consecutivo_documento.objects.filter(tipo_de_documento='NCT', org_creadora=orgactivas).count()
	nohaynotas = Nota_credito.objects.filter(org_creadora=orgactivas, generado=True).count()
	creditnote = get_object_or_404(Nota_credito, pk=pk)
	creditnote = reemplazardatos_credit_note(creditnote)
	factura_generadora = Factura_de_venta.objects.filter(referencia_notacredito=creditnote.consecutivo_interno, org_creadora=orgactivas)
	if factura_generadora:
		factura_generadora = factura_generadora.get(referencia_notacredito=creditnote.consecutivo_interno, org_creadora=orgactivas)
	else:
		factura_generadora = None
	cotizacion_generadora = Cotizacion.objects.filter(referencia_factura=creditnote.referencia_factura, org_creadora=orgactivas)
	if cotizacion_generadora:
		cotizacion_generadora = cotizacion_generadora.get(referencia_factura=creditnote.referencia_factura, org_creadora=orgactivas)
	else:
		cotizacion_generadora = None
	remisionesgeneradas = Remision.objects.filter(referencia_factura=creditnote.referencia_factura, org_creadora=orgactivas).count()
	if remisionesgeneradas:
		remisionesgeneradas = Remision.objects.get(referencia_factura=creditnote.referencia_factura, org_creadora=orgactivas)
	else:
		remisionesgeneradas = 0
	if request.method == "POST":
			dic = request.POST
			busqueda = dic["buscar"]
			orden = dic["ordenar"]
			buscarxfecha = Nota_credito.objects.filter(fecha_emision__contains=busqueda, org_creadora=orgactivas, generado=True)
			buscarxconsec = Nota_credito.objects.filter(consecutivo_interno__contains=busqueda, org_creadora=orgactivas, generado=True)
			buscarxcliente = Nota_credito.objects.filter(nombre_cliente__contains=busqueda, org_creadora=orgactivas, generado=True)
			buscarxtotal = Nota_credito.objects.filter(total_documento__contains=busqueda, org_creadora=orgactivas, generado=True)
			if buscarxfecha:
				lista = buscarxfecha.order_by(orden)
				lista = reemplazardatos_credits_notes(lista)
			elif buscarxconsec:
				lista = buscarxconsec.order_by(orden)
				lista = reemplazardatos_credits_notes(lista)
			elif buscarxcliente:
				lista = buscarxcliente.order_by(orden)
				lista = reemplazardatos_credits_notes(lista)
			elif buscarxtotal:
				lista = buscarxtotal.order_by(orden)
				lista = reemplazardatos_credits_notes(lista)
			else:
				lista = Nota_credito.objects.filter(org_creadora=orgactivas, generado=True).order_by('-consecutivo_interno')
				lista = reemplazardatos_credits_notes(lista)
	creditnotes = Nota_credito.objects.filter(org_creadora=orgactivas, generado=True).order_by('-consecutivo_interno')
	creditnotes = reemplazardatos_credits_notes(creditnotes)
	return render(request, 'groway/detalle_nota_credito.html', {'orgactivas':orgactivas, 'creditnote':creditnote, 'creditnotes':creditnotes, 'lista':lista, 'nohaynotas':nohaynotas, 'nohayconsecutivo':nohayconsecutivo, 'factura_generadora':factura_generadora,
		'cotizacion_generadora':cotizacion_generadora, 'remisionesgeneradas':remisionesgeneradas})

def pdf_nota_credito(request, pk):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	consecutivo_fac = Consecutivo_documento.objects.filter(tipo_de_documento='FVE', org_creadora=orgactivas)
	if consecutivo_fac:
		consecutivo_fac = consecutivo_fac.get(tipo_de_documento='FVE', org_creadora=orgactivas)
	else:
		consecutivo_fac = None
	creditnote = get_object_or_404(Nota_credito, pk=pk)
	creditnote = reemplazardatos_credit_note(creditnote)
	template = get_template('groway/pdf_nota_credito.html')
	consec = creditnote.consecutivo_interno
	context = {'creditnote':creditnote, 'consecutivo_fac':consecutivo_fac, 'orgactivas':orgactivas}
	html = template.render(context)
	result = BytesIO()
	pdf = pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=result, link_callback=fetch_resources)
	if pdf:
		response = HttpResponse(result.getvalue(), content_type='application/pdf')
		filename = "Nota crédito %s.pdf"%(consec)
		content = "inline; filename = %s"%(filename)
		response['Content-Disposition'] = content
		return response
	return HttpResponse("Not found")

@login_required
def notas_debito(request):
	lista ="valor"
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayconsecutivo = Consecutivo_documento.objects.filter(tipo_de_documento='NDT', org_creadora=orgactivas).count()
	nohaynotas = Nota_debito.objects.filter(org_creadora=orgactivas, generado=True).count()
	if request.method == "POST":
			dic = request.POST
			busqueda = dic["buscar"]
			orden = dic["ordenar"]
			buscarxfecha = Nota_debito.objects.filter(fecha_emision__contains=busqueda, org_creadora=orgactivas, generado=True)
			buscarxconsec = Nota_debito.objects.filter(consecutivo_interno__contains=busqueda, org_creadora=orgactivas, generado=True)
			buscarxcliente = Nota_debito.objects.filter(nombre_cliente__contains=busqueda, org_creadora=orgactivas, generado=True)
			buscarxtotal = Nota_debito.objects.filter(total_documento__contains=busqueda, org_creadora=orgactivas, generado=True)
			if buscarxfecha:
				lista = buscarxfecha.order_by(orden)
				lista = reemplazardatos_debits_notes(lista)
			elif buscarxconsec:
				lista = buscarxconsec.order_by(orden)
				lista = reemplazardatos_debits_notes(lista)
			elif buscarxcliente:
				lista = buscarxcliente.order_by(orden)
				lista = reemplazardatos_debits_notes(lista)
			elif buscarxtotal:
				lista = buscarxtotal.order_by(orden)
				lista = reemplazardatos_debits_notes(lista)
			else:
				lista = Nota_debito.objects.filter(org_creadora=orgactivas, generado=True).order_by('-consecutivo_interno')
				lista = reemplazardatos_debits_notes(lista)
	debitnotes = Nota_debito.objects.filter(org_creadora=orgactivas, generado=True).order_by('-consecutivo_interno')
	debitnotes = reemplazardatos_debits_notes(debitnotes)
	return render(request, 'groway/notas_debito.html', {'orgactivas':orgactivas, 'debitnotes':debitnotes, 'lista':lista, 'nohaynotas':nohaynotas, 'nohayconsecutivo':nohayconsecutivo})


def detalle_nota_debito(request, pk):
	lista ="valor"
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayconsecutivo = Consecutivo_documento.objects.filter(tipo_de_documento='NCT', org_creadora=orgactivas).count()
	nohaynotas = Nota_debito.objects.filter(org_creadora=orgactivas, generado=True).count()
	debitnote = get_object_or_404(Nota_debito, pk=pk)
	debitnote = reemplazardatos_debit_note(debitnote)
	factura_generadora = Factura_de_venta.objects.filter(referencia_notadebito=debitnote.consecutivo_interno, org_creadora=orgactivas)
	if factura_generadora:
		factura_generadora = factura_generadora.get(referencia_notadebito=debitnote.consecutivo_interno, org_creadora=orgactivas)
	else:
		factura_generadora = None
	cotizacion_generadora = Cotizacion.objects.filter(referencia_factura=debitnote.referencia_factura, org_creadora=orgactivas)
	if cotizacion_generadora:
		cotizacion_generadora = cotizacion_generadora.get(referencia_factura=debitnote.referencia_factura, org_creadora=orgactivas)
	else:
		cotizacion_generadora = None
	remisionesgeneradas = Remision.objects.filter(referencia_factura=debitnote.referencia_factura, org_creadora=orgactivas).count()
	if remisionesgeneradas:
		remisionesgeneradas = Remision.objects.get(referencia_factura=debitnote.referencia_factura, org_creadora=orgactivas)
	else:
		remisionesgeneradas = 0
	if request.method == "POST":
			dic = request.POST
			busqueda = dic["buscar"]
			orden = dic["ordenar"]
			buscarxfecha = Nota_debito.objects.filter(fecha_emision__contains=busqueda, org_creadora=orgactivas, generado=True)
			buscarxconsec = Nota_debito.objects.filter(consecutivo_interno__contains=busqueda, org_creadora=orgactivas, generado=True)
			buscarxcliente = Nota_debito.objects.filter(nombre_cliente__contains=busqueda, org_creadora=orgactivas, generado=True)
			buscarxtotal = Nota_debito.objects.filter(total_documento__contains=busqueda, org_creadora=orgactivas, generado=True)
			if buscarxfecha:
				lista = buscarxfecha.order_by(orden)
				lista = reemplazardatos_debits_notes(lista)
			elif buscarxconsec:
				lista = buscarxconsec.order_by(orden)
				lista = reemplazardatos_debits_notes(lista)
			elif buscarxcliente:
				lista = buscarxcliente.order_by(orden)
				lista = reemplazardatos_debits_notes(lista)
			elif buscarxtotal:
				lista = buscarxtotal.order_by(orden)
				lista = reemplazardatos_debits_notes(lista)
			else:
				lista = Nota_debito.objects.filter(org_creadora=orgactivas, generado=True).order_by('-consecutivo_interno')
				lista = reemplazardatos_debits_notes(lista)
	debitnotes = Nota_debito.objects.filter(org_creadora=orgactivas, generado=True).order_by('-consecutivo_interno')
	debitnotes = reemplazardatos_debits_notes(debitnotes)
	return render(request, 'groway/detalle_nota_debito.html', {'orgactivas':orgactivas, 'debitnote':debitnote, 'debitnotes':debitnotes, 'lista':lista, 'nohaynotas':nohaynotas, 'nohayconsecutivo':nohayconsecutivo, 'factura_generadora':factura_generadora,
		'cotizacion_generadora':cotizacion_generadora, 'remisionesgeneradas':remisionesgeneradas})

def pdf_nota_debito(request, pk):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	consecutivo_fac = Consecutivo_documento.objects.filter(tipo_de_documento='FVE', org_creadora=orgactivas)
	if consecutivo_fac:
		consecutivo_fac = consecutivo_fac.get(tipo_de_documento='FVE', org_creadora=orgactivas)
	else:
		consecutivo_fac = None
	debitnote = get_object_or_404(Nota_debito, pk=pk)
	debitnote = reemplazardatos_debit_note(debitnote)
	template = get_template('groway/pdf_nota_debito.html')
	consec = debitnote.consecutivo_interno
	context = {'debitnote':debitnote, 'consecutivo_fac':consecutivo_fac, 'orgactivas':orgactivas}
	html = template.render(context)
	result = BytesIO()
	pdf = pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=result, link_callback=fetch_resources)
	if pdf:
		response = HttpResponse(result.getvalue(), content_type='application/pdf')
		filename = "Nota débito %s.pdf"%(consec)
		content = "inline; filename = %s"%(filename)
		response['Content-Disposition'] = content
		return response
	return HttpResponse("Not found")

@login_required
def facturas_compra(request):
	lista ="valor"
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayproveedores = Contacto.objects.filter(relacion_activa="PD", org_creadora=orgactivas).count()
	nohayinsumo = Insumo.objects.filter(org_creadora=orgactivas).count()
	nohayconsecutivo = Consecutivo_documento.objects.filter(tipo_de_documento='FCO', org_creadora=orgactivas).count()
	nohayterminospago = Termino_de_pago.objects.filter(org_creadora=orgactivas).count()
	nohayfacturas = Factura_de_compra.objects.filter(org_creadora=orgactivas, generado=True).count()
	if request.method == "POST":
			dic = request.POST
			busqueda = dic["buscar"]
			orden = dic["ordenar"]
			buscarxfecha = Factura_de_compra.objects.filter(fecha_emision__contains=busqueda, org_creadora=orgactivas, generado=True)
			buscarxconsec = Factura_de_compra.objects.filter(consecutivo_interno__contains=busqueda, org_creadora=orgactivas, generado=True)
			buscarxproveedor = Factura_de_compra.objects.filter(nombre_proveedor__contains=busqueda, org_creadora=orgactivas, generado=True)
			buscarxtotal = Factura_de_compra.objects.filter(total_documento__contains=busqueda, org_creadora=orgactivas, generado=True)
			if buscarxfecha:
				lista = buscarxfecha.order_by(orden)
				lista = reemplazardatos_facturas_comp(lista)
			elif buscarxconsec:
				lista = buscarxconsec.order_by(orden)
				lista = reemplazardatos_facturas_comp(lista)
			elif buscarxcliente:
				lista = buscarxcliente.order_by(orden)
				lista = reemplazardatos_facturas_comp(lista)
			elif buscarxtotal:
				lista = buscarxtotal.order_by(orden)
				lista = reemplazardatos_facturas_comp(lista)
			else:
				lista = Factura_de_compra.objects.filter(org_creadora=orgactivas, generado=True).order_by('-consecutivo_interno')
				lista = reemplazardatos_facturas_comp(lista)
	facturas_comp = Factura_de_compra.objects.filter(org_creadora=orgactivas, generado=True).order_by('-consecutivo_interno')
	facturas_comp = reemplazardatos_facturas_comp(facturas_comp)
	return render(request, 'groway/facturas_compra.html', {'orgactivas':orgactivas, 'facturas_comp':facturas_comp, 'lista':lista, 'nohayfacturas':nohayfacturas, 'nohayterminospago':nohayterminospago, 'nohayconsecutivo':nohayconsecutivo,
		'nohayproveedores':nohayproveedores, 'nohayinsumo':nohayinsumo})


def nueva_fac_comp_ing(request):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	proveedores_fco = Contacto.objects.filter(relacion_activa="PD", org_creadora=orgactivas).order_by('nombre_legal')
	insumos_fco = Insumo.objects.filter(org_creadora=orgactivas).order_by('codigo')
	nohayproveedores = Contacto.objects.filter(relacion_activa="PD", org_creadora=orgactivas).count()
	nohayinsumo = Insumo.objects.filter(org_creadora=orgactivas).count()
	nohayconsecutivo = Consecutivo_documento.objects.filter(tipo_de_documento='FCO', org_creadora=orgactivas).count()
	nohayterminospago = Termino_de_pago.objects.filter(org_creadora=orgactivas).count()
	nohayfacturas = Factura_de_compra.objects.filter(org_creadora=orgactivas, generado=True).count()
	documentoborrador = Factura_de_compra.objects.filter(org_creadora=orgactivas, generado=False).last()
	if request.method == "POST":
		if documentoborrador:
			form = Factura_de_compraForm(request.POST, instance=documentoborrador)
		else:
			form = Factura_de_compraForm(request.POST)
		dic = request.POST
		prov = dic["proveedores_fco"]
		item_1 = dic["items_1"]
		item_2 = dic["items_2"]
		item_3 = dic["items_3"]
		item_4 = dic["items_4"]
		item_5 = dic["items_5"]
		if form.is_valid():
			factura_comp = form.save(commit=False)
			factura_comp.org_creadora = orgactivas
			factura_comp.comprador = request.user
			factura_comp.proveedor = prov
			if item_1 != '0':
				factura_comp.item_1 = item_1
			if item_2 != '0':
				factura_comp.item_2 = item_2
			if item_3 != '0':
				factura_comp.item_3 = item_3
			if item_4 != '0':
				factura_comp.item_4 = item_4
			if item_5 != '0':
				factura_comp.item_5 = item_5
			factura_comp.auto_info_organizacion()
			factura_comp.auto_info_proveedor()
			factura_comp.info_item()
			factura_comp.save()
			return redirect('nueva_fac_comp_cal', pk=factura_comp.pk)
	else:
		form = Factura_de_compraForm()
	facturas_comp = Factura_de_compra.objects.filter(org_creadora=orgactivas, generado=True).order_by('-consecutivo_interno')
	facturas_comp = reemplazardatos_facturas_comp(facturas_comp)
	return render(request, 'groway/nueva_factura_compra.html', {'form':form, 'orgactivas':orgactivas, 'facturas_comp':facturas_comp, 'nohayfacturas':nohayfacturas, 'nohayterminospago':nohayterminospago, 'nohayconsecutivo':nohayconsecutivo,
		'proveedores_fco':proveedores_fco, 'insumos_fco':insumos_fco, 'nohayproveedores':nohayproveedores, 'nohayinsumo':nohayinsumo})

def nueva_fac_comp_cal(request, pk):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	proveedores_fco = Contacto.objects.filter(relacion_activa="PD", org_creadora=orgactivas).order_by('nombre_legal')
	insumos_fco = Insumo.objects.filter(org_creadora=orgactivas).order_by('codigo')
	nohayproveedores = Contacto.objects.filter(relacion_activa="PD", org_creadora=orgactivas).count()
	nohayinsumo = Insumo.objects.filter(org_creadora=orgactivas).count()
	nohayconsecutivo = Consecutivo_documento.objects.filter(tipo_de_documento='FCO', org_creadora=orgactivas).count()
	nohayterminospago = Termino_de_pago.objects.filter(org_creadora=orgactivas).count()
	nohayfacturas = Factura_de_compra.objects.filter(org_creadora=orgactivas, generado=True).count()
	factura_comp = get_object_or_404(Factura_de_compra, pk=pk)
	if request.method == "POST":
		form = Factura_de_compraForm(request.POST, instance=factura_comp)
		dic = request.POST
		prov = dic["proveedores_fco"]
		item_1 = dic["items_1"]
		item_2 = dic["items_2"]
		item_3 = dic["items_3"]
		item_4 = dic["items_4"]
		item_5 = dic["items_5"]
		if form.is_valid():
			factura_comp = form.save(commit=False)
			if factura_comp.cantidad_1:
				factura_comp.org_creadora = orgactivas
				factura_comp.fecha_emision = timezone.now()
				factura_comp.comprador = request.user
				factura_comp.proveedor = prov
				if item_1 != '0':
					factura_comp.item_1 = item_1
				if item_2 != '0':
					factura_comp.item_2 = item_2
				if item_3 != '0':
					factura_comp.item_3 = item_3
				if item_4 != '0':
					factura_comp.item_4 = item_4
				if item_5 != '0':
					factura_comp.item_5 = item_5
				factura_comp.info_item()
				factura_comp.auto_info_organizacion()
				factura_comp.auto_info_proveedor()
				factura_comp.calculo_item()
				factura_comp.calculo_total_factura()
				factura_comp.save()
				return redirect('nueva_fac_comp_cal', pk=factura_comp.pk)
			else:
				return redirect('nueva_fac_comp_cal', pk=factura_comp.pk)
	else:
		form = Factura_de_compraForm(instance=factura_comp)
	facturas_comp = Factura_de_compra.objects.filter(org_creadora=orgactivas, generado=True).order_by('-consecutivo_interno')
	facturas_comp = reemplazardatos_facturas_comp(facturas_comp)
	return render(request, 'groway/nueva_factura_compra.html', {'form':form, 'orgactivas':orgactivas, 'facturas_comp':facturas_comp, 'factura_comp':factura_comp, 'nohayfacturas':nohayfacturas, 'nohayterminospago':nohayterminospago, 'nohayconsecutivo':nohayconsecutivo,
		'proveedores_fco':proveedores_fco, 'insumos_fco':insumos_fco, 'nohayproveedores':nohayproveedores, 'nohayinsumo':nohayinsumo})

def nueva_fac_comp_fin(request, pk):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	factura_comp = get_object_or_404(Factura_de_compra, pk=pk)
	factura_comp.org_creadora = orgactivas
	factura_comp.fecha_emision = timezone.now()
	factura_comp.save()
	factura_comp.tipo_impuestodoc()
	factura_comp.auto_consecutivo()
	factura_comp.generado = True
	factura_comp.save()
	return redirect('detalle_factura_compra', pk=pk)

def atras_fac_comp(request, pk):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	proveedores_fco = Contacto.objects.filter(relacion_activa="PD", org_creadora=orgactivas).order_by('nombre_legal')
	insumos_fco = Insumo.objects.filter(org_creadora=orgactivas).order_by('codigo')
	nohayproveedores = Contacto.objects.filter(relacion_activa="PD", org_creadora=orgactivas).count()
	nohayinsumo = Insumo.objects.filter(org_creadora=orgactivas).count()
	nohayconsecutivo = Consecutivo_documento.objects.filter(tipo_de_documento='FCO', org_creadora=orgactivas).count()
	nohayterminospago = Termino_de_pago.objects.filter(org_creadora=orgactivas).count()
	nohayfacturas = Factura_de_compra.objects.filter(org_creadora=orgactivas, generado=True).count()
	factura_comp = get_object_or_404(Factura_de_compra, pk=pk)
	if request.method == "POST":
		form = Factura_de_compraForm(request.POST, instance=factura_comp)
		dic = request.POST
		prov = dic["proveedores_fco"]
		item_1 = dic["items_1"]
		item_2 = dic["items_2"]
		item_3 = dic["items_3"]
		item_4 = dic["items_4"]
		item_5 = dic["items_5"]
		if form.is_valid():
			factura_comp = form.save(commit=False)
			factura_comp.comprador = request.user
			factura_comp.org_creadora = orgactivas
			factura_comp.proveedor = prov
			if item_1 != '0':
				factura_comp.item_1 = item_1
			if item_2 != '0':
				factura_comp.item_2 = item_2
			if item_3 != '0':
				factura_comp.item_3 = item_3
			if item_4 != '0':
				factura_comp.item_4 = item_4
			if item_5 != '0':
				factura_comp.item_5 = item_5
			factura_comp.auto_info_organizacion()
			factura_comp.auto_info_proveedor()
			factura_comp.info_item()
			factura_comp.save()
			return redirect('nueva_fac_comp_cal', pk=factura_comp.pk)
	else:
		form = Factura_de_compraForm(instance=factura_comp)
	facturas_comp = Factura_de_compra.objects.filter(org_creadora=orgactivas, generado=True).order_by('-consecutivo_interno')
	facturas_comp = reemplazardatos_facturas_comp(facturas_comp)
	return render(request, 'groway/nueva_factura_compra.html', {'form':form, 'orgactivas':orgactivas, 'facturas_comp':facturas_comp, 'nohayfacturas':nohayfacturas, 'nohayterminospago':nohayterminospago, 'nohayconsecutivo':nohayconsecutivo,
		'proveedores_fco':proveedores_fco, 'insumos_fco':insumos_fco, 'nohayproveedores':nohayproveedores, 'nohayinsumo':nohayinsumo})


def editar_factura_comp(request, pk):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	proveedores_fco = Contacto.objects.filter(relacion_activa="PD", org_creadora=orgactivas).order_by('nombre_legal')
	insumos_fco = Insumo.objects.filter(org_creadora=orgactivas).order_by('codigo')
	nohayproveedores = Contacto.objects.filter(relacion_activa="PD", org_creadora=orgactivas).count()
	nohayinsumo = Insumo.objects.filter(org_creadora=orgactivas).count()
	nohayconsecutivo = Consecutivo_documento.objects.filter(tipo_de_documento='FCO', org_creadora=orgactivas).count()
	nohayterminospago = Termino_de_pago.objects.filter(org_creadora=orgactivas).count()
	nohayfacturas = Factura_de_compra.objects.filter(org_creadora=orgactivas, generado=True).count()
	factura_comp = get_object_or_404(Factura_de_compra, pk=pk)
	consecutivo_factura = factura_comp.consecutivo_interno
	consecutivo_factura_pref = factura_comp.consec_inter_prefijo
	consecutivo_factura_num = factura_comp.consec_inter_numero
	fecha_creacion = factura_comp.fecha_emision
	comprador = factura_comp.comprador
	if request.method == "POST":
		form = Factura_de_compraForm(request.POST, instance=factura_comp)
		dic = request.POST
		prov = dic["proveedores_fco"]
		item_1 = dic["items_1"]
		item_2 = dic["items_2"]
		item_3 = dic["items_3"]
		item_4 = dic["items_4"]
		item_5 = dic["items_5"]
		if form.is_valid():
			factura_comp = form.save(commit=False)
			factura_comp.fecha_emision = fecha_creacion
			factura_comp.consecutivo_interno = consecutivo_factura
			factura_comp.consec_inter_prefijo = consecutivo_factura_pref
			factura_comp.consec_inter_numero = consecutivo_factura_num
			factura_comp.comprador = comprador
			factura_comp.org_creadora = orgactivas
			factura_comp.generado = True
			factura_comp.proveedor = prov
			if item_1 != '0':
				factura_comp.item_1 = item_1
			if item_2 != '0':
				factura_comp.item_2 = item_2
			if item_3 != '0':
				factura_comp.item_3 = item_3
			if item_4 != '0':
				factura_comp.item_4 = item_4
			if item_5 != '0':
				factura_comp.item_5 = item_5
			factura_comp.info_item()
			factura_comp.auto_info_organizacion()
			factura_comp.auto_info_proveedor()
			factura_comp.calculo_item()
			factura_comp.calculo_total_factura()
			factura_comp.tipo_impuestodoc()
			factura_comp.save()
			return redirect('detalle_factura_compra', pk=factura_comp.pk)
	else:
		form = Factura_de_compraForm(instance=factura_comp)
	facturas_comp = Factura_de_compra.objects.filter(org_creadora=orgactivas, generado=True).order_by('-consecutivo_interno')
	facturas_comp = reemplazardatos_facturas_comp(facturas_comp)
	return render(request, 'groway/editar_factura_comp.html', {'form':form, 'orgactivas':orgactivas, 'facturas_comp':facturas_comp, 'factura_comp':factura_comp, 'nohayfacturas':nohayfacturas, 'nohayterminospago':nohayterminospago, 'nohayconsecutivo':nohayconsecutivo,
		'proveedores_fco':proveedores_fco, 'insumos_fco':insumos_fco, 'nohayproveedores':nohayproveedores, 'nohayinsumo':nohayinsumo})

def detalle_factura_compra(request, pk):
	lista ="valor"
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayproveedores = Contacto.objects.filter(relacion_activa="PD", org_creadora=orgactivas).count()
	nohayinsumo = Insumo.objects.filter(org_creadora=orgactivas).count()
	nohayconsecutivo = Consecutivo_documento.objects.filter(tipo_de_documento='FCO', org_creadora=orgactivas).count()
	nohayterminospago = Termino_de_pago.objects.filter(org_creadora=orgactivas).count()
	nohayfacturas = Factura_de_compra.objects.filter(org_creadora=orgactivas, generado=True).count()
	factura_comp = get_object_or_404(Factura_de_compra, pk=pk)
	factura_comp = reemplazardatos_factura_comp(factura_comp)
	if request.method == "POST":
		dic = request.POST
		busqueda = dic["buscar"]
		orden = dic["ordenar"]
		buscarxfecha = Factura_de_compra.objects.filter(fecha_emision__contains=busqueda, org_creadora=orgactivas, generado=True)
		buscarxconsec = Factura_de_compra.objects.filter(consecutivo_interno__contains=busqueda, org_creadora=orgactivas, generado=True)
		buscarxproveedor = Factura_de_compra.objects.filter(nombre_proveedor__contains=busqueda, org_creadora=orgactivas, generado=True)
		buscarxtotal = Factura_de_compra.objects.filter(total_documento__contains=busqueda, org_creadora=orgactivas, generado=True)
		if buscarxfecha:
			lista = buscarxfecha.order_by(orden)
			lista = reemplazardatos_facturas_comp(lista)
		elif buscarxconsec:
			lista = buscarxconsec.order_by(orden)
			lista = reemplazardatos_facturas_comp(lista)
		elif buscarxcliente:
			lista = buscarxcliente.order_by(orden)
			lista = reemplazardatos_facturas_comp(lista)
		elif buscarxtotal:
			lista = buscarxtotal.order_by(orden)
			lista = reemplazardatos_facturas_comp(lista)
		else:
			lista = Factura_de_compra.objects.filter(org_creadora=orgactivas, generado=True).order_by('-consecutivo_interno')
			lista = reemplazardatos_facturas_comp(lista)
	facturas_comp = Factura_de_compra.objects.filter(org_creadora=orgactivas, generado=True).order_by('-consecutivo_interno')
	facturas_comp = reemplazardatos_facturas_comp(facturas_comp)
	return render(request, 'groway/detalle_factura_compra.html', {'orgactivas':orgactivas, 'factura_comp':factura_comp, 'facturas_comp':facturas_comp, 'lista':lista, 'nohayfacturas':nohayfacturas, 'nohayterminospago':nohayterminospago, 'nohayconsecutivo':nohayconsecutivo,
	 'nohayproveedores':nohayproveedores, 'nohayinsumo':nohayinsumo})

def pdf_factura_compra(request, pk):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	factura_comp = get_object_or_404(Factura_de_compra, pk=pk)
	factura_comp = reemplazardatos_factura_comp(factura_comp)
	template = get_template('groway/pdf_factura_compra.html')
	consec = factura_comp.consecutivo_interno
	context = {'factura_comp':factura_comp, 'orgactivas':orgactivas}
	html = template.render(context)
	result = BytesIO()
	pdf = pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=result, link_callback=fetch_resources)
	if pdf:
		response = HttpResponse(result.getvalue(), content_type='application/pdf')
		filename = "Factura de compra %s.pdf"%(consec)
		content = "inline; filename = %s"%(filename)
		response['Content-Disposition'] = content
		return response
	return HttpResponse("Not found")


@login_required
def gastos_registro(request):
	lista ="valor"
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohaygastos = Gastos_registro.objects.filter(org_creadora=orgactivas).count()
	if request.method == "POST":
		dic = request.POST
		busqueda = dic["buscar"]
		orden = dic["ordenar"]
		buscarxfecha = Gastos_registro.objects.filter(fecha_emision__contains=busqueda, org_creadora=orgactivas)
		buscarxconcepto = Gastos_registro.objects.filter(concepto_gasto__contains=busqueda, org_creadora=orgactivas)
		if buscarxfecha:
			lista = buscarxfecha.order_by(orden)
			lista = reemplazardatos_gastos(lista)
		elif buscarxconcepto:
			lista = buscarxconcepto.order_by(orden)
			lista = reemplazardatos_gastos(lista)
		else:
			lista = Gastos_registro.objects.filter(org_creadora=orgactivas).order_by('-fecha_emision')
			lista = reemplazardatos_gastos(lista)
	gastos = Gastos_registro.objects.filter(org_creadora=orgactivas).order_by('-fecha_emision')
	gastos = reemplazardatos_gastos(gastos)
	return render(request, 'groway/gastos_registro.html', {'orgactivas':orgactivas, 'gastos':gastos, 'lista':lista, 'nohaygastos':nohaygastos})

def nuevo_gasto(request):
	form = "valor"
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohaygastos = Gastos_registro.objects.filter(org_creadora=orgactivas).count()
	if request.method == "POST":
		form = Gastos_registroForm(request.POST)
		if form.is_valid():
			gasto = form.save(commit=False)
			gasto.fecha_emision = timezone.now()
			gasto.org_creadora = orgactivas
			gasto.save()
			return redirect('detalle_gasto', pk=gasto.pk)
	else:
		form = Gastos_registroForm()
	gastos = Gastos_registro.objects.filter(org_creadora=orgactivas).order_by('-fecha_emision')
	gastos = reemplazardatos_gastos(gastos)
	return render(request, 'groway/nuevo_gasto.html', {'form':form, 'orgactivas':orgactivas, 'gastos':gastos, 'nohaygastos':nohaygastos})

def editar_gasto(request, pk):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohaygastos = Gastos_registro.objects.filter(org_creadora=orgactivas).count()
	gasto = get_object_or_404(Gastos_registro, pk=pk)
	org_gasto = gasto.org_creadora
	fecha_gasto = gasto.fecha_emision
	if request.method == "POST":
		form = Gastos_registroForm(request.POST, instance=gasto)
		if form.is_valid():
			gasto = form.save(commit=False)
			gasto.fecha_emision = fecha_gasto
			gasto.org_creadora = org_gasto
			gasto.save()
			return redirect('detalle_gasto', pk=gasto.pk)
	else:
		form = Gastos_registroForm(instance=gasto)
	gastos = Gastos_registro.objects.filter(org_creadora=orgactivas).order_by('-fecha_emision')
	gastos = reemplazardatos_gastos(gastos)
	return render(request, 'groway/nuevo_gasto.html', {'form':form, 'orgactivas':orgactivas, 'gastos':gastos, 'gasto':gasto, 'nohaygastos':nohaygastos})

def eliminar_gasto(request, pk):
	gasto = get_object_or_404(Gastos_registro, pk=pk)
	gasto.delete()
	return redirect('gastos_registro')

def detalle_gasto(request, pk):
	lista ="valor"
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohaygastos = Gastos_registro.objects.filter(org_creadora=orgactivas).count()
	if request.method == "POST":
		dic = request.POST
		busqueda = dic["buscar"]
		orden = dic["ordenar"]
		buscarxfecha = Gastos_registro.objects.filter(fecha_emision__contains=busqueda, org_creadora=orgactivas)
		buscarxconcepto = Gastos_registro.objects.filter(concepto_gasto__contains=busqueda, org_creadora=orgactivas)
		if buscarxfecha:
			lista = buscarxfecha.order_by(orden)
			lista = reemplazardatos_gastos(lista)
		elif buscarxconcepto:
			lista = buscarxconcepto.order_by(orden)
			lista = reemplazardatos_gastos(lista)
		else:
			lista = Gastos_registro.objects.filter(org_creadora=orgactivas).order_by('-fecha_emision')
			lista = reemplazardatos_gastos(lista)
	gastos = Gastos_registro.objects.filter(org_creadora=orgactivas).order_by('-fecha_emision')
	gastos = reemplazardatos_gastos(gastos)
	gasto = get_object_or_404(Gastos_registro, pk=pk)
	gasto = reemplazardatos_gasto(gasto)
	return render(request, 'groway/detalle_gasto.html', {'orgactivas':orgactivas, 'gastos':gastos, 'gasto':gasto, 'nohaygastos':nohaygastos, 'lista':lista})


@login_required
def reportes_crecimiento(request):
	lista ="valor"
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayreportes = Crecimiento.objects.filter(org_creadora=orgactivas, guardada=True).count()
	nohayfacturas = Factura_de_venta.objects.filter(org_creadora=orgactivas, generado=True).count()
	if request.method == "POST":
			dic = request.POST
			busqueda = dic["buscar"]
			orden = dic["ordenar"]
			buscarxfecha = Crecimiento.objects.filter(fecha_inicio__contains=busqueda, org_creadora=orgactivas, guardada=True)
			buscarxnombre = Crecimiento.objects.filter(nombre__contains=busqueda, org_creadora=orgactivas, guardada=True)
			buscarxmetrica = Crecimiento.objects.filter(metrica_crecimiento__contains=busqueda, org_creadora=orgactivas, guardada=True)
			if buscarxfecha:
				lista = buscarxfecha.order_by(orden)
				lista = reemplazardatos_reportes(lista)
			elif buscarxnombre:
				lista = buscarxnombre.order_by(orden)
				lista = reemplazardatos_reportes(lista)
			elif buscarxmetrica:
				lista = buscarxmetrica.order_by(orden)
				lista = reemplazardatos_reportes(lista)
			else:
				lista = Crecimiento.objects.filter(org_creadora=orgactivas, guardada=True).order_by('-fecha_creacion')
				lista = reemplazardatos_reportes(lista)
	reportes = Crecimiento.objects.filter(org_creadora=orgactivas, guardada=True).order_by('-fecha_creacion')
	reportes = reemplazardatos_reportes(reportes)
	return render(request, 'groway/reportes_crecimiento.html', {'orgactivas':orgactivas, 'reportes':reportes, 'lista':lista, 'nohayfacturas':nohayfacturas, 'nohayreportes':nohayreportes})

def grafica_nueva(request):
	locale.setlocale(locale.LC_ALL,'')
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	reporte = Crecimiento.objects.filter(org_creadora=orgactivas, guardada=False).last()
	if reporte.fecha_fin == None or reporte.fecha_fin == reporte.fecha_inicio:
		dia = reporte.fecha_inicio.day
		mes = reporte.fecha_inicio.month
		año = reporte.fecha_inicio.year
		desface_tiempo = timedelta(hours=5)
		inicio = datetime(año, mes, dia, 0, 0, 0, tzinfo=pytz.UTC)
		inicio = inicio + desface_tiempo
		fin = datetime(año, mes, dia, 23, 59, 59, tzinfo=pytz.UTC)
		fin = fin + desface_tiempo
		hora_a_hora = timedelta(hours=5)
		inicio_hora = inicio
		fin_hora = inicio_hora + hora_a_hora
		ganancias = []
		ventas = []
		horas = []
		while inicio_hora <= fin:
			facturas = Factura_de_venta.objects.filter(fecha_emision__range=(inicio_hora, fin_hora), org_creadora=orgactivas, generado=True, anulada=False).order_by('fecha_emision')
			total_facturas = 0
			total_impuestos = 0
			for factura in facturas:
				venta = factura.total_documento/1000000
				total_facturas = total_facturas + venta
				total_impuestos = total_impuestos + (factura.iva_total/1000000) + (factura.ico_total/1000000)
			creditnotes_concep_1 = Nota_credito.objects.filter(fecha_emision__range=(inicio_hora, fin_hora), org_creadora=orgactivas, generado=True, concepto_nota_credito='1').order_by('fecha_emision')
			creditnotes_concep_3 = Nota_credito.objects.filter(fecha_emision__range=(inicio_hora, fin_hora), org_creadora=orgactivas, generado=True, concepto_nota_credito='3').order_by('fecha_emision')
			creditnotes_concep_4 = Nota_credito.objects.filter(fecha_emision__range=(inicio_hora, fin_hora), org_creadora=orgactivas, generado=True, concepto_nota_credito='4').order_by('fecha_emision')
			debitnotes = Nota_debito.objects.filter(fecha_emision__range=(inicio_hora, fin_hora), org_creadora=orgactivas, generado=True).order_by('fecha_emision')
			total_cn_1 = 0
			imp_cn_1 = 0
			for creditnote in creditnotes_concep_1:
				total = creditnote.total_documento/1000000
				total_cn_1 = total_cn_1 + total
				imp_cn_1 = imp_cn_1 + (creditnote.iva_total/1000000) + (creditnote.ico_total/1000000)
			total_cn_3 = 0
			imp_cn_3 = 0
			for creditnote in creditnotes_concep_3:
				total = creditnote.total_documento/1000000 - creditnote.descuento_rebaja/1000000
				total_cn_3 = total_cn_3 + total
				imp_cn_3 = imp_cn_3 + (creditnote.iva_total/1000000) + (creditnote.ico_total/1000000)
			total_cn_4 = 0
			imp_cn_4 = 0
			for creditnote in creditnotes_concep_4:
				total = creditnote.total_documento/1000000 - creditnote.descuento_rebaja/1000000
				total_cn_4 = total_cn_4 + total
				imp_cn_4 = imp_cn_4 + (creditnote.iva_total/1000000) + (creditnote.ico_total/1000000)
			total_dn = 0
			imp_dn = 0
			for debitnote in debitnotes:
				total = debitnote.total_documento/1000000 + debitnote.cargo_interes/1000000
				total_dn = total_dn + total
				imp_dn = imp_dn + (debitnote.iva_total/1000000) + (debitnote.ico_total/1000000)
			total_ventas = 0
			total_ventas = total_facturas + total_cn_1 + total_cn_3 + total_cn_4 + total_dn
			ventas.append(total_ventas)
			hora = inicio_hora
			hora = hora.strftime("%I:%M %p")
			horas.append(hora)
			facturas_comp = Factura_de_compra.objects.filter(fecha_emision__range=(inicio_hora, fin_hora), org_creadora=orgactivas, generado=True).order_by('fecha_emision')
			total_compras = 0
			for factura_c in facturas_comp:
				compra = factura_c.total_documento/1000000
				total_compras = total_compras + compra
			gastos = Gastos_registro.objects.filter(fecha_emision__range=(inicio_hora, fin_hora), org_creadora=orgactivas).order_by('fecha_emision')
			total_gastos = 0
			for gasto in gastos:
				gasto = gasto.valor_gasto/1000000
				total_gastos = total_gastos + gasto
			total_ganancias = 0
			total_ganancias = total_facturas + total_cn_1 + total_cn_3 + total_cn_4 + total_dn - total_impuestos - imp_cn_1 - imp_cn_3 - imp_cn_4 - imp_dn - total_compras - total_gastos
			ganancias.append(total_ganancias)
			inicio_hora = inicio_hora + hora_a_hora
			fin_hora = inicio_hora + hora_a_hora
		x = np.array(horas)
		y = np.array(ventas)
		x_2 = np.array(horas)
		y_2 = np.array(ganancias)
		f = plt.figure()
		ejes = f.add_axes([0.15, 0.15, 0.75, 0.75])
		if reporte.metrica_crecimiento == 'V':
			ejes.plot(x,y,'g')
		elif reporte.metrica_crecimiento == 'G': 
			ejes.plot(x,y,'g',x_2,y_2,'r')
			ejes.legend(['Ventas','Ganancias'])
		ejes.set_xlabel("Hora")
		ejes.set_ylabel("Millones (COP)")
		ejes.set_title("Reporte " + reporte.fecha_inicio.strftime("%A %d %b %Y"))
		buf = io.BytesIO()
		canvas =FigureCanvasAgg(f)
		canvas.print_png(buf)
		response = HttpResponse(buf.getvalue(), content_type='image/png')
		f.clear()
		response['Content-Length'] = str(len(response.content))
		return response
	else:
		dia_i = reporte.fecha_inicio.day
		mes_i = reporte.fecha_inicio.month
		año_i = reporte.fecha_inicio.year
		dia_f = reporte.fecha_fin.day
		mes_f = reporte.fecha_fin.month
		año_f = reporte.fecha_fin.year
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
			ventas = []
			dias = []
			while inicio_dia <= fin:
				facturas = Factura_de_venta.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True, anulada=False).order_by('fecha_emision')
				total_facturas = 0
				total_impuestos = 0
				for factura in facturas:
					venta = factura.total_documento/1000000
					total_facturas = total_facturas + venta
					total_impuestos = total_impuestos + (factura.iva_total/1000000) + (factura.ico_total/1000000)
				creditnotes_concep_1 = Nota_credito.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True, concepto_nota_credito='1').order_by('fecha_emision')
				creditnotes_concep_3 = Nota_credito.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True, concepto_nota_credito='3').order_by('fecha_emision')
				creditnotes_concep_4 = Nota_credito.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True, concepto_nota_credito='4').order_by('fecha_emision')
				debitnotes = Nota_debito.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True).order_by('fecha_emision')
				total_cn_1 = 0
				imp_cn_1 = 0
				for creditnote in creditnotes_concep_1:
					total = creditnote.total_documento/1000000
					total_cn_1 = total_cn_1 + total
					imp_cn_1 = imp_cn_1 + (creditnote.iva_total/1000000) + (creditnote.ico_total/1000000)
				total_cn_3 = 0
				imp_cn_3 = 0
				for creditnote in creditnotes_concep_3:
					total = creditnote.total_documento/1000000 - creditnote.descuento_rebaja/1000000
					total_cn_3 = total_cn_3 + total
					imp_cn_3 = imp_cn_3 + (creditnote.iva_total/1000000) + (creditnote.ico_total/1000000)
				total_cn_4 = 0
				imp_cn_4 = 0
				for creditnote in creditnotes_concep_4:
					total = creditnote.total_documento/1000000 - creditnote.descuento_rebaja/1000000
					total_cn_4 = total_cn_4 + total
					imp_cn_4 = imp_cn_4 + (creditnote.iva_total/1000000) + (creditnote.ico_total/1000000)
				total_dn = 0
				imp_dn = 0
				for debitnote in debitnotes:
					total = debitnote.total_documento/1000000 + debitnote.cargo_interes/1000000
					total_dn = total_dn + total
					imp_dn = imp_dn + (debitnote.iva_total/1000000) + (debitnote.ico_total/1000000)
				total_ventas = 0
				total_ventas = total_facturas + total_cn_1 + total_cn_3 + total_cn_4 + total_dn
				ventas.append(total_ventas)
				dia = inicio_dia
				dia = dia.strftime("%a %d")
				dias.append(dia)
				facturas_comp = Factura_de_compra.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True).order_by('fecha_emision')
				total_compras = 0
				for factura_c in facturas_comp:
					compra = factura_c.total_documento/1000000
					total_compras = total_compras + compra
				gastos = Gastos_registro.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas).order_by('fecha_emision')
				total_gastos = 0
				for gasto in gastos:
					gasto = gasto.valor_gasto/1000000
					total_gastos = total_gastos + gasto
				total_ganancias = 0
				total_ganancias = total_facturas + total_cn_1 + total_cn_3 + total_cn_4 + total_dn - total_impuestos - imp_cn_1 - imp_cn_3 - imp_cn_4 - imp_dn - total_compras - total_gastos
				ganancias.append(total_ganancias)
				inicio_dia = inicio_dia + dia_a_dia
				fin_dia = inicio_dia + dia_a_dia
			x = np.array(dias)
			y = np.array(ventas)
			x_2 = np.array(dias)
			y_2 = np.array(ganancias)
			f = plt.figure()
			ejes = f.add_axes([0.15, 0.15, 0.75, 0.75])
			if reporte.metrica_crecimiento == 'V':
				ejes.plot(x,y,'g')
			elif reporte.metrica_crecimiento == 'G': 
				ejes.plot(x,y,'g',x_2,y_2,'r')
				ejes.legend(['Ventas','Ganancias'])
			ejes.set_xlabel("Día")
			ejes.set_ylabel("Millones (COP)")
			ejes.set_title("Reporte " + reporte.fecha_inicio.strftime("%d %b") + " al " + reporte.fecha_fin.strftime("%d %b %Y"))
			buf = io.BytesIO()
			canvas =FigureCanvasAgg(f)
			canvas.print_png(buf)
			response = HttpResponse(buf.getvalue(), content_type='image/png')
			f.clear()
			response['Content-Length'] = str(len(response.content))
			return response

		elif periodo > semana and periodo <= mes:
			semana_a_semana = timedelta(days=7)
			inicio_dia = inicio
			fin_dia = inicio_dia + semana_a_semana
			ganancias = []
			ventas = []
			semanas = []
			while inicio_dia <= fin:
				facturas = Factura_de_venta.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True, anulada=False).order_by('fecha_emision')
				total_facturas = 0
				total_impuestos = 0
				for factura in facturas:
					venta = factura.total_documento/1000000
					total_facturas = total_facturas + venta
					total_impuestos = total_impuestos + (factura.iva_total/1000000) + (factura.ico_total/1000000)
				creditnotes_concep_1 = Nota_credito.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True, concepto_nota_credito='1').order_by('fecha_emision')
				creditnotes_concep_3 = Nota_credito.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True, concepto_nota_credito='3').order_by('fecha_emision')
				creditnotes_concep_4 = Nota_credito.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True, concepto_nota_credito='4').order_by('fecha_emision')
				debitnotes = Nota_debito.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True).order_by('fecha_emision')
				total_cn_1 = 0
				imp_cn_1 = 0
				for creditnote in creditnotes_concep_1:
					total = creditnote.total_documento/1000000
					total_cn_1 = total_cn_1 + total
					imp_cn_1 = imp_cn_1 + (creditnote.iva_total/1000000) + (creditnote.ico_total/1000000)
				total_cn_3 = 0
				imp_cn_3 = 0
				for creditnote in creditnotes_concep_3:
					total = creditnote.total_documento/1000000 - creditnote.descuento_rebaja/1000000
					total_cn_3 = total_cn_3 + total
					imp_cn_3 = imp_cn_3 + (creditnote.iva_total/1000000) + (creditnote.ico_total/1000000)
				total_cn_4 = 0
				imp_cn_4 = 0
				for creditnote in creditnotes_concep_4:
					total = creditnote.total_documento/1000000 - creditnote.descuento_rebaja/1000000
					total_cn_4 = total_cn_4 + total
					imp_cn_4 = imp_cn_4 + (creditnote.iva_total/1000000) + (creditnote.ico_total/1000000)
				total_dn = 0
				imp_dn = 0
				for debitnote in debitnotes:
					total = debitnote.total_documento/1000000 + debitnote.cargo_interes/1000000
					total_dn = total_dn + total
					imp_dn = imp_dn + (debitnote.iva_total/1000000) + (debitnote.ico_total/1000000)
				total_ventas = 0
				total_ventas = total_facturas + total_cn_1 + total_cn_3 + total_cn_4 + total_dn
				ventas.append(total_ventas)
				semana = inicio_dia.strftime("%d") + " al " + fin_dia.strftime("%d")
				semanas.append(semana)
				facturas_comp = Factura_de_compra.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True).order_by('fecha_emision')
				total_compras = 0
				for factura_c in facturas_comp:
					compra = factura_c.total_documento/1000000
					total_compras = total_compras + compra
				gastos = Gastos_registro.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas).order_by('fecha_emision')
				total_gastos = 0
				for gasto in gastos:
					gasto = gasto.valor_gasto/1000000
					total_gastos = total_gastos + gasto
				total_ganancias = 0
				total_ganancias = total_facturas + total_cn_1 + total_cn_3 + total_cn_4 + total_dn - total_impuestos - imp_cn_1 - imp_cn_3 - imp_cn_4 - imp_dn - total_compras - total_gastos
				ganancias.append(total_ganancias)
				inicio_dia = inicio_dia + semana_a_semana
				fin_dia = inicio_dia + semana_a_semana
			x = np.array(semanas)
			y = np.array(ventas)
			x_2 = np.array(semanas)
			y_2 = np.array(ganancias)
			f = plt.figure()
			ejes = f.add_axes([0.15, 0.15, 0.75, 0.75])
			if reporte.metrica_crecimiento == 'V':
				ejes.plot(x,y,'g')
			elif reporte.metrica_crecimiento == 'G': 
				ejes.plot(x,y,'g',x_2,y_2,'r')
				ejes.legend(['Ventas','Ganancias'])
			ejes.set_xlabel("Semana")
			ejes.set_ylabel("Millones (COP)")
			ejes.set_title("Reporte " + reporte.fecha_inicio.strftime("%d %b") + " al " + reporte.fecha_fin.strftime("%d %b %Y"))
			buf = io.BytesIO()
			canvas =FigureCanvasAgg(f)
			canvas.print_png(buf)
			response = HttpResponse(buf.getvalue(), content_type='image/png')
			f.clear()
			response['Content-Length'] = str(len(response.content))
			return response

		elif periodo > mes and periodo <= año:
			mes_a_mes = timedelta(days=30)
			inicio_dia = inicio
			fin_dia = inicio_dia + mes_a_mes
			ganancias = []
			ventas = []
			meses = []
			while inicio_dia <= fin:
				facturas = Factura_de_venta.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True, anulada=False).order_by('fecha_emision')
				total_facturas = 0
				total_impuestos = 0
				for factura in facturas:
					venta = factura.total_documento/1000000
					total_facturas = total_facturas + venta
					total_impuestos = total_impuestos + (factura.iva_total/1000000) + (factura.ico_total/1000000)
				creditnotes_concep_1 = Nota_credito.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True, concepto_nota_credito='1').order_by('fecha_emision')
				creditnotes_concep_3 = Nota_credito.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True, concepto_nota_credito='3').order_by('fecha_emision')
				creditnotes_concep_4 = Nota_credito.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True, concepto_nota_credito='4').order_by('fecha_emision')
				debitnotes = Nota_debito.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True).order_by('fecha_emision')
				total_cn_1 = 0
				imp_cn_1 = 0
				for creditnote in creditnotes_concep_1:
					total = creditnote.total_documento/1000000
					total_cn_1 = total_cn_1 + total
					imp_cn_1 = imp_cn_1 + (creditnote.iva_total/1000000) + (creditnote.ico_total/1000000)
				total_cn_3 = 0
				imp_cn_3 = 0
				for creditnote in creditnotes_concep_3:
					total = creditnote.total_documento/1000000 - creditnote.descuento_rebaja/1000000
					total_cn_3 = total_cn_3 + total
					imp_cn_3 = imp_cn_3 + (creditnote.iva_total/1000000) + (creditnote.ico_total/1000000)
				total_cn_4 = 0
				imp_cn_4 = 0
				for creditnote in creditnotes_concep_4:
					total = creditnote.total_documento/1000000 - creditnote.descuento_rebaja/1000000
					total_cn_4 = total_cn_4 + total
					imp_cn_4 = imp_cn_4 + (creditnote.iva_total/1000000) + (creditnote.ico_total/1000000)
				total_dn = 0
				imp_dn = 0
				for debitnote in debitnotes:
					total = debitnote.total_documento/1000000 + debitnote.cargo_interes/1000000
					total_dn = total_dn + total
					imp_dn = imp_dn + (debitnote.iva_total/1000000) + (debitnote.ico_total/1000000)
				total_ventas = 0
				total_ventas = total_facturas + total_cn_1 + total_cn_3 + total_cn_4 + total_dn
				ventas.append(total_ventas)
				mes = inicio_dia.strftime("%b")
				meses.append(mes)
				facturas_comp = Factura_de_compra.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True).order_by('fecha_emision')
				total_compras = 0
				for factura_c in facturas_comp:
					compra = factura_c.total_documento/1000000
					total_compras = total_compras + compra
				gastos = Gastos_registro.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas).order_by('fecha_emision')
				total_gastos = 0
				for gasto in gastos:
					gasto = gasto.valor_gasto/1000000
					total_gastos = total_gastos + gasto
				total_ganancias = 0
				total_ganancias = total_facturas + total_cn_1 + total_cn_3 + total_cn_4 + total_dn - total_impuestos - imp_cn_1 - imp_cn_3 - imp_cn_4 - imp_dn - total_compras - total_gastos
				ganancias.append(total_ganancias)
				inicio_dia = inicio_dia + mes_a_mes
				fin_dia = inicio_dia + mes_a_mes
			x = np.array(meses)
			y = np.array(ventas)
			x_2 = np.array(meses)
			y_2 = np.array(ganancias)
			f = plt.figure()
			ejes = f.add_axes([0.15, 0.15, 0.75, 0.75])
			if reporte.metrica_crecimiento == 'V':
				ejes.plot(x,y,'g')
			elif reporte.metrica_crecimiento == 'G': 
				ejes.plot(x,y,'g',x_2,y_2,'r')
				ejes.legend(['Ventas','Ganancias'])
			ejes.set_xlabel("Mes")
			ejes.set_ylabel("Millones (COP)")
			ejes.set_title("Reporte " + reporte.fecha_inicio.strftime("%d %b %Y") + " al " + reporte.fecha_fin.strftime("%d %b %Y"))
			buf = io.BytesIO()
			canvas =FigureCanvasAgg(f)
			canvas.print_png(buf)
			response = HttpResponse(buf.getvalue(), content_type='image/png')
			f.clear()
			response['Content-Length'] = str(len(response.content))
			return response

		elif periodo > año:
			año_a_año = timedelta(days=365)
			inicio_dia = inicio
			fin_dia = inicio_dia + año_a_año
			ganancias = []
			ventas = []
			años = []
			while inicio_dia <= fin:
				facturas = Factura_de_venta.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True, anulada=False).order_by('fecha_emision')
				total_facturas = 0
				total_impuestos = 0
				for factura in facturas:
					venta = factura.total_documento/1000000
					total_facturas = total_facturas + venta
					total_impuestos = total_impuestos + (factura.iva_total/1000000) + (factura.ico_total/1000000)
				creditnotes_concep_1 = Nota_credito.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True, concepto_nota_credito='1').order_by('fecha_emision')
				creditnotes_concep_3 = Nota_credito.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True, concepto_nota_credito='3').order_by('fecha_emision')
				creditnotes_concep_4 = Nota_credito.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True, concepto_nota_credito='4').order_by('fecha_emision')
				debitnotes = Nota_debito.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True).order_by('fecha_emision')
				total_cn_1 = 0
				imp_cn_1 = 0
				for creditnote in creditnotes_concep_1:
					total = creditnote.total_documento/1000000
					total_cn_1 = total_cn_1 + total
					imp_cn_1 = imp_cn_1 + (creditnote.iva_total/1000000) + (creditnote.ico_total/1000000)
				total_cn_3 = 0
				imp_cn_3 = 0
				for creditnote in creditnotes_concep_3:
					total = creditnote.total_documento/1000000 - creditnote.descuento_rebaja/1000000
					total_cn_3 = total_cn_3 + total
					imp_cn_3 = imp_cn_3 + (creditnote.iva_total/1000000) + (creditnote.ico_total/1000000)
				total_cn_4 = 0
				imp_cn_4 = 0
				for creditnote in creditnotes_concep_4:
					total = creditnote.total_documento/1000000 - creditnote.descuento_rebaja/1000000
					total_cn_4 = total_cn_4 + total
					imp_cn_4 = imp_cn_4 + (creditnote.iva_total/1000000) + (creditnote.ico_total/1000000)
				total_dn = 0
				imp_dn = 0
				for debitnote in debitnotes:
					total = debitnote.total_documento/1000000 + debitnote.cargo_interes/1000000
					total_dn = total_dn + total
					imp_dn = imp_dn + (debitnote.iva_total/1000000) + (debitnote.ico_total/1000000)
				total_ventas = 0
				total_ventas = total_facturas + total_cn_1 + total_cn_3 + total_cn_4 + total_dn
				ventas.append(total_ventas)
				mes = inicio_dia.strftime("%Y")
				años.append(mes)
				facturas_comp = Factura_de_compra.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True).order_by('fecha_emision')
				total_compras = 0
				for factura_c in facturas_comp:
					compra = factura_c.total_documento/1000000
					total_compras = total_compras + compra
				gastos = Gastos_registro.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas).order_by('fecha_emision')
				total_gastos = 0
				for gasto in gastos:
					gasto = gasto.valor_gasto/1000000
					total_gastos = total_gastos + gasto
				total_ganancias = 0
				total_ganancias = total_facturas + total_cn_1 + total_cn_3 + total_cn_4 + total_dn - total_impuestos - imp_cn_1 - imp_cn_3 - imp_cn_4 - imp_dn - total_compras - total_gastos
				ganancias.append(total_ganancias)
				inicio_dia = inicio_dia + año_a_año
				fin_dia = inicio_dia + año_a_año
			x = np.array(años)
			y = np.array(ventas)
			x_2 = np.array(años)
			y_2 = np.array(ganancias)
			f = plt.figure()
			ejes = f.add_axes([0.15, 0.15, 0.75, 0.75])
			if reporte.metrica_crecimiento == 'V':
				ejes.plot(x,y,'g')
			elif reporte.metrica_crecimiento == 'G': 
				ejes.plot(x,y,'g',x_2,y_2,'r')
				ejes.legend(['Ventas','Ganancias'])
			ejes.set_xlabel("Año")
			ejes.set_ylabel("Millones (COP)")
			ejes.set_title("Reporte " + reporte.fecha_inicio.strftime("%d %b %Y") + " al " + reporte.fecha_fin.strftime("%d %b %Y"))
			buf = io.BytesIO()
			canvas =FigureCanvasAgg(f)
			canvas.print_png(buf)
			response = HttpResponse(buf.getvalue(), content_type='image/png')
			f.clear()
			response['Content-Length'] = str(len(response.content))
			return response

def grafica_detalle(request):
	locale.setlocale(locale.LC_ALL,'')
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	reporte = Crecimiento.objects.filter(org_creadora=orgactivas, guardada=True, mostrar=True)
	if reporte:
		reporte = Crecimiento.objects.get(org_creadora=orgactivas, guardada=True, mostrar=True)
		if reporte.fecha_fin == None or reporte.fecha_fin == reporte.fecha_inicio:
			dia = reporte.fecha_inicio.day
			mes = reporte.fecha_inicio.month
			año = reporte.fecha_inicio.year
			desface_tiempo = timedelta(hours=5)
			inicio = datetime(año, mes, dia, 0, 0, 0, tzinfo=pytz.UTC)
			inicio = inicio + desface_tiempo
			fin = datetime(año, mes, dia, 23, 59, 59, tzinfo=pytz.UTC)
			fin = fin + desface_tiempo
			hora_a_hora = timedelta(hours=5)
			inicio_hora = inicio
			fin_hora = inicio_hora + hora_a_hora
			ganancias = []
			ventas = []
			horas = []
			while inicio_hora <= fin:
				facturas = Factura_de_venta.objects.filter(fecha_emision__range=(inicio_hora, fin_hora), org_creadora=orgactivas, generado=True, anulada=False).order_by('fecha_emision')
				total_facturas = 0
				total_impuestos = 0
				for factura in facturas:
					venta = factura.total_documento/1000000
					total_facturas = total_facturas + venta
					total_impuestos = total_impuestos + (factura.iva_total/1000000) + (factura.ico_total/1000000)
				creditnotes_concep_1 = Nota_credito.objects.filter(fecha_emision__range=(inicio_hora, fin_hora), org_creadora=orgactivas, generado=True, concepto_nota_credito='1').order_by('fecha_emision')
				creditnotes_concep_3 = Nota_credito.objects.filter(fecha_emision__range=(inicio_hora, fin_hora), org_creadora=orgactivas, generado=True, concepto_nota_credito='3').order_by('fecha_emision')
				creditnotes_concep_4 = Nota_credito.objects.filter(fecha_emision__range=(inicio_hora, fin_hora), org_creadora=orgactivas, generado=True, concepto_nota_credito='4').order_by('fecha_emision')
				debitnotes = Nota_debito.objects.filter(fecha_emision__range=(inicio_hora, fin_hora), org_creadora=orgactivas, generado=True).order_by('fecha_emision')
				total_cn_1 = 0
				imp_cn_1 = 0
				for creditnote in creditnotes_concep_1:
					total = creditnote.total_documento/1000000
					total_cn_1 = total_cn_1 + total
					imp_cn_1 = imp_cn_1 + (creditnote.iva_total/1000000) + (creditnote.ico_total/1000000)
				total_cn_3 = 0
				imp_cn_3 = 0
				for creditnote in creditnotes_concep_3:
					total = creditnote.total_documento/1000000 - creditnote.descuento_rebaja/1000000
					total_cn_3 = total_cn_3 + total
					imp_cn_3 = imp_cn_3 + (creditnote.iva_total/1000000) + (creditnote.ico_total/1000000)
				total_cn_4 = 0
				imp_cn_4 = 0
				for creditnote in creditnotes_concep_4:
					total = creditnote.total_documento/1000000 - creditnote.descuento_rebaja/1000000
					total_cn_4 = total_cn_4 + total
					imp_cn_4 = imp_cn_4 + (creditnote.iva_total/1000000) + (creditnote.ico_total/1000000)
				total_dn = 0
				imp_dn = 0
				for debitnote in debitnotes:
					total = debitnote.total_documento/1000000 + debitnote.cargo_interes/1000000
					total_dn = total_dn + total
					imp_dn = imp_dn + (debitnote.iva_total/1000000) + (debitnote.ico_total/1000000)
				total_ventas = 0
				total_ventas = total_facturas + total_cn_1 + total_cn_3 + total_cn_4 + total_dn
				ventas.append(total_ventas)
				hora = inicio_hora
				hora = hora.strftime("%I:%M %p")
				horas.append(hora)
				facturas_comp = Factura_de_compra.objects.filter(fecha_emision__range=(inicio_hora, fin_hora), org_creadora=orgactivas, generado=True).order_by('fecha_emision')
				total_compras = 0
				for factura_c in facturas_comp:
					compra = factura_c.total_documento/1000000
					total_compras = total_compras + compra
				gastos = Gastos_registro.objects.filter(fecha_emision__range=(inicio_hora, fin_hora), org_creadora=orgactivas).order_by('fecha_emision')
				total_gastos = 0
				for gasto in gastos:
					gasto = gasto.valor_gasto/1000000
					total_gastos = total_gastos + gasto
				total_ganancias = 0
				total_ganancias = total_facturas + total_cn_1 + total_cn_3 + total_cn_4 + total_dn - total_impuestos - imp_cn_1 - imp_cn_3 - imp_cn_4 - imp_dn - total_compras - total_gastos
				ganancias.append(total_ganancias)
				inicio_hora = inicio_hora + hora_a_hora
				fin_hora = inicio_hora + hora_a_hora
			x = np.array(horas)
			y = np.array(ventas)
			x_2 = np.array(horas)
			y_2 = np.array(ganancias)
			f = plt.figure()
			ejes = f.add_axes([0.15, 0.15, 0.75, 0.75])
			if reporte.metrica_crecimiento == 'V':
				ejes.plot(x,y,'g')
			elif reporte.metrica_crecimiento == 'G': 
				ejes.plot(x,y,'g',x_2,y_2,'r')
				ejes.legend(['Ventas','Ganancias'])
			ejes.set_xlabel("Hora")
			ejes.set_ylabel("Millones (COP)")
			ejes.set_title("Reporte " + reporte.fecha_inicio.strftime("%A %d %b %Y"))
			buf = io.BytesIO()
			canvas =FigureCanvasAgg(f)
			canvas.print_png(buf)
			response = HttpResponse(buf.getvalue(), content_type='image/png')
			f.clear()
			response['Content-Length'] = str(len(response.content))
			return response
		else:
			dia_i = reporte.fecha_inicio.day
			mes_i = reporte.fecha_inicio.month
			año_i = reporte.fecha_inicio.year
			dia_f = reporte.fecha_fin.day
			mes_f = reporte.fecha_fin.month
			año_f = reporte.fecha_fin.year
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
				ventas = []
				dias = []
				while inicio_dia <= fin:
					facturas = Factura_de_venta.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True, anulada=False).order_by('fecha_emision')
					total_facturas = 0
					total_impuestos = 0
					for factura in facturas:
						venta = factura.total_documento/1000000
						total_facturas = total_facturas + venta
						total_impuestos = total_impuestos + (factura.iva_total/1000000) + (factura.ico_total/1000000)
					creditnotes_concep_1 = Nota_credito.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True, concepto_nota_credito='1').order_by('fecha_emision')
					creditnotes_concep_3 = Nota_credito.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True, concepto_nota_credito='3').order_by('fecha_emision')
					creditnotes_concep_4 = Nota_credito.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True, concepto_nota_credito='4').order_by('fecha_emision')
					debitnotes = Nota_debito.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True).order_by('fecha_emision')
					total_cn_1 = 0
					imp_cn_1 = 0
					for creditnote in creditnotes_concep_1:
						total = creditnote.total_documento/1000000
						total_cn_1 = total_cn_1 + total
						imp_cn_1 = imp_cn_1 + (creditnote.iva_total/1000000) + (creditnote.ico_total/1000000)
					total_cn_3 = 0
					imp_cn_3 = 0
					for creditnote in creditnotes_concep_3:
						total = creditnote.total_documento/1000000 - creditnote.descuento_rebaja/1000000
						total_cn_3 = total_cn_3 + total
						imp_cn_3 = imp_cn_3 + (creditnote.iva_total/1000000) + (creditnote.ico_total/1000000)
					total_cn_4 = 0
					imp_cn_4 = 0
					for creditnote in creditnotes_concep_4:
						total = creditnote.total_documento/1000000 - creditnote.descuento_rebaja/1000000
						total_cn_4 = total_cn_4 + total
						imp_cn_4 = imp_cn_4 + (creditnote.iva_total/1000000) + (creditnote.ico_total/1000000)
					total_dn = 0
					imp_dn = 0
					for debitnote in debitnotes:
						total = debitnote.total_documento/1000000 + debitnote.cargo_interes/1000000
						total_dn = total_dn + total
						imp_dn = imp_dn + (debitnote.iva_total/1000000) + (debitnote.ico_total/1000000)
					total_ventas = 0
					total_ventas = total_facturas + total_cn_1 + total_cn_3 + total_cn_4 + total_dn
					ventas.append(total_ventas)
					dia = inicio_dia
					dia = dia.strftime("%a %d")
					dias.append(dia)
					facturas_comp = Factura_de_compra.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True).order_by('fecha_emision')
					total_compras = 0
					for factura_c in facturas_comp:
						compra = factura_c.total_documento/1000000
						total_compras = total_compras + compra
					gastos = Gastos_registro.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas).order_by('fecha_emision')
					total_gastos = 0
					for gasto in gastos:
						gasto = gasto.valor_gasto/1000000
						total_gastos = total_gastos + gasto
					total_ganancias = 0
					total_ganancias = total_facturas + total_cn_1 + total_cn_3 + total_cn_4 + total_dn - total_impuestos - imp_cn_1 - imp_cn_3 - imp_cn_4 - imp_dn - total_compras - total_gastos
					ganancias.append(total_ganancias)
					inicio_dia = inicio_dia + dia_a_dia
					fin_dia = inicio_dia + dia_a_dia
				x = np.array(dias)
				y = np.array(ventas)
				x_2 = np.array(dias)
				y_2 = np.array(ganancias)
				f = plt.figure()
				ejes = f.add_axes([0.15, 0.15, 0.75, 0.75])
				if reporte.metrica_crecimiento == 'V':
					ejes.plot(x,y,'g')
				elif reporte.metrica_crecimiento == 'G': 
					ejes.plot(x,y,'g',x_2,y_2,'r')
					ejes.legend(['Ventas','Ganancias'])
				ejes.set_xlabel("Día")
				ejes.set_ylabel("Millones (COP)")
				ejes.set_title("Reporte " + reporte.fecha_inicio.strftime("%d %b") + " al " + reporte.fecha_fin.strftime("%d %b %Y"))
				buf = io.BytesIO()
				canvas =FigureCanvasAgg(f)
				canvas.print_png(buf)
				response = HttpResponse(buf.getvalue(), content_type='image/png')
				f.clear()
				response['Content-Length'] = str(len(response.content))
				return response

			elif periodo > semana and periodo <= mes:
				semana_a_semana = timedelta(days=7)
				inicio_dia = inicio
				fin_dia = inicio_dia + semana_a_semana
				ganancias = []
				ventas = []
				semanas = []
				while inicio_dia <= fin:
					facturas = Factura_de_venta.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True, anulada=False).order_by('fecha_emision')
					total_facturas = 0
					total_impuestos = 0
					for factura in facturas:
						venta = factura.total_documento/1000000
						total_facturas = total_facturas + venta
						total_impuestos = total_impuestos + (factura.iva_total/1000000) + (factura.ico_total/1000000)
					creditnotes_concep_1 = Nota_credito.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True, concepto_nota_credito='1').order_by('fecha_emision')
					creditnotes_concep_3 = Nota_credito.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True, concepto_nota_credito='3').order_by('fecha_emision')
					creditnotes_concep_4 = Nota_credito.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True, concepto_nota_credito='4').order_by('fecha_emision')
					debitnotes = Nota_debito.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True).order_by('fecha_emision')
					total_cn_1 = 0
					imp_cn_1 = 0
					for creditnote in creditnotes_concep_1:
						total = creditnote.total_documento/1000000
						total_cn_1 = total_cn_1 + total
						imp_cn_1 = imp_cn_1 + (creditnote.iva_total/1000000) + (creditnote.ico_total/1000000)
					total_cn_3 = 0
					imp_cn_3 = 0
					for creditnote in creditnotes_concep_3:
						total = creditnote.total_documento/1000000 - creditnote.descuento_rebaja/1000000
						total_cn_3 = total_cn_3 + total
						imp_cn_3 = imp_cn_3 + (creditnote.iva_total/1000000) + (creditnote.ico_total/1000000)
					total_cn_4 = 0
					imp_cn_4 = 0
					for creditnote in creditnotes_concep_4:
						total = creditnote.total_documento/1000000 - creditnote.descuento_rebaja/1000000
						total_cn_4 = total_cn_4 + total
						imp_cn_4 = imp_cn_4 + (creditnote.iva_total/1000000) + (creditnote.ico_total/1000000)
					total_dn = 0
					imp_dn = 0
					for debitnote in debitnotes:
						total = debitnote.total_documento/1000000 + debitnote.cargo_interes/1000000
						total_dn = total_dn + total
						imp_dn = imp_dn + (debitnote.iva_total/1000000) + (debitnote.ico_total/1000000)
					total_ventas = 0
					total_ventas = total_facturas + total_cn_1 + total_cn_3 + total_cn_4 + total_dn
					ventas.append(total_ventas)
					semana = inicio_dia.strftime("%d") + " al " + fin_dia.strftime("%d")
					semanas.append(semana)
					facturas_comp = Factura_de_compra.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True).order_by('fecha_emision')
					total_compras = 0
					for factura_c in facturas_comp:
						compra = factura_c.total_documento/1000000
						total_compras = total_compras + compra
					gastos = Gastos_registro.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas).order_by('fecha_emision')
					total_gastos = 0
					for gasto in gastos:
						gasto = gasto.valor_gasto/1000000
						total_gastos = total_gastos + gasto
					total_ganancias = 0
					total_ganancias = total_facturas + total_cn_1 + total_cn_3 + total_cn_4 + total_dn - total_impuestos - imp_cn_1 - imp_cn_3 - imp_cn_4 - imp_dn - total_compras - total_gastos
					ganancias.append(total_ganancias)
					inicio_dia = inicio_dia + semana_a_semana
					fin_dia = inicio_dia + semana_a_semana
				x = np.array(semanas)
				y = np.array(ventas)
				x_2 = np.array(semanas)
				y_2 = np.array(ganancias)
				f = plt.figure()
				ejes = f.add_axes([0.15, 0.15, 0.75, 0.75])
				if reporte.metrica_crecimiento == 'V':
					ejes.plot(x,y,'g')
				elif reporte.metrica_crecimiento == 'G': 
					ejes.plot(x,y,'g',x_2,y_2,'r')
					ejes.legend(['Ventas','Ganancias'])
				ejes.set_xlabel("Semana")
				ejes.set_ylabel("Millones (COP)")
				ejes.set_title("Reporte " + reporte.fecha_inicio.strftime("%d %b") + " al " + reporte.fecha_fin.strftime("%d %b %Y"))
				buf = io.BytesIO()
				canvas =FigureCanvasAgg(f)
				canvas.print_png(buf)
				response = HttpResponse(buf.getvalue(), content_type='image/png')
				f.clear()
				response['Content-Length'] = str(len(response.content))
				return response

			elif periodo > mes and periodo <= año:
				mes_a_mes = timedelta(days=30)
				inicio_dia = inicio
				fin_dia = inicio_dia + mes_a_mes
				ganancias = []
				ventas = []
				meses = []
				while inicio_dia <= fin:
					facturas = Factura_de_venta.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True, anulada=False).order_by('fecha_emision')
					total_facturas = 0
					total_impuestos = 0
					for factura in facturas:
						venta = factura.total_documento/1000000
						total_facturas = total_facturas + venta
						total_impuestos = total_impuestos + (factura.iva_total/1000000) + (factura.ico_total/1000000)
					creditnotes_concep_1 = Nota_credito.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True, concepto_nota_credito='1').order_by('fecha_emision')
					creditnotes_concep_3 = Nota_credito.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True, concepto_nota_credito='3').order_by('fecha_emision')
					creditnotes_concep_4 = Nota_credito.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True, concepto_nota_credito='4').order_by('fecha_emision')
					debitnotes = Nota_debito.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True).order_by('fecha_emision')
					total_cn_1 = 0
					imp_cn_1 = 0
					for creditnote in creditnotes_concep_1:
						total = creditnote.total_documento/1000000
						total_cn_1 = total_cn_1 + total
						imp_cn_1 = imp_cn_1 + (creditnote.iva_total/1000000) + (creditnote.ico_total/1000000)
					total_cn_3 = 0
					imp_cn_3 = 0
					for creditnote in creditnotes_concep_3:
						total = creditnote.total_documento/1000000 - creditnote.descuento_rebaja/1000000
						total_cn_3 = total_cn_3 + total
						imp_cn_3 = imp_cn_3 + (creditnote.iva_total/1000000) + (creditnote.ico_total/1000000)
					total_cn_4 = 0
					imp_cn_4 = 0
					for creditnote in creditnotes_concep_4:
						total = creditnote.total_documento/1000000 - creditnote.descuento_rebaja/1000000
						total_cn_4 = total_cn_4 + total
						imp_cn_4 = imp_cn_4 + (creditnote.iva_total/1000000) + (creditnote.ico_total/1000000)
					total_dn = 0
					imp_dn = 0
					for debitnote in debitnotes:
						total = debitnote.total_documento/1000000 + debitnote.cargo_interes/1000000
						total_dn = total_dn + total
						imp_dn = imp_dn + (debitnote.iva_total/1000000) + (debitnote.ico_total/1000000)
					total_ventas = 0
					total_ventas = total_facturas + total_cn_1 + total_cn_3 + total_cn_4 + total_dn
					ventas.append(total_ventas)
					mes = inicio_dia.strftime("%b")
					meses.append(mes)
					facturas_comp = Factura_de_compra.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True).order_by('fecha_emision')
					total_compras = 0
					for factura_c in facturas_comp:
						compra = factura_c.total_documento/1000000
						total_compras = total_compras + compra
					gastos = Gastos_registro.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas).order_by('fecha_emision')
					total_gastos = 0
					for gasto in gastos:
						gasto = gasto.valor_gasto/1000000
						total_gastos = total_gastos + gasto
					total_ganancias = 0
					total_ganancias = total_facturas + total_cn_1 + total_cn_3 + total_cn_4 + total_dn - total_impuestos - imp_cn_1 - imp_cn_3 - imp_cn_4 - imp_dn - total_compras - total_gastos
					ganancias.append(total_ganancias)
					inicio_dia = inicio_dia + mes_a_mes
					fin_dia = inicio_dia + mes_a_mes
				x = np.array(meses)
				y = np.array(ventas)
				x_2 = np.array(meses)
				y_2 = np.array(ganancias)
				f = plt.figure()
				ejes = f.add_axes([0.15, 0.15, 0.75, 0.75])
				if reporte.metrica_crecimiento == 'V':
					ejes.plot(x,y,'g')
				elif reporte.metrica_crecimiento == 'G': 
					ejes.plot(x,y,'g',x_2,y_2,'r')
					ejes.legend(['Ventas','Ganancias'])
				ejes.set_xlabel("Mes")
				ejes.set_ylabel("Millones (COP)")
				ejes.set_title("Reporte " + reporte.fecha_inicio.strftime("%d %b %Y") + " al " + reporte.fecha_fin.strftime("%d %b %Y"))
				buf = io.BytesIO()
				canvas =FigureCanvasAgg(f)
				canvas.print_png(buf)
				response = HttpResponse(buf.getvalue(), content_type='image/png')
				f.clear()
				response['Content-Length'] = str(len(response.content))
				return response

			elif periodo > año:
				año_a_año = timedelta(days=365)
				inicio_dia = inicio
				fin_dia = inicio_dia + año_a_año
				ganancias = []
				ventas = []
				años = []
				while inicio_dia <= fin:
					facturas = Factura_de_venta.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True, anulada=False).order_by('fecha_emision')
					total_facturas = 0
					total_impuestos = 0
					for factura in facturas:
						venta = factura.total_documento/1000000
						total_facturas = total_facturas + venta
						total_impuestos = total_impuestos + (factura.iva_total/1000000) + (factura.ico_total/1000000)
					creditnotes_concep_1 = Nota_credito.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True, concepto_nota_credito='1').order_by('fecha_emision')
					creditnotes_concep_3 = Nota_credito.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True, concepto_nota_credito='3').order_by('fecha_emision')
					creditnotes_concep_4 = Nota_credito.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True, concepto_nota_credito='4').order_by('fecha_emision')
					debitnotes = Nota_debito.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True).order_by('fecha_emision')
					total_cn_1 = 0
					imp_cn_1 = 0
					for creditnote in creditnotes_concep_1:
						total = creditnote.total_documento/1000000
						total_cn_1 = total_cn_1 + total
						imp_cn_1 = imp_cn_1 + (creditnote.iva_total/1000000) + (creditnote.ico_total/1000000)
					total_cn_3 = 0
					imp_cn_3 = 0
					for creditnote in creditnotes_concep_3:
						total = creditnote.total_documento/1000000 - creditnote.descuento_rebaja/1000000
						total_cn_3 = total_cn_3 + total
						imp_cn_3 = imp_cn_3 + (creditnote.iva_total/1000000) + (creditnote.ico_total/1000000)
					total_cn_4 = 0
					imp_cn_4 = 0
					for creditnote in creditnotes_concep_4:
						total = creditnote.total_documento/1000000 - creditnote.descuento_rebaja/1000000
						total_cn_4 = total_cn_4 + total
						imp_cn_4 = imp_cn_4 + (creditnote.iva_total/1000000) + (creditnote.ico_total/1000000)
					total_dn = 0
					imp_dn = 0
					for debitnote in debitnotes:
						total = debitnote.total_documento/1000000 + debitnote.cargo_interes/1000000
						total_dn = total_dn + total
						imp_dn = imp_dn + (debitnote.iva_total/1000000) + (debitnote.ico_total/1000000)
					total_ventas = 0
					total_ventas = total_facturas + total_cn_1 + total_cn_3 + total_cn_4 + total_dn
					ventas.append(total_ventas)
					mes = inicio_dia.strftime("%Y")
					años.append(mes)
					facturas_comp = Factura_de_compra.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas, generado=True).order_by('fecha_emision')
					total_compras = 0
					for factura_c in facturas_comp:
						compra = factura_c.total_documento/1000000
						total_compras = total_compras + compra
					gastos = Gastos_registro.objects.filter(fecha_emision__range=(inicio_dia, fin_dia), org_creadora=orgactivas).order_by('fecha_emision')
					total_gastos = 0
					for gasto in gastos:
						gasto = gasto.valor_gasto/1000000
						total_gastos = total_gastos + gasto
					total_ganancias = 0
					total_ganancias = total_facturas + total_cn_1 + total_cn_3 + total_cn_4 + total_dn - total_impuestos - imp_cn_1 - imp_cn_3 - imp_cn_4 - imp_dn - total_compras - total_gastos
					ganancias.append(total_ganancias)
					inicio_dia = inicio_dia + año_a_año
					fin_dia = inicio_dia + año_a_año
				x = np.array(años)
				y = np.array(ventas)
				x_2 = np.array(años)
				y_2 = np.array(ganancias)
				f = plt.figure()
				ejes = f.add_axes([0.15, 0.15, 0.75, 0.75])
				if reporte.metrica_crecimiento == 'V':
					ejes.plot(x,y,'g')
				elif reporte.metrica_crecimiento == 'G': 
					ejes.plot(x,y,'g',x_2,y_2,'r')
					ejes.legend(['Ventas','Ganancias'])
				ejes.set_xlabel("Año")
				ejes.set_ylabel("Millones (COP)")
				ejes.set_title("Reporte " + reporte.fecha_inicio.strftime("%d %b %Y") + " al " + reporte.fecha_fin.strftime("%d %b %Y"))
				buf = io.BytesIO()
				canvas =FigureCanvasAgg(f)
				canvas.print_png(buf)
				response = HttpResponse(buf.getvalue(), content_type='image/png')
				f.clear()
				response['Content-Length'] = str(len(response.content))
				return response
	

def nuevo_reporte_ing(request):
	form = "valor"
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayreportes = Crecimiento.objects.filter(org_creadora=orgactivas, guardada=True).count()
	nohayfacturas = Factura_de_venta.objects.filter(org_creadora=orgactivas, generado=True).count()
	reporteborrador = Crecimiento.objects.filter(org_creadora=orgactivas, guardada=False).last()
	if request.method == "POST":
		if reporteborrador:
			form = CrecimientoForm(request.POST, instance=reporteborrador)
		else:
			form = CrecimientoForm(request.POST)
		if form.is_valid():
			reporte = form.save(commit=False)
			reporte.org_creadora = orgactivas
			reporte.calcular_reporte()
			reporte.save()
			return redirect('nuevo_reporte_fin', pk=reporte.pk)
	else:
		form = CrecimientoForm()
	reportes = Crecimiento.objects.filter(org_creadora=orgactivas, guardada=True).order_by('-fecha_creacion')
	reportes = reemplazardatos_reportes(reportes)
	return render(request, 'groway/nuevo_reporte.html', {'form':form, 'orgactivas':orgactivas, 'reportes':reportes, 'nohayfacturas':nohayfacturas, 'nohayreportes':nohayreportes})

def nuevo_reporte_fin(request, pk):
	form = "valor"
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayreportes = Crecimiento.objects.filter(org_creadora=orgactivas, guardada=True).count()
	nohayfacturas = Factura_de_venta.objects.filter(org_creadora=orgactivas, generado=True).count()
	reporte = get_object_or_404(Crecimiento, pk=pk)
	if request.method == "POST":
		form = CrecimientoForm(request.POST, instance=reporte)
		if form.is_valid():
			reporte = form.save(commit=False)
			reporte.fecha_creacion = timezone.now()
			reporte.org_creadora = orgactivas
			reporte.calcular_reporte()
			reporte.guardada = True
			reporte.save()
			return redirect('mostrar_reporte', pk=reporte.pk)
	else:
		form = CrecimientoForm(instance=reporte)
	reportes = Crecimiento.objects.filter(org_creadora=orgactivas, guardada=True).order_by('-fecha_creacion')
	reportes = reemplazardatos_reportes(reportes)
	return render(request, 'groway/nuevo_reporte.html', {'form':form, 'orgactivas':orgactivas, 'reportes':reportes, 'reporte':reporte, 'nohayfacturas':nohayfacturas, 'nohayreportes':nohayreportes})


def atras_reporte(request, pk):
	form = "valor"
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayreportes = Crecimiento.objects.filter(org_creadora=orgactivas, guardada=True).count()
	nohayfacturas = Factura_de_venta.objects.filter(org_creadora=orgactivas, generado=True).count()
	reporte = get_object_or_404(Crecimiento, pk=pk)
	if request.method == "POST":
		form = CrecimientoForm(request.POST, instance=reporte)
		if form.is_valid():
			reporte = form.save(commit=False)
			reporte.org_creadora = orgactivas
			reporte.calcular_reporte()
			reporte.save()
			return redirect('nuevo_reporte_fin', pk=reporte.pk)
	else:
		form = CrecimientoForm(instance=reporte)
	reportes = Crecimiento.objects.filter(org_creadora=orgactivas, guardada=True).order_by('-fecha_creacion')
	reportes = reemplazardatos_reportes(reportes)
	return render(request, 'groway/nuevo_reporte.html', {'form':form, 'orgactivas':orgactivas, 'reportes':reportes, 'nohayfacturas':nohayfacturas, 'nohayreportes':nohayreportes})


def editar_reporte(request, pk):
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayreportes = Crecimiento.objects.filter(org_creadora=orgactivas, guardada=True).count()
	nohayfacturas = Factura_de_venta.objects.filter(org_creadora=orgactivas, generado=True).count()
	reporte = get_object_or_404(Crecimiento, pk=pk)
	org_reporte = reporte.org_creadora
	fecha_reporte = reporte.fecha_creacion
	if request.method == "POST":
		form = CrecimientoForm(request.POST, instance=reporte)
		if form.is_valid():
			reporte = form.save(commit=False)
			reporte.fecha_creacion = fecha_reporte
			reporte.org_creadora = org_reporte
			reporte.calcular_reporte()
			reporte.guardada = True
			reporte.save()
			return redirect('mostrar_reporte', pk=reporte.pk)
	else:
		form = CrecimientoForm(instance=reporte)
	reportes = Crecimiento.objects.filter(org_creadora=orgactivas, guardada=True).order_by('-fecha_creacion')
	reportes = reemplazardatos_reportes(reportes)
	return render(request, 'groway/nuevo_reporte.html', {'form':form, 'orgactivas':orgactivas, 'reportes':reportes, 'nohayfacturas':nohayfacturas, 'nohayreportes':nohayreportes})

def eliminar_reporte(request, pk):
	reporte = get_object_or_404(Crecimiento, pk=pk)
	reporte.delete()
	return redirect('reportes_crecimiento')

def mostrar_reporte(request, pk):
	reporte = get_object_or_404(Crecimiento, pk=pk)
	if reporte.mostrar == False:
		reporte_activo = Crecimiento.objects.filter(mostrar=True)
		if reporte_activo:
			reporte_activo = reporte_activo.get(mostrar=True)
			reporte_activo.mostrar = False
			reporte_activo.save()
		reporte.mostrar = True
		reporte.save()
	return redirect('detalle_reporte', pk=pk)

def detalle_reporte(request, pk):
	lista ="valor"
	orgactivas = Organizacion.objects.filter(activa=True, administrador=request.user)
	if orgactivas:
		orgactivas = orgactivas.get(activa=True, administrador=request.user)
	else:
		orgactivas = None
	nohayreportes = Crecimiento.objects.filter(org_creadora=orgactivas, guardada=True).count()
	nohayfacturas = Factura_de_venta.objects.filter(org_creadora=orgactivas, generado=True).count()
	reporte = get_object_or_404(Crecimiento, pk=pk)
	reporte.mostrar = True
	reporte = reemplazardatos_reporte(reporte)
	if request.method == "POST":
		dic = request.POST
		busqueda = dic["buscar"]
		orden = dic["ordenar"]
		buscarxfecha = Crecimiento.objects.filter(fecha_inicio__contains=busqueda, org_creadora=orgactivas, guardada=True)
		buscarxnombre = Crecimiento.objects.filter(nombre__contains=busqueda, org_creadora=orgactivas, guardada=True)
		buscarxmetrica = Crecimiento.objects.filter(metrica_crecimiento__contains=busqueda, org_creadora=orgactivas, guardada=True)
		if buscarxfecha:
			lista = buscarxfecha.order_by(orden)
			lista = reemplazardatos_reportes(lista)
		elif buscarxnombre:
			lista = buscarxnombre.order_by(orden)
			lista = reemplazardatos_reportes(lista)
		elif buscarxmetrica:
			lista = buscarxmetrica.order_by(orden)
			lista = reemplazardatos_reportes(lista)
		else:
			lista = Crecimiento.objects.filter(org_creadora=orgactivas, guardada=True).order_by('-fecha_creacion')
			lista = reemplazardatos_reportes(lista)
	reportes = Crecimiento.objects.filter(org_creadora=orgactivas, guardada=True).order_by('-fecha_creacion')
	reportes = reemplazardatos_reportes(reportes)
	return render(request, 'groway/detalle_reporte.html', {'orgactivas':orgactivas, 'reporte':reporte, 'reportes':reportes, 'lista':lista, 'nohayreportes':nohayreportes, 'nohayfacturas':nohayfacturas})
