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
collection_proveedores = db["proveedores"]
collection_cuentas = db["cuentas"]
collection_referencias = db["referencias"]
collection_fletes = db["fletes"]
collection_pagos = db["pagos"]
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
    
        def crear_pago(self, id_flete, fecha, banco, monto, tipo_pago,):
            data_factura = self.consultar_flete(id_flete)
            if self.data_flete:
                pago = {
                    "fecha": fecha,
                    "banco": banco,
                    "monto": monto,
                    "tipo_pago": tipo_pago,
                    "id_flete": id_flete,
                    "clase": "pago_flete",
                }
                collection_pagos.insert_one(pago)
                print(f"Pago de flete creado para la factura con ID: {id_flete}, serie {self.serie} y folio {self.folio}")
            else:
                print("No se encontró la factura con el ID especificado")

        def consultar_pagos(self, id_flete):
            self.id_flete = id_flete
            self.consultar_flete(id_flete)
            self.data_pagos = list(collection_pagos.find({"id_flete": id_flete}))
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
            tipo_pago = data_new.get("tipo_pago")
            if validar_fecha(fecha) and validar_numeros([monto]):
                id_pago = ObjectId(id_pago)
                data_pago = collection_pagos.find_one({"_id": id_pago})
                if data_pago:
                    data_new = {
                        "fecha": fecha,
                        "banco": banco,
                        "monto": monto,
                        "tipo_pago": tipo_pago,
                        "clase": "pago_flete"
                    }
                    collection_pagos.update_one({"_id": id_pago}, {"$set": data_new})
                    print("\n""Pago actualizado:")
                    self.consultar_pagos(data_pago.get("id_flete"))
                else:
                    print("No se encontró el pago con el ID especificado")
    
        def eliminar_pago(self, id_pago):
            self.id_pago = id_pago
            id_pago = ObjectId(id_pago)
            data_pago = collection_pagos.find_one({"_id": id_pago})
            if data_pago:
                collection_pagos.delete_one({"_id": id_pago})
                self.mensaje = (f"pago con ID: {id_pago} eliminado")
                self.mensaje = f"pago con ID: {id_pago} eliminado"; print(self.mensaje)

            else:
                self.mensaje = "No se encontró el pago con el ID especificado"; print(self.mensaje)

        def consultar_todos_pagos(self):
            # buscar todos los pagos con clase "pago_flete"
            self.data_pagos = list(collection_pagos.find({"clase": "pago_flete"}))
            if self.data_pagos:
                for pago in self.data_pagos:
                    print("-----")
                    print("\n".join([f"{key}: {value}" for key, value in pago.items()]))
                    print("-----")
                self.mensaje = "Pagos encontrados"; print(self.mensaje)
            else:
                self.mensaje = "No se encontraron pagos de fletes"; print(self.mensaje)     
    
    class archivos_flete(crear_flete):
        def __init__(self):
            super().__init__()
        def guardar_archivo(self, id_elemento,url):
            self.id_elemento = id_elemento
            self.data_archivo = collection_archivos.find_one({"id_elemento": str(id_elemento)})

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
                    "archivo": Binary(contenido_binario),
                    "clase" : "archivo_flete"
                }
                collection_archivos.insert_one(documento)
                self.mensaje = (f"archivo del flete con serie {self.serie} y folio {self.folio} guardado")
                print(self.mensaje)

        def consultar_archivo(self, id_elemento):
            self.id_elemento = id_elemento
            self.data_archivo = collection_archivos.find_one({"id_elemento": str(id_elemento)})
            if self.data_archivo:
                self.nombre_archivo = self.data_archivo.get("nombre_archivo")
                self.archivo = self.data_archivo.get("archivo")
                ruta_descarga = os.path.join("static", "temp", "archivo_descargado.pdf")
                with open(ruta_descarga, "wb") as archivo_pdf:
                    archivo_pdf.write(self.archivo)
                self.mensaje = (f"archivo del flete con ID: {id_elemento} descargado"); print(self.mensaje)
            else:
                self.mensaje = "No se encontró el archivo con el ID especificado"; print(self.mensaje)
    
        def editar_archivo(self, id_elemento, url):
            self.id_elemento = id_elemento
            self.data_archivo = collection_archivos.find_one({"id_elemento": str(id_elemento)})
            self.url = url
            if self.data_archivo:
                self.nombre_archivo = "archivo-" + id_elemento + ".pdf"
                with open(url, "rb") as archivo_pdf:
                    contenido_binario = archivo_pdf.read()
                documento = {
                    "id_elemento": id_elemento,
                    "nombre_archivo": self.nombre_archivo,
                    "archivo": Binary(contenido_binario)
                }
                collection_archivos.update_one({"id_elemento": id_elemento}, {"$set": documento})
                self.mensaje = (f"archivo del flete con ID: {id_elemento} actualizado"); print(self.mensaje)
            else:
                self.mensaje = "No se encontró el archivo con el ID especificado"; print(self.mensaje)

        def eliminar_archivo(self, id_elemento):
            self.id_elemento = id_elemento
            self.consultar_flete(id_elemento)
            serie = self.serie
            folio = self.folio
            self.data_archivo = collection_archivos.find_one({"id_elemento": str(id_elemento)})
            if self.data_archivo:
                collection_archivos.delete_one({"id_elemento": str(id_elemento)})
                self.mensaje = (f"archivo del flete con serie {serie}, y folio: {folio} Eliminado "); print(self.mensaje)
            else:
                self.mensaje = "No se encontró el archivo con el ID especificado"; print(self.mensaje)

        def cosultar_todos_fletes(self):
            self.data_archivos = list(collection_archivos.find({"clase": "archivo_flete"}))
            if self.data_archivos:
                for archivo in self.data_archivos:
                    _id = archivo.get("id_elemento")
                    id_elemento = archivo.get("id_elemento")
                    nombre_archivo = archivo.get("nombre_archivo")
                    clase = archivo.get("clase")
                    print("-----")
                    print(f"_id: {_id}, id_elemento: {id_elemento}, nombre_archivo: {nombre_archivo}, clase: {clase}")
                    print("-----")
                self.mensaje = "Archivos encontrados"; print(self.mensaje)
            else:
                self.mensaje = "No se encontraron archivos"; print(self.mensaje)

    class asignar(crear_flete):
        def __init__(self):
            super().__init__()

        def asignar_referencia(self, id_flete, id_referencia):
            self.id_flete = id_flete
            self.id_referencia = id_referencia
            pass
        

