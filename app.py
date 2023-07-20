import sched
from bson import ObjectId
from pymongo import MongoClient
import pandas as pd
import datetime
import sys
from bson.binary import Binary
import os

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
collection_archivos = db["archivos"]

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
        self.archivos = self.archivos_flete()

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
                print(f"Pago de flete creado para la factura con ID: {id_flete}, serie {self.serie} y folio {self.folio}")
            else:
                print("No se encontró la factura con el ID especificado")

        def consultar_pagos(self, id_flete):
            self.id_flete = id_flete
            self.consultar_flete(id_flete)
            self.data_pagos = list(collection_pagos_fletes.find({"id_flete": str(id_flete)}))
            self.suma_pagos = 0
            self.total = self.data_flete.get("total")
            
            if self.data_pagos:
                for pago in self.data_pagos:
                    print("-----")
                    print("\n".join([f"{key}: {value}" for key, value in pago.items()]))
                    print("-----")
                    self.suma_pagos += pago.get("monto")

                print(f"Total de pagos: {self.suma_pagos}")
                print(f"Total de la factura: {self.total}")

                self.saldo = self.total - self.suma_pagos
                if self.saldo == 0:
                    print("La factura ya está pagada")
                elif self.saldo > 0:
                    print(f"Saldo pendiente: {self.saldo}")
                elif self.saldo < 0:
                    print("La factura está sobre pagada")
                else:
                    print("Error al calcular el saldo")            
            else:
                print("No se encontraron pagos para la factura con el ID especificado")

        def actualizar_pago(self, id_pago, data_new):
            self.id_pago = id_pago
            fecha = data_new.get("fecha")
            banco = data_new.get("banco")
            monto = data_new.get("monto")
            refencia = data_new.get("refencia")
            pedimento = data_new.get("pedimento")
            tipo_pago = data_new.get("tipo_pago")
            if validar_fecha(fecha) and validar_numeros([monto]):
                id_pago = ObjectId(id_pago)
                data_pago = collection_pagos_fletes.find_one({"_id": id_pago})
                if data_pago:
                    data_new = {
                        "fecha": fecha,
                        "banco": banco,
                        "monto": monto,
                        "refencia": refencia,
                        "pedimento": pedimento,
                        "tipo_pago": tipo_pago
                    }
                    collection_pagos_fletes.update_one({"_id": id_pago}, {"$set": data_new})
                    print("\n""Pago actualizado:")
                    self.consultar_pagos(data_pago.get("id_flete"))
                else:
                    print("No se encontró el pago con el ID especificado")
    
        def eliminar_pago(self, id_pago):
            self.id_pago = id_pago
            id_pago = ObjectId(id_pago)
            data_pago = collection_pagos_fletes.find_one({"_id": id_pago})
            if data_pago:
                collection_pagos_fletes.delete_one({"_id": id_pago})
                print(f"Pago Elimnado")
                self.consultar_pagos(data_pago.get("id_flete"))
            else:
                print("No se encontró el pago con el ID especificado")
    
    class archivos_flete(crear_flete):
        def __init__(self):
            super().__init__()
        def guardar_archivo(self, id_elemento,url):
            self.id_elemento = id_elemento
            self.data_archivo = collection_archivos.find_one({"id_elemento": id_elemento})

            if self.data_archivo:
                self.mensaje = "El archivo ya existe"
                print(self.mensaje)
            else:
                self.consultar_flete(id_elemento)
                self.nombre_archivo = "archivo-" + id_elemento + ".pdf"
                with open(url, "rb") as archivo_pdf:
                    contenido_binario = archivo_pdf.read()
                documento = {
                    "id_elemento": id_elemento,
                    "nombre_archivo": self.nombre_archivo,
                    "archivo": Binary(contenido_binario)
                }
                collection_archivos.insert_one(documento)
                self.mensaje = (f"archivo del flete con serie {self.serie} y folio {self.folio} guardado")
                print(self.mensaje)

        def consultar_archivo(self, id_elemento):
            self.id_elemento = id_elemento
            self.data_archivo = collection_archivos.find_one({"id_elemento": id_elemento})
            if self.data_archivo:
                self.nombre_archivo = self.data_archivo.get("nombre_archivo")
                self.archivo = self.data_archivo.get("archivo")
                ruta_descarga = os.path.join("static", "temp", "archivo_descargado.pdf")
                with open(ruta_descarga, "wb") as archivo_pdf:
                    archivo_pdf.write(self.archivo)
                print("archivo descargado")
            else:
                print("No se encontró el archivo con el ID especificado")
    
# crear pago 

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
#flete.pago.crear_pago("64b8b33a01bc283c649eb332", "01-01-2021", "BANAMEX", 10, "VER23-000001", "3002152", "PPD")
#flete.pago.consultar_pagos("64b8b33a01bc283c649eb332")
#flete.pago.eliminar_pago("64b8b77627091d07946f045e")

# Test de archivos
#flete.archivos.guardar_archivo("64b8b33a01bc283c649eb332","static/temp/archivo.pdf")
#flete.archivos.consultar_archivo("64b8b33a01bc283c649eb332")