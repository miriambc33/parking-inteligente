import os
import time
from datetime import datetime
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials

# Clave y endpoint de Azure
AZURE_KEY = "CwmlTZ0fkq34inleOOrBif7ATNdvrpmiEX5wIFJbz2tLw9vQeuEVJQQJ99BBAC5RqLJXJ3w3AAAFACOG6TCY"
AZURE_ENDPOINT = "https://pruebavision33.cognitiveservices.azure.com/"

computervision_client = ComputerVisionClient(AZURE_ENDPOINT, CognitiveServicesCredentials(AZURE_KEY))

# Leer matrícula
def leer_matricula(imagen):
    try:
        time.sleep(1.5)
        with open(imagen, "rb") as image_stream:
            result = computervision_client.read_in_stream(image_stream, raw=True)

        operation_location = result.headers["Operation-Location"]
        operation_id = operation_location.split("/")[-1]

        while True:
            result = computervision_client.get_read_result(operation_id)
            if result.status not in ['notStarted', 'running']:
                break
            time.sleep(1.5)

        if result.status == OperationStatusCodes.succeeded:
            for line in result.analyze_result.read_results:
                for word in line.lines:
                    texto = word.text.strip().replace(" ", "").upper()
                    if validar_matricula(texto):
                        return texto
                    else:
                        print(f" Matrícula no válida: {texto}")
        return ''
    except Exception as e:
        print(f"[ERROR] en leer_matricula ({imagen}): {e}")
        return ''


def validar_matricula(m):
    import re
    return re.match(r'^\d{4}[A-Z]{3}$', m.replace(" ", "").replace("O", "0").replace("I", "1")) is not None


# Leer entradas existentes
def leer_entradas():
    mapa = {}
    if os.path.exists("entradas.txt"):
        with open("entradas.txt", "r") as f:
            for linea in f:
                partes = linea.strip().split(";")
                if len(partes) == 2:
                    matricula, fecha = partes
                    mapa[matricula] = datetime.strptime(fecha, "%d/%m/%Y %H:%M")
    return mapa

# Procesar imágenes de entrada
def leer_matriculas_entrada(coches):
    for fichero in os.listdir("entradas"):
        ruta = os.path.join("entradas", fichero)
        matricula = leer_matricula(ruta)
        if matricula:
            coches[matricula] = datetime.now()
        else:
        os.remove(ruta)

# Procesar imágenes de salida
def leer_matriculas_salida(coches):
    for fichero in os.listdir("salidas"):
        ruta = os.path.join("salidas", fichero)
        matricula = leer_matricula(ruta)
        salida = datetime.now()
        with open("salidas.txt", "a") as f:
            if matricula in coches:
                entrada = coches[matricula]
                horas = int((salida - entrada).total_seconds() // 3600)
                precio = horas * 6
                f.write(f"{matricula};{entrada.strftime('%d/%m/%Y %H:%M')};{salida.strftime('%d/%m/%Y %H:%M')};{precio}\n")
                del coches[matricula]
            else:
                f.write(f"{matricula};00/00/0000 00:00;{salida.strftime('%d/%m/%Y %H:%M')};100\n")
        os.remove(ruta)


# Actualizar fichero de entradas
def actualizar_entradas(coches):
    with open("entradas.txt", "w") as f:
        for matricula, fecha in coches.items():
            f.write(f"{matricula};{fecha.strftime('%d/%m/%Y %H:%M')}\n")

# Programa principal
def main():
    coches = leer_entradas()
    leer_matriculas_entrada(coches)
    leer_matriculas_salida(coches)
    actualizar_entradas(coches)

if __name__ == "__main__":
    main()