class cuentas():
    def __init__(self):
        pass

    def crear_cuenta(self, nombre, tipo_cuenta, cuenta_numero, moneda):
        self.nombre = nombre
        self.tipo_cuenta = tipo_cuenta
        self.cuenta_numero = cuenta_numero
        self.moneda = moneda
        cuenta = {
            "nombre": nombre,
            "tipo_cuenta": tipo_cuenta,
            "cuenta_numero": cuenta_numero,
            "moneda": moneda
        }
        collection_cuentas.insert_one(cuenta)
        print("Cuenta creada")
    
    def consultar_cuenta(self, id_cuenta):
        self.id_cuenta = id_cuenta
        id_cuenta = ObjectId(id_cuenta)
        self.data_cuenta = collection_cuentas.find_one({"_id": id_cuenta})
        if self.data_cuenta:
            self.nombre = self.data_cuenta.get("nombre")
            self.tipo_cuenta = self.data_cuenta.get("tipo_cuenta")
            self.cuenta_numero = self.data_cuenta.get("cuenta_numero")
            self.moneda = self.data_cuenta.get("moneda")
            self.mensaje = (f"Cuenta encontrada: {self.nombre}, Numero: {self.cuenta_numero}"); print(self.mensaje)
        else:
            self.mensaje = "No se encontró la cuenta con el ID especificado"; print(self.mensaje)

    def editar_cuenta(self, id_cuenta, data_new):
        self.id_cuenta = ObjectId(id_cuenta)
        self.data_cuenta = collection_cuentas.find_one({"_id": self.id_cuenta})
        if self.data_cuenta:
            nombre = data_new.get("nombre")
            tipo_cuenta = data_new.get("tipo_cuenta")
            cuenta_numero = data_new.get("cuenta_numero")
            moneda = data_new.get("moneda")
            data_new = {
                "nombre": nombre,
                "tipo_cuenta": tipo_cuenta,
                "cuenta_numero": cuenta_numero,
                "moneda": moneda
            }
            collection_cuentas.update_one({"_id": self.id_cuenta}, {"$set": data_new})
            self.mensaje = (f"Cuenta con ID: {id_cuenta} actualizada"); print(self.mensaje)
        else:
            self.mensaje = "No se encontró la cuenta con el ID especificado"; print(self.mensaje)

    def eliminar_cuenta(self, id_cuenta):
        self.id_cuenta = id_cuenta
        id_cuenta = ObjectId(id_cuenta)
        self.data_cuenta = collection_cuentas.find_one({"_id": id_cuenta})
        if self.data_cuenta:
            collection_cuentas.delete_one({"_id": id_cuenta})
            self.mensaje = (f"Cuenta con ID: {id_cuenta} eliminada"); print(self.mensaje)
        else:
            self.mensaje = "No se encontró la cuenta con el ID especificado"; print(self.mensaje)

    def consultar_cuentas(self):
        self.data_cuentas = list(collection_cuentas.find())
        if self.data_cuentas:
            for cuenta in self.data_cuentas:
                print("-----")
                print("\n".join([f"{key}: {value}" for key, value in cuenta.items()]))
                print("-----")
                self.mensaje = "Cuentas encontradas"; print(self.mensaje)
        else:
            self.mensaje = "No se encontraron cuentas"; print(self.mensaje)


