import os
import time
from datetime import datetime
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials

# Clave y endpoint de Azure
AZURE_KEY = "TU_CLAVE"
AZURE_ENDPOINT = "URL-ENDPOINT"

computervision_client = ComputerVisionClient(AZURE_ENDPOINT, CognitiveServicesCredentials(AZURE_KEY))

# ----------------------
# 1. Leer matrícula
# ----------------------
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
                    print(f"[Azure] Línea detectada: {word.text}")
                    if validar_matricula(texto):
                        print(f"[OK] Matrícula válida detectada: {texto}")
                        return texto
                    else:
                        print(f"[INFO] Línea descartada: {texto}")
        print("[WARNING] No se encontró ninguna matrícula válida.")
        return ''
    except Exception as e:
        print(f"[ERROR] en leer_matricula ({imagen}): {e}")
        return ''


def validar_matricula(m):
    import re
    return re.match(r'^\d{4}[A-Z]{3}$', m.replace(" ", "").replace("O", "0").replace("I", "1")) is not None

# ----------------------
# 2. Leer entradas existentes
# ----------------------
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

# ----------------------
# 3. Procesar imágenes de entrada
# ----------------------
def leer_matriculas_entrada(coches):
    print("🔍 Procesando imágenes en la carpeta 'entradas/'...")
    for fichero in os.listdir("entradas"):
        ruta = os.path.join("entradas", fichero)
        print(f"🛞 Procesando imagen de entrada: {fichero}")
        matricula = leer_matricula(ruta)
        if matricula:
            coches[matricula] = datetime.now()
            print(f"✅ Entrada registrada: {matricula}")
        else:
            print("⚠️ No se detectó matrícula válida.")
        os.remove(ruta)


# ----------------------
# 4. Procesar imágenes de salida
# ----------------------
def leer_matriculas_salida(coches):
    print("🔍 Procesando imágenes en la carpeta 'salidas/'...")
    for fichero in os.listdir("salidas"):
        ruta = os.path.join("salidas", fichero)
        print(f"🚗 Procesando imagen de salida: {fichero}")
        matricula = leer_matricula(ruta)
        salida = datetime.now()
        with open("salidas.txt", "a") as f:
            if matricula in coches:
                entrada = coches[matricula]
                horas = int((salida - entrada).total_seconds() // 3600)
                precio = horas * 6
                f.write(f"{matricula};{entrada.strftime('%d/%m/%Y %H:%M')};{salida.strftime('%d/%m/%Y %H:%M')};{precio}\n")
                print(f"💰 Salida registrada: {matricula} | {horas}h = {precio} €")
                del coches[matricula]
            else:
                f.write(f"{matricula};00/00/0000 00:00;{salida.strftime('%d/%m/%Y %H:%M')};100\n")
                print(f"❌ Matrícula no encontrada: {matricula} | Precio fijo 100 €")
        os.remove(ruta)


# ----------------------
# 5. Actualizar fichero de entradas
# ----------------------
def actualizar_entradas(coches):
    with open("entradas.txt", "w") as f:
        for matricula, fecha in coches.items():
            f.write(f"{matricula};{fecha.strftime('%d/%m/%Y %H:%M')}\n")

# ----------------------
# 6. Programa principal
# ----------------------
def main():
    print("🚦 Iniciando gestión del parking...")
    coches = leer_entradas()
    leer_matriculas_entrada(coches)
    leer_matriculas_salida(coches)
    actualizar_entradas(coches)
    print("✅ Programa finalizado.")


if __name__ == "__main__":
    main()
