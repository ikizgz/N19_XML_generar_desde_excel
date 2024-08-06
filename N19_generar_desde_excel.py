#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#  N19_generar_desde_excel.py
#
#  Copyright 2024 Ignacio Izaguerri
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
"""

import pathlib  # Módulo para manejo paths
from datetime import datetime  # Módulo para manejo fechas

import pandas as pd  # Módulo para manejo y análisis de estructuras de datos (Listas y DataFrames {matrices})

from N19_generar_xml import (
    create_iso20022_xml,  # Módulo N19_generar_xml en la misma carpeta
)

# Cargar el archivo Excel
file_path = pathlib.Path(__file__).parent / "Datos_Remesa_SEPA_Norma_19.xlsx"
datos_presentador = pd.read_excel(file_path, sheet_name="Datos_Presentador")
print(datos_presentador)
datos_pagadores = pd.read_excel(file_path, sheet_name="Datos_Pagadores")
print(datos_pagadores)

# Crear el archivo XML
xml_data = create_iso20022_xml(datos_presentador, datos_pagadores)

# Guardar el archivo XML
xml_file_path = (
    pathlib.Path(__file__).parent
    / f"{datetime.now().strftime("%Y-%m-%d_%H%M%S")}_Remesa_SEPA_Norma_19_14.xml"
)
with open(xml_file_path, "wb") as f:
    f.write(xml_data)

print(f"Archivo XML generado: {xml_file_path}")