class proveedores():
    def __init__(self):
        pass
    def crear_proveedor(self, nombre, id_fiscal, pais, clave_pais, cuenta_principal, cuenta_secundaria, moneda):
        self.nombre = nombre
        self.id_fiscal = id_fiscal
        self.pais = pais
        self.clave_pais = clave_pais
        self.cuenta_principal = cuenta_principal
        self.cuenta_secundaria = cuenta_secundaria
        self.moneda = moneda
        data_proveedor = collection_proveedores.find_one({"id_fiscal": id_fiscal})
        if data_proveedor == None:
            proveedor = {"nombre": nombre,"id_fiscal": id_fiscal,"pais": pais,"clave_pais": clave_pais,"cuenta_principal": cuenta_principal,"cuenta_secundaria": cuenta_secundaria,"moneda": moneda}
            collection_proveedores.insert_one(proveedor)
            self.mensaje = "Proveedor creado con exito"; print(self.mensaje)
        else:
            self.mensaje = "El proveedor ya existe"; print(self.mensaje)
    
    def consultar_proveedor(self, id_provedor):
        self.id_provedor = id_provedor
        self.data_proveedor = collection_proveedores.find_one({"_id": ObjectId(id_provedor)})
        if self.data_proveedor:
            self.nombre = self.data_proveedor.get("nombre")
            self.id_fiscal = self.data_proveedor.get("id_fiscal")
            self.pais = self.data_proveedor.get("pais")
            self.clave_pais = self.data_proveedor.get("clave_pais")
            self.cuenta_principal = self.data_proveedor.get("cuenta_principal")
            self.cuenta_secundaria = self.data_proveedor.get("cuenta_secundaria")
            self.moneda = self.data_proveedor.get("moneda")
            self.mensaje = (f"Proveedor encontrado: {self.nombre}, RFC: {self.id_fiscal}"); print(self.mensaje)
        else:
            self.mensaje = "No se encontró el proveedor con el ID especificado"; print(self.mensaje)

    def editar_proveedor(self, id_provedor,nombre, id_fiscal, pais, clave_pais, cuenta_principal, cuenta_secundaria, moneda):
        self.nombre = nombre
        self.id_fiscal = id_fiscal
        self.pais = pais
        self.clave_pais = clave_pais
        self.cuenta_principal = cuenta_principal
        self.cuenta_secundaria = cuenta_secundaria
        self.moneda = moneda
        self.data_proveedor = collection_proveedores.find_one({"_id": ObjectId(id_provedor)})
        if self.data_proveedor:
            data_new = {
                "nombre": nombre, "id_fiscal": id_fiscal, "pais": pais, "clave_pais": clave_pais,"cuenta_principal": cuenta_principal, "cuenta_secundaria": cuenta_secundaria, "moneda": moneda}
            collection_proveedores.update_one({"_id": ObjectId(id_provedor)}, {"$set": data_new})
            self.mensaje = (f"Proveedor con ID: {id_provedor} actualizado"); print(self.mensaje)
        else:
            self.mensaje = "No se encontró el proveedor con el ID especificado"; print(self.mensaje)

    def eliminar_proveedor(self, id_provedor):
        self.id_provedor = id_provedor
        self.data_proveedor = collection_proveedores.find_one({"_id": ObjectId(id_provedor)})
        if self.data_proveedor:
            collection_proveedores.delete_one({"_id": ObjectId(id_provedor)})
            self.mensaje = (f"Proveedor con ID: {id_provedor} eliminado"); print(self.mensaje)
        else:
            self.mensaje = "No se encontró el proveedor con el ID especificado"; print(self.mensaje)

    def consultar_todos_proveedores(self):
        self.data_proveedores = list(collection_proveedores.find())
        if self.data_proveedores:
            for proveedor in self.data_proveedores:
                print("-----")
                print("\n".join([f"{key}: {value}" for key, value in proveedor.items()]))
                print("-----")
                self.mensaje = "Proveedores encontrados"; print(self.mensaje)
        else:
            self.mensaje = "No se encontraron proveedores"; print(self.mensaje)


