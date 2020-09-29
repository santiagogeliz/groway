# Listas - Dicts para los ChoiceFields

REGISTRO_CIVIL = '11'
TARJETA_IDENTIDAD = '12'
CEDULA_CIUDADANIA = '13'
TARJETA_EXTRANJERA = '21'
CEDULA_EXTRANJERIA = '22'
NIT = '31'
PASAPORTE = '41'
DOCUMENTO_EXTRANJERO = '42'
NO_OBLIGADO_RUT_PN = 'R-00-PN'
DOCUMENTOS_IDENTIDAD =[(REGISTRO_CIVIL,'Registro Civil'), (TARJETA_IDENTIDAD, 'Tarjeta de Identidad'),
(CEDULA_CIUDADANIA, 'Cédula de Ciudadanía'), (NIT, 'NIT'), (PASAPORTE, 'Pasaporte'),
(DOCUMENTO_EXTRANJERO, 'Documento de identificación extranjero'), (NO_OBLIGADO_RUT_PN, 'No obigado a registrarse en el RUT PN')]

PERSONA_JURIDICA = '1'
PERSONA_NATURAL = '2'
NATURALEZA = [(PERSONA_JURIDICA, 'Persona Juridica'), (PERSONA_NATURAL, 'Persona Natural')]

REGIMEN_COMUN = '2'
REGIMEN_SIMPLE = '0'
REGIMEN_TRIBUTARIO = [(REGIMEN_COMUN, "Régimen Común"), (REGIMEN_SIMPLE, "Régimen Simple")]

SI_RESPONSABLE = 'SI'
NO_RESPONSABLE = 'NO'
RESPONSABLE_IVA = [(SI_RESPONSABLE, "Si"), (NO_RESPONSABLE, "No")]

