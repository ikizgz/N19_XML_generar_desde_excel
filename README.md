# N19 XML generar desde Excel

Script Python para generar un archivo XML según la norma 19-14 ISO 20022 para presentar remesas a la Entidad Bancaria.

El script principal toma los datos de las hojas `datos_presentador` y `datos_pagadores` del Excel que se adjunta como ejemplo y genera el correspondiente archivo XML con la remesa de Norma 19 lista para presentar a tu Entidad Bancaria.

## Comenzando 🚀

Para utilizarlo sólamente descarga los archivos en la carpeta que desees.

### Archivos:
- N19_generar_desde_excel.py
- N19_generar_xml.py
- Datos_Remesa_SEPA_Norma_19.xlsx

### Pre-requisitos 📋

_Necesitas tener instalado Python en tu pc._

Puedes descargarlo para tu sistema concreto en [https://www.python.org/downloads/]

## Ejecutando ⚙️

- Modifica el archivo Excel de ejemplo e incorpora los datos reales de tu presentador (los facilita la Entidad) y los datos de los pagadores.
- Ejecuta el script de python N19_generar_desde_excel.py

### Resultado
- Se genera un archivo XML con el nombre %Y-%m-%d_%H%M%S_Remesa_SEPA_Norma_19_14.xml

## Licencia 📄

Este proyecto está bajo la Licencia GPL-3.0 - mira el archivo [LICENSE.md](LICENSE.md) para detalles