class referencia():
    def __init__(self):
        pass

    def crear_referencia(self, referencia, pedimentos, detalle_bien, proveedor, contendores):
        self.referencia = referencia
        self.pedimentos = pedimentos
        self.detalle_bien = detalle_bien
        self.proveedor = proveedor
        self.contendores = contendores
        self.data_referencia = collection_referencias.find_one({"referencia": referencia})
        self.data_proveedor = collection_proveedores.find_one({"_id": ObjectId(proveedor)})
        print(self.data_proveedor)
        if self.data_proveedor:
            if self.data_referencia == None:
                data_referencia = {"referencia": referencia, "pedimentos": pedimentos, "detalle_bien": detalle_bien, "proveedor": proveedor, "contendores": contendores}
                collection_referencias.insert_one(data_referencia)
                self.mensaje = "Referencia creada con exito"; print(self.mensaje)
            else:
                self.mensaje = "La referencia ya existe"; print(self.mensaje)
        else:
            self.mensaje = "No se encontró el proveedor con el ID especificado"; print(self.mensaje)

    def consultar_referencia(self, id_referencia):
        self.id_referencia = id_referencia
        self.data_referencia = collection_referencias.find_one({"_id": ObjectId(id_referencia)})
        self.data_proveedor = collection_proveedores.find_one({"_id": ObjectId(self.data_referencia.get("proveedor"))})
        if self.data_referencia:
            self.referencia = self.data_referencia.get("referencia")
            self.pedimentos = self.data_referencia.get("pedimentos")
            self.detalle_bien = self.data_referencia.get("detalle_bien")
            self.proveedor = self.data_referencia.get("proveedor")
            self.contendores = self.data_referencia.get("contendores")
            self.nombre_proveedor = self.data_proveedor.get("nombre")
            self.mensaje = (f"Referencia encontrada: {self.referencia}"); print(self.mensaje)
            print("-----")
            print(f"Referencia: {self.referencia} \nPedimentos: {self.pedimentos} \nDetalle del bien: {self.detalle_bien} \nProveedor: {self.nombre_proveedor} \nContendores: {self.contendores}")
            print("-----")
        else:
            self.mensaje = "No se encontró la referencia con el ID especificado"; print(self.mensaje)

    def editar_referencia(self, id_referencia, referencia, pedimentos, detalle_bien, proveedor, contendores):
        self.id_referencia = id_referencia
        self.referencia = referencia
        self.pedimentos = pedimentos
        self.detalle_bien = detalle_bien
        self.proveedor = proveedor
        self.contendores = contendores
        data_referencia = collection_referencias.find_one({"_id": ObjectId(id_referencia)})
        if data_referencia:
            data_new = {"referencia": referencia, "pedimentos": pedimentos, "detalle_bien": detalle_bien, "proveedor": proveedor, "contendores": contendores}
            collection_referencias.update_one({"_id": ObjectId(id_referencia)}, {"$set": data_new})
            self.mensaje = (f"Referencia con ID: {id_referencia} actualizada"); print(self.mensaje)
        else:
            self.mensaje = "No se encontró la referencia con el ID especificado para eliminar"; print(self.mensaje)

    def eliminar_referencia(self, id_referencia):
        self.id_referencia = id_referencia
        data_referencia = collection_referencias.find_one({"_id": ObjectId(id_referencia)})
        if data_referencia:
            collection_referencias.delete_one({"_id": ObjectId(id_referencia)})
            self.mensaje = (f"Referencia con ID: {id_referencia} eliminada"); print(self.mensaje)
        else:
            self.mensaje = "No se encontró la referencia con el ID especificado"; print(self.mensaje)
    
    def consulta_totad_refrencias(self):
        self.data_referencias = list(collection_referencias.find())
        if self.data_referencias:
            for referencia in self.data_referencias:
                print("-----")
                print("\n".join([f"{key}: {value}" for key, value in referencia.items()]))
                print("-----")
                self.mensaje = "Referencias encontradas"; print(self.mensaje)
        else:
            self.mensaje = "No se encontraron referencias"; print(self.mensaje)


