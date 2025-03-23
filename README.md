# 🚗 Parking Inteligente con Azure Computer Vision

Este proyecto es una aplicación Python que simula la gestión de un parking inteligente utilizando **Azure Computer Vision** para detectar automáticamente las matrículas de los vehículos a partir de imágenes.

---

## 📌 ¿De qué trata?

El sistema automatiza el control de **entradas y salidas de vehículos** en un aparcamiento:

- Las imágenes de coches se colocan en carpetas (`entradas/` o `salidas/`).
- Azure analiza las imágenes y extrae las matrículas.
- Se registran fechas y horas de entrada/salida.
- Se calcula automáticamente el precio del estacionamiento (6€/hora completa).
- Se almacenan los datos en archivos `entradas.txt` y `salidas.txt`.

---

## 🛠️ Tecnologías utilizadas

- **Python 3**
- **Azure Computer Vision API** (OCR)
- **Librerías**:
  - `azure-cognitiveservices-vision-computervision`
  - `datetime`, `os`, `time`, `re`

---


