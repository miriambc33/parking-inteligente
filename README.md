# 🚗 Parking Inteligente con Azure Computer Vision

Este proyecto es una aplicación Python que simula la gestión de un parking inteligente utilizando **Azure Computer Vision** para detectar automáticamente las matrículas de los vehículos a partir de imágenes.

---

## 📌 ¿De qué trata?

El sistema automatiza el control de **entradas y salidas de vehículos** en un aparcamiento:

- Las imágenes de coches se colocan en carpetas (`entradas/` o `salidas/`).
- Azure analiza las imágenes y extrae las matrículas.
- Se registran fechas y horas de entrada/salida.
- Se calcula automáticamente el precio del estacionamiento (6 €/hora completa).
- Se almacenan los datos en archivos `entradas.txt` y `salidas.txt`.

---

## 🛠️ Tecnologías utilizadas

- **Python 3**
- **Azure Computer Vision API** (OCR)
- **Librerías**:
  - `azure-cognitiveservices-vision-computervision`
  - `datetime`, `os`, `time`, `re`

---

## 📂 Estructura del proyecto

```
parking-inteligente/
├── entradas/            # Imágenes de vehículos entrando
├── salidas/             # Imágenes de vehículos saliendo
├── entradas.txt         # Matrículas y horas de entrada
├── salidas.txt          # Registro de salidas y precios
├── main.py              # Código principal
└── README.md           
```

---

## ▶️ ¿Cómo ejecutar el proyecto?

### 1. Instalar dependencias

```bash
pip install azure-cognitiveservices-vision-computervision
```

### 2. Configurar claves de Azure

Crea un recurso "Computer Vision" en Azure. Luego, copia y pega tus credenciales en `main.py`:

```python
AZURE_KEY = "TU_CLAVE_DE_AZURE"
AZURE_ENDPOINT = "https://TUEndpoint.cognitiveservices.azure.com/"
```

---

## 🔄 Funcionamiento del sistema (muy importante)

### El programa debe ejecutarse en dos fases distintas:

#### 🚘 1. Fase de entrada:

- Coloca imágenes en la carpeta `entradas/`
- Ejecuta el programa:

```bash
python main.py
```

➡️ Se registrarán las matrículas y la hora de entrada en `entradas.txt`.

---

#### 🚗 2. Fase de salida (más tarde):

- Coloca imágenes en la carpeta `salidas/` (las mismas matrículas)
- Ejecuta el programa de nuevo:

```bash
python main.py
```

➡️ Se registrará la salida, se calculará el precio, y se guardará en `salidas.txt`.

📌 *Una vez registrada la salida, la matrícula se elimina del archivo `entradas.txt`, ya que el coche ha abandonado el parking.*

---

## 💰 Cálculo de precios

- 6 €/hora completa
- Si el coche no tiene registro de entrada, se cobra 100 €
- Se utiliza la diferencia entre las fechas de entrada y salida

---

## 🔐 Archivos generados

- `entradas.txt` → Coches que están **actualmente** en el parking
- `salidas.txt` → Registro completo de **coches que han salido** con fecha, hora y precio

---

## 🧠 Autoría

Proyecto desarrollado por **Miriam** como parte de la **Práctica – Programación de Inteligencia Artificial**.

