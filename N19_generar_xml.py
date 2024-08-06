#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    N19_generar_xml.py
    
    Copyright 2024 Ignacio Izaguerri

    License: GPLv3
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import xml.etree.ElementTree as ET  # Módulo para manejo XML
from datetime import datetime  # Módulo para manejo fechas


# Función para crear el XML según la norma 19-14 ISO 20022
def create_iso20022_xml(datos_presentador, datos_pagadores):
    """
    create_iso20022_xml
    Función para crear el XML según la norma 19-14 ISO 20022
    usando dos DataFrame pasadas como parámetros.

    @param:
        - datos_presentador (contiene: Presentador, NIF, IdPresentador, Sufijo, IBAN, BIC_Entidad, Fecha_Cargo)
        - datos_pagadores (contiene: NIF, Nombre, Apellidos, IBAN, Mandato, Firma_Mandato, Tipo_Adeudo, Referencia_Adeudo, Importe, Concepto)

    @return:
        - estructura XML ISO 20022 creada con los datos pasados.
    """

    # Crear el elemento raíz
    root = ET.Element(
        "Document", xmlns="urn:iso:std:iso:20022:tech:xsd:pain.008.001.02"
    )
    CstmrDrctDbtInitn = ET.SubElement(root, "CstmrDrctDbtInitn")

    # Información del grupo de cabecera
    GrpHdr = ET.SubElement(CstmrDrctDbtInitn, "GrpHdr")
    MsgId = ET.SubElement(GrpHdr, "MsgId")
    MsgId.text = f"MSG-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    CreDtTm = ET.SubElement(GrpHdr, "CreDtTm")
    CreDtTm.text = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    NbOfTxs = ET.SubElement(GrpHdr, "NbOfTxs")
    NbOfTxs.text = str(len(datos_pagadores))
    CtrlSum = ET.SubElement(GrpHdr, "CtrlSum")
    CtrlSum.text = f"{datos_pagadores['Importe'].sum():.2f}"
    InitgPty = ET.SubElement(GrpHdr, "InitgPty")
    Nm = ET.SubElement(InitgPty, "Nm")
    Nm.text = datos_presentador.loc[0, "Presentador"]
    Id = ET.SubElement(InitgPty, "Id")
    OrgId = ET.SubElement(Id, "OrgId")
    Othr = ET.SubElement(OrgId, "Othr")
    Id = ET.SubElement(Othr, "Id")
    Id.text = datos_presentador.loc[0, "IdPresentador"]

    # Información de la presentación de cobro
    PmtInf = ET.SubElement(CstmrDrctDbtInitn, "PmtInf")
    PmtInfId = ET.SubElement(PmtInf, "PmtInfId")
    # PmtInfId.text deberia ser NIFPresentador & Sufijo & Format(FechaCargo, "yyyymmdd") & Format(FechaActual, "yyyymmdd") & Format(FechaActual, "HHMMSS")
    PmtInfId.text = f"{datos_presentador.loc[0, "NIF"]}{datos_presentador.loc[0, "Sufijo"]:03d}{datos_presentador["Fecha_Cargo"].iloc[0].strftime("%Y%m%d")}{datetime.now().strftime('%Y%m%d%H%M%S')}"
    PmtMtd = ET.SubElement(PmtInf, "PmtMtd")
    PmtMtd.text = "DD"
    BtchBookg = ET.SubElement(PmtInf, "BtchBookg")
    BtchBookg.text = "true"
    NbOfTxs = ET.SubElement(PmtInf, "NbOfTxs")
    NbOfTxs.text = str(len(datos_pagadores))
    CtrlSum = ET.SubElement(PmtInf, "CtrlSum")
    CtrlSum.text = f"{datos_pagadores['Importe'].sum():.2f}"
    PmtTpInf = ET.SubElement(PmtInf, "PmtTpInf")
    SvcLvl = ET.SubElement(PmtTpInf, "SvcLvl")
    Cd = ET.SubElement(SvcLvl, "Cd")
    Cd.text = "SEPA"
    LclInstrm = ET.SubElement(PmtTpInf, "LclInstrm")
    Cd = ET.SubElement(LclInstrm, "Cd")
    Cd.text = "CORE"
    SeqTp = ET.SubElement(PmtTpInf, "SeqTp")
    SeqTp.text = "RCUR"
    ReqdColltnDt = ET.SubElement(PmtInf, "ReqdColltnDt")
    ReqdColltnDt.text = datos_presentador["Fecha_Cargo"].iloc[0].strftime("%Y-%m-%d")
    Cdtr = ET.SubElement(PmtInf, "Cdtr")
    Nm = ET.SubElement(Cdtr, "Nm")
    Nm.text = datos_presentador.loc[0, "Presentador"]
    CdtrAcct = ET.SubElement(PmtInf, "CdtrAcct")
    Id = ET.SubElement(CdtrAcct, "Id")
    IBAN = ET.SubElement(Id, "IBAN")
    IBAN.text = datos_presentador.loc[0, "IBAN"]
    CdtrAgt = ET.SubElement(PmtInf, "CdtrAgt")
    FinInstnId = ET.SubElement(CdtrAgt, "FinInstnId")
    BIC = ET.SubElement(FinInstnId, "BIC")
    BIC.text = datos_presentador.loc[0, "BIC_Entidad"]
    ChrgBr = ET.SubElement(PmtInf, "ChrgBr")
    ChrgBr.text = "SLEV"
    CdtrSchmeId = ET.SubElement(PmtInf, "CdtrSchmeId")
    Id = ET.SubElement(CdtrSchmeId, "Id")
    OrgId = ET.SubElement(Id, "OrgId")
    Othr = ET.SubElement(OrgId, "Othr")
    Id = ET.SubElement(Othr, "Id")
    Id.text = datos_presentador.loc[0, "IdPresentador"]

    # Información de cada adeudo directo
    for index, row in datos_pagadores.iterrows():
        DrctDbtTxInf = ET.SubElement(PmtInf, "DrctDbtTxInf")
        PmtId = ET.SubElement(DrctDbtTxInf, "PmtId")
        EndToEndId = ET.SubElement(PmtId, "EndToEndId")
        EndToEndId.text = row["Referencia_Adeudo"]
        InstdAmt = ET.SubElement(DrctDbtTxInf, "InstdAmt", Ccy="EUR")
        InstdAmt.text = f"{row['Importe']:.2f}"
        DrctDbtTx = ET.SubElement(DrctDbtTxInf, "DrctDbtTx")
        MndtRltdInf = ET.SubElement(DrctDbtTx, "MndtRltdInf")
        MndtId = ET.SubElement(MndtRltdInf, "MndtId")
        MndtId.text = row["Mandato"]
        DtOfSgntr = ET.SubElement(MndtRltdInf, "DtOfSgntr")
        DtOfSgntr.text = row["Firma_Mandato"].strftime("%Y-%m-%d")
        DbtrAgt = ET.SubElement(DrctDbtTxInf, "DbtrAgt")
        FinInstnId = ET.SubElement(DbtrAgt, "FinInstnId")
        Othr = ET.SubElement(FinInstnId, "Othr")
        Id = ET.SubElement(Othr, "Id")
        Id.text = "NOTPROVIDED"
        Dbtr = ET.SubElement(DrctDbtTxInf, "Dbtr")
        Nm = ET.SubElement(Dbtr, "Nm")
        Nm.text = f"{row['Nombre']} {row['Apellidos']}"
        Id = ET.SubElement(Dbtr, "Id")
        PrvtId = ET.SubElement(Id, "PrvtId")
        Othr = ET.SubElement(PrvtId, "Othr")
        Id = ET.SubElement(Othr, "Id")
        Id.text = row["NIF"]
        DbtrAcct = ET.SubElement(DrctDbtTxInf, "DbtrAcct")
        Id = ET.SubElement(DbtrAcct, "Id")
        IBAN = ET.SubElement(Id, "IBAN")
        IBAN.text = row["IBAN"].replace(" ", "")
        RmtInf = ET.SubElement(DrctDbtTxInf, "RmtInf")
        Ustrd = ET.SubElement(RmtInf, "Ustrd")
        Ustrd.text = row["Concepto"]
    
    # Convertir el árbol a una cadena XML
    xml_str = ET.tostring(root, encoding="utf-8", method="xml")
    return xml_str

def main():
    print(__name__)
    print(__doc__)
    print(create_iso20022_xml.__doc__)
    
if __name__ == '__main__':
    main()