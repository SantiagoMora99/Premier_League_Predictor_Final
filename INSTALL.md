# 📦 Guía de Instalación - Premier League Predictor

Esta guía te ayudará a configurar el proyecto en tu máquina local después de hacer `git clone`.

## 📋 Prerequisitos

- Python 3.8 o superior
- Node.js 16 o superior (para el frontend)
- Git

## 🚀 Pasos de Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
cd TU_REPOSITORIO
```

### 2. Configurar Python (Backend y Scripts)

#### Crear entorno virtual (recomendado):
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### Instalar dependencias Python:
```bash
pip install -r requirements.txt
```

#### Instalar dependencias del backend:
```bash
cd backend
pip install -r requirements.txt
cd ..
```

### 3. Configurar Frontend (React)

```bash
cd frontend
npm install
cd ..
```

### 4. Generar Datos y Modelos

Como los modelos y datos no están en el repositorio (son archivos grandes), necesitas generarlos:

#### Opción A: Ejecutar el notebook completo
```bash
# Instalar Jupyter
pip install jupyter

# Ejecutar el notebook
jupyter notebook Premier_League_Predictor_FINAL.ipynb
```
Ejecuta todas las celdas para generar:
- `data/*.csv` (datos procesados)
- `models/*.pkl` (modelos entrenados)
- `outputs/*.csv` y `outputs/*.png` (resultados)

#### Opción B: Ejecutar el script Python
```bash
python run_analysis.py
```

### 5. Verificar la Instalación

Verifica que se hayan creado las siguientes carpetas con archivos:
- `data/` (con CSVs de datos)
- `models/` (con archivos .pkl de modelos)
- `outputs/` (con CSVs y PNGs)

## 🎯 Ejecutar el Proyecto

### Opción 1: Web Viewer Interactivo (Recomendado)
```bash
python web_viewer_interactive.py
```
Abre http://127.0.0.1:5001 en tu navegador

### Opción 2: Backend + Frontend Separados

**Terminal 1 - Backend (FastAPI):**
```bash
cd backend
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**Terminal 2 - Frontend (React):**
```bash
cd frontend
npm run dev
```
Abre http://localhost:5173 en tu navegador

### Opción 3: Google Colab
1. Sube `Premier_League_Predictor_FINAL.ipynb` a Google Colab
2. Ejecuta todas las celdas
3. Usa la interfaz Gradio generada

## ⚠️ Solución de Problemas

### Error: "No module named 'pandas'"
```bash
pip install -r requirements.txt
```

### Error: "best_model.pkl not found"
Necesitas generar los modelos primero:
```bash
python run_analysis.py
```

### Error: "API key invalid"
La API key en el código es pública y gratuita. Si no funciona, obtén una nueva en:
https://www.football-data.org/client/register

### Frontend no inicia
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

## 📚 Más Información

Consulta el [README.md](README.md) principal para documentación completa del proyecto.

## 🤝 Contribuir

Si encuentras errores o quieres mejorar el proyecto, siéntete libre de abrir un Issue o Pull Request.