CERO_0 = "1"
BIENES_2_5_961000 = "2"
BIENES_2_5_0 = "3"
BIENES_3_5_961000 = "4"
BIENES_3_5_0 = "5"
BIENES_1_0 = "6"
BIENES_0_1_0 = "7"
COMISIONES_10_0 = "8"
COMISIONES_11_0 = "9"
CONSULTORIAS_3_5_0 = "10"
CONSULTORIAS_6_0 = "11"
CONSULTORIAS_10_0 = "12"
HONORARIOS_10_0 = "13"
HONORARIOS_11_0 = "14"
SERVICIOS_1_142000 = "15"
SERVICIOS_1_0 = "16"
SERVICIOS_2_142000 = "17"
SERVICIOS_2_0 = "18"
SERVICIOS_3_5_142000 = "19"
SERVICIOS_3_5_961000 = "20"
SERVICIOS_3_5_0 = "21"
SERVICIOS_4_142000 = "22"
SERVICIOS_4_0 = "23"
SERVICIOS_6_142000 = "24"
SERVICIOS_6_0 = "25"
SERVICIOSAIU_1_142000 = "26"
SERVICIOSAIU_1_0 = "27"
SERVICIOSAIU_2_142000 = "28"
SERVICIOSAIU_2_0 = "29"
ARRENDAMIENTOS_4_0 = "30"
ARRENDAMIENTOS_3_5_961000 = "31"
ARRENDAMIENTOS_3_5_0 = "32"
RENDIMIENTOSFROS_7_0 = "33"
RENDIMIENTOSFROS_4_0 = "34"
PRODAGRICOLAS_1_5_3276000 = "35"
PRODAGRICOLAS_1_5_0 = "36"
FOMENTOGANADERO_0_75_0 = "37"
SERVICIOSEXTERIOR_15_0 = "38"
SERVICIOSEXTERIOR_20_0 = "39"
DIVIDENDOPARTICIPACIONES_5_0 = "40"
DIVIDENDOPARTICIPACIONES_15_0 = "41"
CONSTRURBANIZACION_2_961000 = "42"
CONSTRURBANIZACION_2_0 = "43"
COMPRACAFE_0_5_0 = "44"
COMPRACAFE_0_5_5697000 = "45"
CONSULADMINDELEGADA_10_0 = "46"
CONSULADMINDELEGADA_11_0 = "47"
SERVICIOSIMPRESION_2_5_0 = "48"
TARIFA_RETERENTA = [(CERO_0, "0%"), (BIENES_2_5_961000, "2.5% Bienes - A partir de 961,000"),
(BIENES_2_5_0, "2.5% Bienes - A partir de 0"), (BIENES_3_5_961000, "3.5% Bienes - A partir de 961,000"),
(BIENES_3_5_0, "3.5% Bienes - A partir de 0"), (BIENES_1_0, "1% Bienes - A partir de 0"),
(BIENES_0_1_0, "0.1% Bienes - A partir de 0"), (COMISIONES_10_0, "10% Comisiones - A partir de 0"),
(COMISIONES_11_0, "11% Comisiones - A partir de 0"),(CONSULTORIAS_3_5_0, "3.5% Consultorías - A partir de 0"),
(CONSULTORIAS_6_0, "6% Consultorías - A partir de 0"),(CONSULTORIAS_10_0, "10% Consultorías - A partir de 0"),
(HONORARIOS_10_0, "10% Honorarios - A partir de 0"),(HONORARIOS_11_0, "11% Honorarios - A partir de 0"),
(SERVICIOS_1_142000, "1% Servicios - A partir de 142,000"),(SERVICIOS_1_0, "1% Servicios - A partir de 0"), (SERVICIOS_2_142000, "2% Servicios - A partir de 142,000"),
(SERVICIOS_2_0, "2% Servicios - A partir de 0"), (SERVICIOS_3_5_142000, "3.5% Servicios - A partir de 142,000"),
(SERVICIOS_3_5_961000, "3.5% Servicios - A partir de 961,000"), (SERVICIOS_3_5_0, "3.5% Servicios - A partir de 0"),
(SERVICIOS_4_142000, "4% Servicios - A partir de 142,000"), (SERVICIOS_4_0, "4% Servicios - A partir de 0"),
(SERVICIOS_6_142000, "6% Servicios - A partir de 142,000"), (SERVICIOS_6_0, "6% Servicios - A partir de 0"),
(SERVICIOSAIU_1_142000, "1% Servicios AIU - A partir de 142,000"), (SERVICIOSAIU_1_0, "1% Servicios AIU - A partir de 0"),
(SERVICIOSAIU_2_142000, "2% Servicios AIU - A partir de 142,000"), (SERVICIOSAIU_2_0, "2% Servicios AIU - A partir de 0"),
(ARRENDAMIENTOS_4_0, "4% Harrendamientos - A partir de 0"), (ARRENDAMIENTOS_3_5_961000, "3.5% Harrendamientos - A partir de 961,000"),
(ARRENDAMIENTOS_3_5_0, "3.5% Harrendamientos - A partir de 0"), (RENDIMIENTOSFROS_7_0, "7% Rendimientos Fros. - A partir de 0"),
(RENDIMIENTOSFROS_4_0, "4% Rendimientos Fros. - A partir de 0"), (PRODAGRICOLAS_1_5_3276000, "1.5% Prod. Agrícolas - A partir de 3,276,000"),
(PRODAGRICOLAS_1_5_0, "1.5% Prod. Agrícolas - A partir de 0"), (FOMENTOGANADERO_0_75_0, "0.75% Cuota Fomento Ganadero - A partir de 0"),
(SERVICIOSEXTERIOR_15_0, "15% Servicios Exterior - A partir de 0"), (SERVICIOSEXTERIOR_20_0, "20% Servicios Exterior - A partir de 0"),
(DIVIDENDOPARTICIPACIONES_5_0, "5% Dividendos y Participaciones - A partir de 0"), (DIVIDENDOPARTICIPACIONES_15_0, "15% Dividendos y Participaciones - A partir de 0"),
(CONSTRURBANIZACION_2_961000, "2% Construcción y Urbanización - A partir de 961,000"), (CONSTRURBANIZACION_2_0, "2% Construcción y Urbanización - A partir de 0"),
(COMPRACAFE_0_5_0, "0.5% Compra de Café - A partir de 0"), (COMPRACAFE_0_5_5697000, "0.5% Compra de Café - A partir de 5,697,000"),
(CONSULADMINDELEGADA_10_0, "10% Consultorías Adm. Delegada - A partir de 0"), (CONSULADMINDELEGADA_11_0, "11% Consultorías Adm. Delegada - A partir de 0"),
(SERVICIOSIMPRESION_2_5_0, "2.5% Servicios de Impresión - A partir de 0")]

AUTORETERENTA_UNO = "1"
AUTORETERENTA_DOS = "2"
AUTORETERENTA_TRES = "3"
TARIFA_AUTORETERENTA = [(AUTORETERENTA_UNO, "Tarifa 0.4%"), (AUTORETERENTA_DOS, "Tarifa 0.8%"), (AUTORETERENTA_TRES, "Tarifa 1.6%")]

IVA_UNO = '1'
IVA_DOS = '2'
EXCLUIDO = '3'
EXENTO = '4'
TARIFA_IVA = [(IVA_UNO, "19.00"), (IVA_DOS, "5.00"), (EXCLUIDO, "Excluido"), (EXENTO, "Exento")]