# test pagos
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
#flete.archivos.guardar_archivo("64b8766de33fa1c05003d7a8","static/temp/archivo.pdf")
#flete.archivos.consultar_archivo("64b8766de33fa1c05003d7a8")
#flete.archivos.editar_archivo("64b8766de33fa1c05003d7a8","static/temp/archivo_update.pdf")
#flete.archivos.eliminar_archivo("64b8766de33fa1c05003d7a8")
#flete.archivos.cosultar_todos_fletes()


# Test de cuentas
cuenta = cuentas()
#cuenta.crear_cuenta("SANTANDER", "Cheques", "123456789", "MXN")
#cuenta.consultar_cuenta("64b96e7b3a849c0ade58367d")
data_new = {
    "nombre": "BANORTE",
    "tipo_cuenta": "Cheques",
    "cuenta_numero": "123456789",
    "moneda": "MXN"
}
#cuenta.editar_cuenta("64b96e7b3a849c0ade58367d", data_new)
#cuenta.eliminar_cuenta("64b96e7b3a849c0ade58367d")
#cuenta.consultar_cuentas()

# Test de proveedores
proveedor = proveedores()
#proveedor.crear_proveedor("ALL MIGHT", "ALLM-000000", "MEXICO", "MX", "123456789", "", "MXN")
#proveedor.consultar_proveedor("64b98d5af038e5b5baab32bb")
#proveedor.editar_proveedor("64b98d5af038e5b5baab32bb", "ALL MIGHT NUEVO", "ALLM-000000", "MEXICO", "MX", "123456789", "", "MXN")
#proveedor.consultar_proveedor("64b98d5af038e5b5baab32bb")
#proveedor.eliminar_proveedor("64b98d5af038e5b5baab32bb")


referencia_data = {
    "referencia": "REF-000001",
    "pedimentos": ["PED-000001"],
    "detalle_bien": "Detalle del bien",
    "proveedor": "64b9c686d3b905e724d6ca3d",
    "contendores": ["CONT-000001", "CONT-000002"]
}
id_referencia = "64b9c9b6d9b4c7d005526fc2"
referencia = referencia()
#referencia.crear_referencia(**referencia_data)
#referencia.consultar_referencia(id_referencia)
#referencia.editar_referencia(id_referencia, "REF-000001", ["PED-000002"], "Detalle del bien", "64b9c686d3b905e724d6ca3d", ["CONT-000001", "CONT-000002"])
#referencia.eliminar_referencia(id_referencia)