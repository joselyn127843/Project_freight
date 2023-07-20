import sched
from bson import ObjectId
from pymongo import MongoClient
import pandas as pd
import datetime
import sys

client = MongoClient("mongodb://localhost:27017/")
db = client["Pruebas"]
collection_facturas = db["facturas"]
collection_proveedores = db["proveedores"]
collection_cuentas = db["cuentas"]
collection_USD = db["USD"]
collection_EUR = db["EUR"]
collection_pedimemtos = db["pedimentos"]
collection_factores = db["factores"]
collection_pagos = db["pagos"]
collection_fletes = db["fletes"]
collection_pagos_fletes = db["pagos_fletes"]

#validaciones
def validar_fecha(fecha):
    try:
        datetime.datetime.strptime(fecha, "%d-%m-%Y")
        if fecha.count('-') == 2:
            return True
        else:
            raise ValueError("El formato de la fecha es incorrecto. Debe ser dd-mm-aaaa.")
    except ValueError as error:
        print("Error: ", error)
        return False


def validar_numeros(valores):
    for valor in valores:
        if not isinstance(valor, (float, int)):
            errores = (f"¡Error! El valor '{valor}' no es un número válido.")
            print(errores)
            return False
    return True


class fletes ():
    def __init__(self,):
        self.pago = self.pagar_fletes()
        self.factura = self.crear_flete()

    class crear_flete():
        def __init__(self):
            pass

        def crear_flete(self, fecha, serie, folio, proveedor, tipo_cambio, sub_total, iva, retencion_iva, retencion_isr, total, clase, metodo_pago):
            self.fecha = fecha
            self.serie = serie
            self.folio = folio
            self.proveedor = proveedor
            self.tipo_cambio = tipo_cambio
            self.sub_total = sub_total
            self.iva = iva
            self.retencion_iva = retencion_iva
            self.retencion_isr = retencion_isr
            self.total = total
            self.clase = clase       
            self.metodo_pago = metodo_pago     
            
            if validar_fecha(fecha) and validar_numeros([tipo_cambio, sub_total, iva, retencion_iva, retencion_isr, total]):
                flete = {
                    "fecha_comprovante": datetime.datetime.strptime(fecha, "%d-%m-%Y"),
                    "serie": serie,
                    "folio": folio,
                    "proveedor": proveedor,
                    "tipo_cambio": tipo_cambio,
                    "sub_total": sub_total,
                    "iva": iva,
                    "retencion_iva": retencion_iva,
                    "retencion_isr": retencion_isr,
                    "total": total,
                    "clase": clase,
                    "metodo_pago": metodo_pago
                }
                collection_fletes.insert_one(flete)
                print("Flete creado")
            else:
                print("Porfavor verifique los datos capturados.")

        def consultar_flete(self, id_flete):
            self.id_flete = id_flete
            id_flete = ObjectId(id_flete)
            self.data_flete = collection_fletes.find_one({"_id": id_flete})
            if self.data_flete:
                self.fecha = self.data_flete.get("fecha_comprovante")
                self.serie = self.data_flete.get("serie")
                self.folio = self.data_flete.get("folio")
                self.proveedor = self.data_flete.get("proveedor")
                self.tipo_cambio = self.data_flete.get("tipo_cambio")
                self.sub_total = self.data_flete.get("sub_total")
                self.iva = self.data_flete.get("iva")
                self.retencion_iva = self.data_flete.get("retencion_iva")
                self.retencion_isr = self.data_flete.get("retencion_isr")
                self.total = self.data_flete.get("total")
                self.clase = self.data_flete.get("clase")
                self.metodo_pago = self.data_flete.get("metodo_pago")
                print("Flete encontrado")
            else:
                print("No se encontró el flete con el ID especificado")

        def actualizar_flete(self, id_flete, data_new):
            self.id_flete = id_flete
            fecha = data_new.get("fecha_comprovante")
            serie = data_new.get("serie")
            folio = data_new.get("folio")
            proveedor = data_new.get("proveedor")
            tipo_cambio = data_new.get("tipo_cambio")
            sub_total = data_new.get("sub_total")
            iva = data_new.get("iva")
            retencion_iva = data_new.get("retencion_iva")
            retencion_isr = data_new.get("retencion_isr")
            total = data_new.get("total")
            clase = data_new.get("clase")
            if validar_fecha(fecha) and validar_numeros([tipo_cambio, sub_total, iva, retencion_iva, retencion_isr, total]):
                id_flete = ObjectId(id_flete)
                data_flete = collection_fletes.find_one({"_id": id_flete})
                if data_flete:
                    data_new = {
                        "fecha_comprovante": datetime.datetime.strptime(fecha, "%d-%m-%Y"),
                        "serie": serie,
                        "folio": folio,
                        "proveedor": proveedor,
                        "tipo_cambio": tipo_cambio,
                        "sub_total": sub_total,
                        "iva": iva,
                        "retencion_iva": retencion_iva,
                        "retencion_isr": retencion_isr,
                        "total": total,
                        "clase": clase
                    }
                    collection_fletes.update_one({"_id": id_flete}, {"$set": data_new})
                    print("\n""Factura a actualizado:")
                    self.consultar_flete(id_flete)
                    newdata = self.data_flete
                    print("\n".join([f"{key}: {value}" for key, value in newdata.items()]))
                else:
                    print("No se encontró el flete con el ID especificado")
        
        def eliminar_flete(self, id_flete):
            self.consultar_flete(id_flete)
            self.id_flete = id_flete
            id_flete = ObjectId(id_flete)
            if self.data_flete:
                collection_fletes.delete_one({"_id": id_flete})
                print(f"flete Elimnado Serie:'{self.serie}' folio: '{self.folio}'." )
            else:
               pass

    class pagar_fletes(crear_flete):
        def __init__(self):
            super().__init__()
    
        def crear_pago(self, id_flete, fecha, banco, monto, refencia, pedimento, tipo_pago):
            data_factura = self.consultar_flete(id_flete)
            if self.data_flete:
                pago = {
                    "fecha": fecha,
                    "banco": banco,
                    "monto": monto,
                    "refencia": refencia,
                    "pedimento": pedimento,
                    "tipo_pago": tipo_pago,
                    "id_flete": id_flete
                }
                collection_pagos_fletes.insert_one(pago)
                print(f"Pago de flete creado para la factura con ID: {id_flete}, serie {self.serie} y folio {self.serie}")
            else:
                print("No se encontró la factura con el ID especificado")
    
# test facturas

flete = fletes()
#flete.factura.crear_flete("01-01-2021", "A", "1", "5f9f9b3b9c9d6b3b3c4b4b4b", 20, 100, 16, 0, 0, 116, "flete", "PPD")
#flete.factura.consultar_flete("64b83bf49ea1498d767cede1")
#flete.factura.eliminar_flete("64b83c1311156b90fd38da0e")

id_= "64b859265b83b2f39f0601f3"
data_new = {
    "fecha_comprovante": "01-01-2021",
    "serie": "sched",
    "folio": "1764",
    "proveedor": "5f9f9b3b9c9d6b3b3c4b4b4b",
    "tipo_cambio": 20,
    "sub_total": 100,
    "iva": 16,
    "retencion_iva": 100,
    "retencion_isr": 0,
    "total": 116,
    "clase": 0
}
#flete.factura.actualizar_flete(id_, data_new)


# Test de pagos
#flete.pago.crear_pago_2("64b8766de33fa1c05003d7a8")
#flete.pago.crear_pago("64b8766de33fa1c05003d7a8", "01-01-2021", "BANAMEX", 100, "VER23-000001", "3002152", "PPD")