ICO_UNO = '1'
ICO_DOS = '2'
ICO_TRES = '3'
EXENTO_ICO = '4'
TARIFA_ICO = [(ICO_UNO, "16.00"), (ICO_DOS, "8.00"), (ICO_TRES, "4.00"), (EXENTO_ICO, "Exento")]

CLIENTE = 'CL'
PROVEEDOR = 'PD'
OTRO = 'OT'
RELACIONES = [(CLIENTE, 'Cliente'), (PROVEEDOR, 'Proveedor'), (OTRO, 'Otro')]

CORRIENTE = 'CCO'
AHORRO = 'AHO'
TIPO_CUENTA = [(CORRIENTE, 'Cuenta Corriente'), (AHORRO, 'Cuenta Ahorros')]

SERVICIO = 'SV'
INVENTARIABLE = 'IN'
NO_INVENTARIABLE = 'NI'
TIPO_ITEM = [(SERVICIO, 'Servicio'), (INVENTARIABLE, 'Inventariable'), (NO_INVENTARIABLE, 'No Inventariable')]

ITEM_VENTA = 'IV'
INSUMO = 'IM'
DESTINO_ITEM = [(ITEM_VENTA, "Item de Venta"), (INSUMO, "Insumo")]

UNIDAD = 'UNID'
METROS = 'M'
CENTIMETROS = 'CM'
KILOGRAMO = "KG"
GRAMOS = 'G'
LITROS = 'L'
MILILITRO = 'ML'
UNIDADES_MEDIDA = [(UNIDAD, "UNID"), (METROS, "M"), (CENTIMETROS, "CM"), (GRAMOS, "G"), (KILOGRAMO, "KG"), (LITROS, "L"), (MILILITRO, "ML")]

FACTURA_DE_VENTA = "FVE"
FACTURA_DE_EXPORTACION = "FEX"
FACTURA_DE_CONTINGENCIA = "FCG"
FACTURA_DE_COMPRA = "FCO"
COTIZACION = "CZN"
REMISION = "RSN"
NOTA_CREDITO = "NCT"
NOTA_DEBITO = "NDT"
TIPO_DE_DOCUMENTO = [(FACTURA_DE_VENTA, 'Factura de Venta'), (FACTURA_DE_COMPRA, 'Factura de Compra'),
(COTIZACION, 'Cotización'), (REMISION, 'Remisión'), (NOTA_CREDITO, 'Nota Crédito'),(NOTA_DEBITO, 'Nota Débito')]

COLOMBIA_PESO = 'COP'
USA_DOLLAR = 'USD'
EUROPE_EURO = 'EUR'
MONEDAS = [(COLOMBIA_PESO, 'Colombia, Pesos'), (USA_DOLLAR, 'United States of America, Dollar'), (EUROPE_EURO, 'Euro Member Country')]

ALEMANIA = 'DE'
ARGENTINA = 'AR'
ARMENIA = 'AM'
ARUBA = 'AW'
AUSTRALIA = 'AU'
BAHAMAS = 'BS'
BOLIVIA = 'BO'
BRASIL = 'BR'
CANADA = 'CA'
CHILE = 'CL'
CHINA = 'CN'
COLOMBIA = 'CO'
COSTA_RICA = 'CR'
CUBA = 'CU'
ECUADOR = 'EC'
EGIPTO = 'EG'
EL_SALVADOR = 'SV'
ESPAÑA = 'ES'
ESTADOS_UNIDOS = 'US'
FILIPINAS = 'PH'
FRANCIA = 'FR'
GUATEMALA = 'GT'
HAITI = 'HT'
HONDURAS = 'HN'
ITALIA = 'IT'
JAPON = 'JP'
NICARAGUA = 'NI'
PANAMA = 'PA'
PARAGUAY = 'PY'
PERU = 'PE'
PORTUGAL = 'PT'
PUERTO_RICO = 'PR'
REINO_UNIDO = 'GB'
RUSIA = 'RU'
URUGUAY = 'UY'
VENEZUELA = 'VE'
PAISES = [(ALEMANIA, 'Alemania'), (ARGENTINA, 'Argentina'), (ARMENIA, 'Armenia'), (ARUBA, 'Aruba'), (AUSTRALIA, 'Australia'), (BAHAMAS, 'Bahamas'), (BOLIVIA, 'Bolivia'),
(BRASIL, 'Brasil'), (CANADA, 'Canadá'), (CHILE, 'Chile'), (CHINA, 'China'), (COLOMBIA, 'Colombia'), (COSTA_RICA, 'Costa Rica'), (CUBA, 'Cuba'), (ECUADOR, 'Ecuador'),
(EGIPTO, 'Egipto'), (EL_SALVADOR, 'El Salvador'), (ESPAÑA, 'España'), (ESTADOS_UNIDOS, 'Estados Unidos'), (FILIPINAS, 'Filipinas'), (FRANCIA, 'Francia'), (GUATEMALA, 'Guatemala'),
(HAITI, 'Haití'), (HONDURAS, 'Honduras'), (ITALIA, 'Italia'), (JAPON, 'Japón'), (NICARAGUA, 'Nicaragua'), (PANAMA, 'Panamá'), (PARAGUAY, 'Paraguay'), (PERU, 'Perú'),
(PORTUGAL, 'Portugal'), (PUERTO_RICO, 'Puerto Rico'), (REINO_UNIDO, 'Reino Unido'), (RUSIA, 'Rusia'), (URUGUAY, 'Uruguay'), (VENEZUELA, 'Venezuela')]

