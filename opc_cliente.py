import time
import opcua
from opcua import ua

import os
import numpy as np

def inicio():
    files = open("./ip_server_opc.txt", "r")
    sw = True
    for file in files:
        client = opcua.Client(file)
        print(file)
        try:
            if client.connect() is None:
                sw = True
                break
        except:
            print("Ha ocurrido un error")
            print("")
            sw = False
    files.close()
    if sw:
        return client
    else:       
        return None

client = inicio()
if client is None:
    print("Error de conexion")
    exit()

while True:    
    #var = client.get_node("NS4|Numeric|5")
    var = client.get_node("ns=4;i=3")
    dv = var.get_value()
    #a =  bool(input("valor"))
    #dv = ua.DataValue(ua.Variant(a, ua.VariantType.Boolean))
    print("VAR",dv)
    var = client.get_node("ns=4;i=5")
    dv = var.get_value()
    print("MOTOR",dv)
  
    a =  input("valor")
    
    if a == "salir": 
        break
    a = bool(a)
    print("a",a)
    dv = ua.DataValue(ua.Variant(a, ua.VariantType.Boolean))
    print("MOTOR mod",dv.Value)
    #time.sleep(1)
    try:
        var.set_value(dv)
    except:
        print("An exception occurred")
    
    b =  input("valor entero")
    b = int(b)
    print("b int",b)
    dv = ua.DataValue(ua.Variant(b, ua.VariantType.Int16))
    print("dv.Value",dv.Value)
    #time.sleep(1)
    var1 = client.get_node("ns=4;i=3")
    #try:
    var1.set_value(dv)
    #except:
    #    print("An exception occurred")
    
    