EFECTIVO = '10'
CHEQUE = '20'
TRASFERENCIA_BANCARIA = '41'
CONSIGNACION_BANCARIA = '42'
MEDIOS_DE_PAGO = [(EFECTIVO, 'Efectivo'), (CHEQUE, 'Cheque'), (TRASFERENCIA_BANCARIA, 'Transferencia Bancaria'), (CONSIGNACION_BANCARIA, 'Consignación Bancaria')]

VALOR_TOTAL_IVA = "01"
VALOR_TOTAL_IMPUESTO_CONSUMO = "02"
VALOR_TOTAL_ICA = "03"
VALOR_TOTAL_IMPUESTO_NACIONAL_CONSUMO = "04"
TIPO_IMPUESTO = [(VALOR_TOTAL_IVA, "Valor total del IVA"), (VALOR_TOTAL_IMPUESTO_CONSUMO, "Valor total de impuesto al consumo"),
(VALOR_TOTAL_ICA, "Valor total del ICA"), (VALOR_TOTAL_IMPUESTO_NACIONAL_CONSUMO, "Valor total del impuesto nacional al consumo")]

DEVOLUCION_BIENES = "1"
ANULACION_FACTURA = "2"
REBAJA_TOTAL = "3"
DESCUENTO_TOTAL = "4"
RESCISION = "5"
INCUMPLIMIENTO = "6"
INTERESES = "1"
GASTOSXCOBRAR = "2"
CAMBIO_VALOR = "3"
CONCEPTO_NOTA_DEBITO = [(INTERESES, "Intereses"),(GASTOSXCOBRAR, "Gastos por cobrar"),(CAMBIO_VALOR, "Cambio del valor de la Factura")]
CONCEPTO_NOTA_CREDITO = [(DEVOLUCION_BIENES, "Devolución de parte de los bienes; no aceptación de partes del servicio"),
(ANULACION_FACTURA, "Anulación de factura electrónica por falta de requisitos"), (REBAJA_TOTAL, "Rebaja voluntaria al saldo por cobrar"),
(DESCUENTO_TOTAL, "Descuento total aplicado en la factura"), (RESCISION, "Rescisión administrativa; nulidad por recepción de decisión administrativa o judicial."),
(INCUMPLIMIENTO, "Resolución por incumplimientos de lo pactado entre las partes")]

CRECIMIENTO_VENTAS = "V"
CRECIMIENTO_VENTAS_VS_GANANCIAS = "G"
METRICA_CRECIMIENTO = [(CRECIMIENTO_VENTAS, "Crecimiento de Ventas"), (CRECIMIENTO_VENTAS_VS_GANANCIAS, "Crecimiento de Ventas VS Ganancias")]

RENTA_ALQUILER = "R"
SERVICIOS = "S"
PERSONAL = "P"
OFICINA = "O"
PUBLICIDAD = "U"
MANTENIMIENTO = "M"
LIMPIEZA = "L"
ASESORIA = "A"
TRANSPORTE = "T"
IMPUESTOS = "I"
CONCEPTO_GASTO = [(RENTA_ALQUILER, "Pago de Alquiler"), (SERVICIOS, "Pago de Servicios"), (PERSONAL, "Pago de Nómina"),
(OFICINA, "Material de oficina"), (PUBLICIDAD, "Marketing y Publicidad"), (MANTENIMIENTO, "Mantenimiento"), (LIMPIEZA, "Servicios de Limpiesa"),
(ASESORIA, "Asesorías, servicios jurídicos y auditorías"), (TRANSPORTE, "Transporte"), (IMPUESTOS, "Impuestos")]