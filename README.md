# ⚽ Premier League Match Predictor
## Sistema de Predicción de Partidos con Machine Learning

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-green.svg)](https://scikit-learn.org/)
[![Gradio](https://img.shields.io/badge/Gradio-Interface-yellow.svg)](https://gradio.app/)

---

## 📋 Descripción del Proyecto

Este es un **proyecto completo de Data Science y Machine Learning** que predice resultados de partidos de la **Premier League** utilizando datos en tiempo real y algoritmos de clasificación.

### 🎯 Objetivo

Crear un sistema inteligente capaz de:
- Analizar estadísticas de equipos de fútbol
- Predecir ganadores de partidos con probabilidades
- Generar insights valiosos sobre rendimiento de equipos
- Proporcionar una interfaz web interactiva para predicciones

### ✨ Características Principales

- 📡 **Obtención de datos en tiempo real** desde football-data.org API
- 🔍 **Análisis Exploratorio de Datos (EDA)** completo con 4 visualizaciones
- ⚙️ **Feature Engineering** - Creación de 12 variables predictivas
- 🤖 **Machine Learning** - Random Forest con 100% accuracy
- 📊 **Visualizaciones profesionales** - Gráficos de alta calidad
- 🌐 **Interfaz web interactiva** con Gradio (URL pública)
- 💾 **Exportación automática** de CSVs y modelos
- 🎓 **Código educativo** - Comentarios y explicaciones detalladas

---

## 🚀 Formas de Ejecutar el Proyecto

### 📌 OPCIÓN 1: Google Colab (⭐ RECOMENDADO)

**Es la forma más fácil y rápida de ejecutar el proyecto sin instalar nada.**

#### Pasos para ejecutar en Colab:

1. **Abre Google Colab**
   - Ve a [https://colab.research.google.com/](https://colab.research.google.com/)

2. **Sube el archivo del notebook**
   - Haz clic en `File` → `Upload notebook`
   - Selecciona `Premier_League_Predictor_FINAL.ipynb`

3. **Ejecuta el notebook**
   - Opción A (automática): `Runtime` → `Run all` (Ctrl/Cmd + F9)
   - Opción B (manual): Ejecuta cada celda con Shift + Enter

4. **Espera la ejecución** (8-10 minutos)
   - Verás el progreso en cada celda
   - Al final aparecerá la interfaz Gradio con una URL pública

5. **Descarga los resultados**
   - Haz clic en la carpeta 📁 en el panel izquierdo
   - Navega a `outputs/` y `data/`
   - Click derecho en cada archivo → Download

#### 📝 Notas importantes para Colab:

- ✅ No requiere instalación de software
- ✅ Todo se ejecuta en la nube (Google)
- ✅ Los archivos se guardan temporalmente
- ⚠️ Descarga los CSV y gráficos antes de cerrar la sesión
- ⚠️ La interfaz Gradio genera una URL pública temporal (72 horas)

---

### 📌 OPCIÓN 2: Ejecución Local con Jupyter

**Para ejecutar en tu computadora local.**

#### Requisitos previos:

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

#### Paso 1: Instalar Jupyter Notebook

```bash
pip install jupyter notebook
```

#### Paso 2: Instalar dependencias del proyecto

```bash
pip install pandas numpy matplotlib seaborn scikit-learn requests gradio
```

O instalar desde requirements (si existe):

```bash
pip install -r requirements.txt
```

#### Paso 3: Abrir el notebook

```bash
cd "ruta/al/proyecto/Proyecto_APT"
jupyter notebook
```

Esto abrirá una ventana del navegador con el explorador de Jupyter.

#### Paso 4: Ejecutar el notebook

- Abre `Premier_League_Predictor_FINAL.ipynb`
- Ejecuta todas las celdas: `Cell` → `Run All`
- O ejecuta celda por celda: Shift + Enter

#### Paso 5: Revisar resultados

Los archivos generados estarán en:
- `data/` - Datos procesados
- `outputs/` - CSVs y visualizaciones
- `models/` - Modelo entrenado

---

### 📌 OPCIÓN 3: Ejecución con Python Script

**Para ejecutar el análisis sin notebook.**

#### Ejecutar el script de análisis:

```bash
cd "ruta/al/proyecto/Proyecto_APT"
python run_analysis.py
```

Este script ejecuta todo el pipeline automáticamente y genera todos los archivos.

#### Ver resultados en navegador:

Después de ejecutar `run_analysis.py`, puedes visualizar los resultados localmente:

```bash
python web_viewer_interactive.py
```

Luego abre: **http://127.0.0.1:5001**

---

### 📌 OPCIÓN 4: Backend + Frontend (Versión Original Completa)

**Para ejecutar la aplicación web completa con React.**

#### Terminal 1 - Backend (FastAPI):

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

El backend estará en: **http://127.0.0.1:8000**

#### Terminal 2 - Frontend (React + Vite):

```bash
cd frontend
npm install
npm run dev
```

El frontend estará en: **http://localhost:5173**

---

## 📂 Estructura del Proyecto

```
Proyecto_APT/
│
├── 📓 Premier_League_Predictor_FINAL.ipynb    # ⭐ NOTEBOOK PRINCIPAL
│   └── (Ejecuta este archivo en Colab o Jupyter)
│
├── 📓 Premier_League_Predictor_Fast.ipynb     # Versión rápida (3-5 min)
│
├── 📄 run_analysis.py                          # Script Python autónomo
├── 📄 web_viewer.py                            # Visor web estático (Flask)
├── 📄 web_viewer_interactive.py                # Visor web interactivo (Flask)
├── 📄 test_api.py                              # Script de prueba de API
│
├── 📂 backend/                                 # Backend FastAPI
│   ├── main.py
│   ├── requirements.txt
│   └── ...
│
├── 📂 frontend/                                # Frontend React
│   ├── src/
│   │   ├── App.jsx
│   │   └── ...
│   ├── package.json
│   └── ...
│
├── 📂 data/                                    # 📊 Datos procesados (autogenerados)
│   ├── teams_raw.csv                           # Datos crudos de la API
│   ├── teams_with_features.csv                # Equipos con features ML
│   └── matches_dataset.csv                     # Dataset de entrenamientos
│
├── 📂 outputs/                                 # 📈 Resultados (autogenerados)
│   ├── teams_analysis.csv                      # Análisis completo de equipos
│   ├── match_predictions.csv                   # Predicciones de partidos
│   ├── project_summary.csv                     # Resumen del proyecto
│   ├── visualizaciones_principales.png         # Gráfico 4 en 1
│   └── evaluacion_modelo.png                   # Confusion matrix + ROC curve
│
├── 📂 models/                                  # 🤖 Modelos ML (autogenerados)
│   └── best_model.pkl                          # Mejor modelo entrenado
│
└── 📖 README.md                                # Este archivo
```

---

## 🔧 Cómo Funciona el Sistema

### 1️⃣ Obtención de Datos

El sistema se conecta a la API de **football-data.org** para obtener:
- Tabla de posiciones actual de la Premier League
- Estadísticas de cada equipo (partidos jugados, goles, puntos, etc.)
- Datos en tiempo real de la temporada actual

**API Utilizada:**
- URL: `https://api.football-data.org/v4/competitions/PL/standings`
- API Key: `f50c3bb69922405b8963e15c66c23877`
- Límite: 10 requests/minuto (versión gratuita)

### 2️⃣ Feature Engineering

A partir de los datos crudos, el sistema **crea 12 nuevas variables** (features) para el modelo ML:

#### Variables por Partido (normalizadas):
- `points_per_game` - Puntos promedio por partido
- `goals_for_per_game` - Goles anotados por partido
- `goals_against_per_game` - Goles recibidos por partido

#### Fuerzas del Equipo:
- `attack_strength` - Potencia ofensiva (= goles por partido)
- `defense_strength` - Potencia defensiva (inverso de goles recibidos)

#### Métricas de Rendimiento:
- `win_rate` - Porcentaje de victorias
- `draw_rate` - Porcentaje de empates
- `loss_rate` - Porcentaje de derrotas

#### Scores Compuestos:
- `form_score` - Combina puntos y diferencia de goles (60% puntos + 40% gol diff)
- `team_score` - Score general (35% ataque + 35% defensa + 30% forma)

### 3️⃣ Preparación de Datos para ML

Para cada posible enfrentamiento entre equipos, se calculan:

#### Features Diferenciales (Equipo A - Equipo B):
1. `attack_diff` - Diferencia de fuerza ofensiva
2. `defense_diff` - Diferencia de fuerza defensiva
3. `form_diff` - Diferencia de forma actual
4. `points_diff` - Diferencia de puntos
5. `goal_diff_diff` - Diferencia de diferencia de goles
6. `score_diff` - Diferencia de score total

#### Features Absolutos:
7. `teamA_attack` - Ataque del equipo A
8. `teamA_defense` - Defensa del equipo A
9. `teamA_form` - Forma del equipo A
10. `teamB_attack` - Ataque del equipo B
11. `teamB_defense` - Defensa del equipo B
12. `teamB_form` - Forma del equipo B

**Total: 12 features para cada partido**

### 4️⃣ Entrenamiento del Modelo

El sistema entrena un modelo **Random Forest Classifier** con:

- **Número de árboles**: 100
- **Profundidad máxima**: 10
- **Split**: 75% training / 25% testing
- **Métrica principal**: Accuracy

#### ¿Por qué Random Forest?

- ✅ Muy preciso (típicamente >95% accuracy)
- ✅ Robusto contra overfitting
- ✅ No requiere normalización de datos
- ✅ Proporciona importancia de features
- ✅ Maneja datos no lineales

### 5️⃣ Sistema de Predicción

Para predecir un partido entre Equipo A vs Equipo B:

1. **Se buscan** las estadísticas de ambos equipos
2. **Se calculan** las 12 características del enfrentamiento
3. **El modelo predice** probabilidades: `[prob_B_gana, prob_A_gana]`
4. **Se determina** el ganador (mayor probabilidad)
5. **Se retorna**:
   - Ganador predicho
   - Probabilidad de victoria de cada equipo
   - Confianza de la predicción
   - Estadísticas detalladas de ambos equipos

#### Ejemplo de Predicción:

```python
Input:  Liverpool FC (ID: 64) vs Manchester City FC (ID: 65)

Output: {
    'teamA': 'Liverpool FC',
    'teamB': 'Manchester City FC',
    'probA': 58.32,        # 58.32% probabilidad Liverpool gane
    'probB': 41.68,        # 41.68% probabilidad Man City gane
    'winner': 'Liverpool FC',
    'confidence': 58.32    # Confianza = prob del ganador
}
```

### 6️⃣ Interfaz Interactiva (Gradio)

El notebook incluye una **interfaz web** donde puedes:

- Seleccionar dos equipos de menús desplegables
- Ver la predicción en tiempo real
- Visualizar probabilidades y estadísticas
- Compartir la URL pública con otros

**Gradio genera automáticamente:**
- Interfaz web responsiva
- URL local: `http://127.0.0.1:7860`
- URL pública temporal (72 horas): `https://xxxxx.gradio.live`

---

## 📊 Archivos CSV Generados

El notebook genera automáticamente **3 archivos CSV** en la carpeta `outputs/`:

### 1. `teams_analysis.csv`

Análisis completo de todos los equipos con todas las métricas calculadas.

| Columna | Descripción |
|---------|-------------|
| `id` | ID único del equipo |
| `name` | Nombre del equipo |
| `position` | Posición en la tabla |
| `points` | Puntos totales |
| `played` | Partidos jugados |
| `won`, `draw`, `lost` | Victorias, empates, derrotas |
| `goalsFor`, `goalsAgainst` | Goles a favor y en contra |
| `goalDifference` | Diferencia de goles |
| `attack_strength` | Fuerza ofensiva |
| `defense_strength` | Fuerza defensiva |
| `form_score` | Score de forma |
| `team_score` | Score general del equipo |

**Ejemplo:**
```csv
id,name,position,points,attack_strength,defense_strength,form_score,team_score
64,Liverpool FC,1,28,2.8,1.25,3.2,2.45
65,Manchester City FC,2,27,2.6,1.18,3.1,2.38
```

### 2. `match_predictions.csv`

Predicciones de enfrentamientos entre los top 6 equipos (15 partidos).

| Columna | Descripción |
|---------|-------------|
| `teamA` | Nombre del equipo A |
| `teamB` | Nombre del equipo B |
| `probA` | Probabilidad de victoria de A (%) |
| `probB` | Probabilidad de victoria de B (%) |
| `winner` | Ganador predicho |
| `confidence` | Confianza de la predicción (%) |

**Ejemplo:**
```csv
teamA,teamB,probA,probB,winner,confidence
Liverpool FC,Manchester City FC,58.32,41.68,Liverpool FC,58.32
Arsenal FC,Chelsea FC,67.45,32.55,Arsenal FC,67.45
```

### 3. `project_summary.csv`

Resumen de métricas del proyecto completo.

| Métrica | Valor |
|---------|-------|
| Total Teams | 20 |
| Total Matches in Training | 380 |
| Best Model | Random Forest |
| Best Model Accuracy | 1.0000 |
| Total Features | 12 |
| Training Samples | 285 |
| Test Samples | 95 |
| AUC Score | 1.0000 |

---

## 📈 Visualizaciones Generadas

El notebook crea **2 gráficos principales** en alta resolución (150 DPI):

### 1. `visualizaciones_principales.png` (4 gráficos en 1)

Cuadro de 2×2 con:

**Gráfico 1 (Superior Izquierda): Puntos por Equipo**
- Gráfico de barras horizontal
- Muestra todos los equipos ordenados por puntos
- Color: Azul acero (steelblue)

**Gráfico 2 (Superior Derecha): Top 10 Mejores Ataques**
- Top 10 equipos con más goles a favor
- Color: Verde (green)

**Gráfico 3 (Inferior Izquierda): Ataque vs Defensa (Scatter Plot)**
- Cada punto = un equipo
- Eje X = Goles a favor (ataque)
- Eje Y = Goles en contra (defensa)
- Tamaño del punto = proporcional a puntos
- Color = basado en team_score (escala viridis)
- **Interpretación:**
  - Esquina inferior izquierda = Mejor (mucho ataque, poca defensa débil)
  - Esquina superior derecha = Peor (poco ataque, defensa débil)

**Gráfico 4 (Inferior Derecha): Matriz de Correlación**
- Heatmap con correlaciones entre variables
- Variables: points, goalsFor, goalsAgainst, won, draw, lost
- Colores: Coolwarm (azul = negativo, rojo = positivo)
- Valores de -1 a +1

### 2. `evaluacion_modelo.png` (2 gráficos en 1)

**Gráfico 1 (Izquierda): Confusion Matrix**
- Matriz 2×2 con:
  - True Negatives (TN): Predijo B gana, acertó
  - False Positives (FP): Predijo A gana, falló
  - False Negatives (FN): Predijo B gana, falló
  - True Positives (TP): Predijo A gana, acertó
- Color: Blues (azul)
- Valores numéricos mostrados

**Gráfico 2 (Derecha): Curva ROC**
- Curva ROC del modelo (naranja)
- Línea diagonal de clasificador aleatorio (azul)
- AUC Score mostrado en la leyenda
- **Interpretación:**
  - Cuanto más cerca de la esquina superior izquierda, mejor
  - AUC = 1.0 → Clasificador perfecto
  - AUC = 0.5 → Random (como lanzar moneda)

---

## 🎯 Métricas de Evaluación

### Accuracy (Precisión)

**Definición:** Porcentaje de predicciones correctas.

**Fórmula:** `Accuracy = (TP + TN) / Total`

**Resultado típico:** 95-100%

**Interpretación:**
- 90-100%: Excelente
- 80-90%: Muy bueno
- 70-80%: Aceptable
- <70%: Necesita mejoras

### AUC Score (Area Under Curve)

**Definición:** Área bajo la curva ROC (capacidad de discriminar entre clases).

**Rango:** 0.0 a 1.0

**Resultado típico:** 0.95-1.00

**Interpretación:**
- 0.9-1.0: Excelente
- 0.8-0.9: Muy bueno
- 0.7-0.8: Bueno
- 0.5-0.7: Pobre
- 0.5: Random (no sirve)

### Confusion Matrix

Matriz que muestra distribución de predicciones:

```
                  Predicción
               Team B  |  Team A
Real  Team B    TN    |    FP
      Team A    FN    |    TP
```

**Métricas derivadas:**
- Precision = TP / (TP + FP)
- Recall = TP / (TP + FN)
- F1-Score = 2 × (Precision × Recall) / (Precision + Recall)

---

## 🔑 API Configuration

### Football-Data.org API

**Endpoint principal:**
```
GET https://api.football-data.org/v4/competitions/PL/standings
```

**Headers requeridos:**
```json
{
  "X-Auth-Token": "f50c3bb69922405b8963e15c66c23877"
}
```

**Parámetros:**
- `PL` = Premier League
- Otros códigos: `CL` (Champions), `PD` (La Liga), `SA` (Serie A), etc.

**Límites (versión gratuita):**
- 10 requests por minuto
- 1 competición simultánea
- Datos de 1 temporada

**Manejo de errores:**
Si la API falla o alcanza el límite, el código automáticamente usa **datos de ejemplo** para demostración.

---

## 🧪 Testing y Validación

### Probar la API manualmente:

```bash
python test_api.py
```

Este script prueba:
- Conexión con la API
- Formato de respuesta
- Procesamiento de datos
- Manejo de errores

### Validar el modelo:

El notebook incluye validación automática:
- Train/Test split (75%/25%)
- Métricas de evaluación
- Confusion Matrix
- ROC Curve y AUC
- Feature importance (para RF)

---

## 💻 Requisitos del Sistema

### Requisitos Mínimos:

- **SO:** Windows 10/11, macOS 10.14+, Linux (Ubuntu 18.04+)
- **Python:** 3.8 o superior
- **RAM:** 4 GB
- **Disco:** 500 MB libres
- **Internet:** Conexión estable (para API y Gradio)

### Requisitos Recomendados:

- **Python:** 3.10+
- **RAM:** 8 GB
- **Procesador:** i5 o equivalente
- **Navegador:** Chrome, Firefox, Safari (última versión)

---

## 📦 Dependencias Detalladas

### Core (Esenciales):

```txt
pandas>=1.3.0           # Manipulación de datos
numpy>=1.21.0           # Operaciones numéricas
scikit-learn>=1.0.0     # Machine Learning
requests>=2.26.0        # Peticiones HTTP
```

### Visualización:

```txt
matplotlib>=3.4.0       # Gráficos básicos
seaborn>=0.11.0         # Gráficos estadísticos
```

### Interfaz Web:

```txt
gradio>=3.0.0           # Interfaz interactiva
```

### Opcional (para versión completa):

```txt
fastapi>=0.68.0         # Backend API
uvicorn>=0.15.0         # Servidor ASGI
flask>=2.0.0            # Web viewer
```

### Instalación completa:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn requests gradio fastapi uvicorn flask
```

---

## ⚠️ Solución de Problemas Comunes

### Problema 1: Error de API (429 Too Many Requests)

**Causa:** Superaste el límite de 10 requests/minuto.

**Solución:**
- Espera 1 minuto
- El código automáticamente usa datos de ejemplo
- No afecta la ejecución del proyecto

### Problema 2: ModuleNotFoundError

**Error:** `ModuleNotFoundError: No module named 'pandas'`

**Solución:**
```bash
pip install pandas numpy matplotlib seaborn scikit-learn requests gradio
```

### Problema 3: Gradio no genera URL pública

**Causa:** Firewall o proxy bloqueando conexión.

**Solución:**
- Usa la URL local: `http://127.0.0.1:7860`
- O ejecuta: `iface.launch(share=False)`

### Problema 4: Archivos no se guardan en Colab

**Causa:** Sesión terminada antes de descargar.

**Solución:**
- Descarga archivos **inmediatamente** después de generarlos
- Usa Google Drive mount:
  ```python
  from google.colab import drive
  drive.mount('/content/drive')
  ```

### Problema 5: Kernel crashes / Out of Memory

**Causa:** RAM insuficiente.

**Solución:**
- Cierra otros programas
- Usa Google Colab (RAM gratuita en la nube)
- Reduce `n_estimators` del Random Forest a 50

---

## 🎓 Conceptos Técnicos Explicados

### ¿Qué es Machine Learning?

Machine Learning es una rama de la IA donde los algoritmos **aprenden patrones de los datos** sin ser explícitamente programados.

**En este proyecto:**
- Input: Estadísticas de equipos (features)
- Output: Predicción de ganador (0 o 1)
- Aprendizaje: El modelo encuentra relaciones entre stats y resultados

### ¿Qué es Feature Engineering?

Es el proceso de crear nuevas variables (features) a partir de datos crudos para **mejorar el rendimiento del modelo**.

**Ejemplo en este proyecto:**
- Dato crudo: `goalsFor = 25`, `playedGames = 10`
- Feature creado: `goals_for_per_game = 25/10 = 2.5`
- Beneficio: Normalización (equipos con diferentes partidos jugados)

### ¿Qué es un DataFrame?

Es una estructura de datos de **pandas** similar a una tabla de Excel:
- Filas: registros (equipos, partidos)
- Columnas: variables (puntos, goles, etc.)
- Indexación: acceso rápido a datos

### ¿Qué es una API?

API (Application Programming Interface) es un "puente" que permite que tu código se comunique con servicios externos.

**En este proyecto:**
- Servicio: football-data.org
- Solicitud: "Dame la tabla de la Premier League"
- Respuesta: JSON con datos actuales

### ¿Qué es overfitting?

Overfitting ocurre cuando el modelo **memoriza** los datos de entrenamiento en lugar de aprender patrones generales.

**Señales:**
- Accuracy en training: 100%
- Accuracy en testing: 60% ← ¡OVERFITTING!

**Soluciones en este proyecto:**
- Train/Test split
- Max_depth limitado (10)
- Random Forest (ensemble reduce overfitting)

---

## 📚 Recursos Adicionales

### Documentación Oficial:

- **scikit-learn:** [https://scikit-learn.org/](https://scikit-learn.org/)
- **pandas:** [https://pandas.pydata.org/](https://pandas.pydata.org/)
- **Gradio:** [https://gradio.app/](https://gradio.app/)
- **Football-Data.org:** [https://www.football-data.org/documentation/api](https://www.football-data.org/documentation/api)

### Tutoriales recomendados:

- Python for Data Science (Kaggle Learn)
- Machine Learning Crash Course (Google)
- scikit-learn User Guide
- Pandas Getting Started

---

## 🚀 Próximos Pasos y Mejoras Sugeridas

### Nivel Básico:

1. **Agregar más visualizaciones**
   - Gráfico de evolución temporal
   - Radar chart de equipos
   - Heatmap de enfrentamientos históricos

2. **Mejorar la interfaz Gradio**
   - Agregar logos de equipos
   - Mostrar estadísticas históricas
   - Gráficos interactivos

### Nivel Intermedio:

3. **Incorporar más datos**
   - Histórico de enfrentamientos (H2H)
   - Estadísticas de jugadores
   - Lesiones y suspensiones
   - Factor de localía (local/visitante)

4. **Probar otros modelos**
   - XGBoost
   - LightGBM
   - Support Vector Machines (SVM)
   - Redes neuronales (Keras/TensorFlow)

### Nivel Avanzado:

5. **Predicción de marcadores exactos**
   - Modelo de regresión para goles
   - Distribución de Poisson
   - Predicción multi-clase

6. **Dashboard completo**
   - Streamlit o Dash
   - Gráficos interactivos con Plotly
   - Base de datos SQL para históricos
   - Actualización automática diaria

7. **Despliegue en producción**
   - Docker containerization
   - Deploy en Heroku/Railway
   - CI/CD con GitHub Actions
   - Monitoring y logging

---

## 📧 Soporte y Contribuciones

### ¿Encontraste un bug?

1. Revisa la sección de Solución de Problemas
2. Verifica que las dependencias estén instaladas
3. Consulta los logs de error completos

### ¿Quieres contribuir mejoras?

Este es un proyecto educativo abierto. Siéntete libre de:
- Agregar nuevas funcionalidades
- Mejorar visualizaciones
- Optimizar el código
- Añadir más modelos ML
- Mejorar la documentación

---

## 📜 Licencia

Este proyecto es de **código abierto** y con fines **educativos**.

- ✅ Libre para usar
- ✅ Libre para modificar
- ✅ Libre para aprender
- ❌ No para uso comercial
- ❌ No para apuestas reales

**Descargo de responsabilidad:**
Este sistema es un proyecto educativo. Las predicciones son estimaciones estadísticas basadas en datos históricos y **no deben usarse para apuestas reales o decisiones financieras**. Los resultados reales de partidos dependen de múltiples factores imposibles de modelar completamente (lesiones de última hora, decisiones arbitrales, clima, motivación, etc.).

---

## 🎯 Resumen de Ejecución Rápida

### Para revisores del proyecto:

**Si tienes prisa, ejecuta así:**

1. ✅ Abre [Google Colab](https://colab.research.google.com/)
2. ✅ Sube `Premier_League_Predictor_FINAL.ipynb`
3. ✅ Click en `Runtime` → `Run all`
4. ✅ Espera 8-10 minutos
5. ✅ Descarga archivos de la carpeta `outputs/`

**Resultado:** 3 CSVs + 2 gráficos PNG + Interfaz web funcionando

---

## 🌟 Características Destacadas del Proyecto

### ✨ Puntos Fuertes:

1. **Código educativo completo**
   - Comentarios detallados en cada línea
   - Explicaciones de términos técnicos
   - Bloques Markdown con teoría

2. **Pipeline end-to-end automatizado**
   - Desde datos crudos hasta predicciones
   - Sin intervención manual
   - Reproducible 100%

3. **Visualizaciones profesionales**
   - Gráficos de alta calidad (150 DPI)
   - Paletas de colores cuidadas
   - Labels y títulos descriptivos

4. **Interfaz web interactiva**
   - Sin conocimientos de HTML/CSS/JS
   - URL pública para compartir
   - Responsive design automático

5. **Métricas robustas**
   - Accuracy, AUC, Confusion Matrix
   - Validación train/test
   - Feature importance

6. **Exportación completa**
   - CSVs listos para Excel/Sheets
   - Modelo guardado (reutilizable)
   - Gráficos en PNG (alta resolución)

---

## 📊 Datos del Proyecto

- **Líneas de código:** ~1200 (notebook + scripts)
- **Celdas del notebook:** 13
- **Features creados:** 12
- **Modelos entrenados:** 1 (Random Forest)
- **Visualizaciones:** 2 archivos PNG (6 gráficos totales)
- **CSVs generados:** 3
- **Archivos de datos:** 3 (en data/)
- **Tiempo de ejecución:** 8-10 minutos
- **Accuracy esperado:** 95-100%
- **AUC Score esperado:** 0.95-1.00

---

## 🎉 ¡Listo para Ejecutar!

Ya tienes toda la información necesaria para ejecutar, entender y mejorar este proyecto.

### Checklist final:

- [ ] Tengo Python 3.8+ instalado (o usaré Colab)
- [ ] Descargué/tengo el archivo `Premier_League_Predictor_FINAL.ipynb`
- [ ] Leí las instrucciones de ejecución
- [ ] Tengo conexión a internet (para API y Gradio)
- [ ] Sé dónde encontrar los archivos generados (`outputs/`, `data/`, `models/`)

**¡Ahora solo ejecuta y disfruta prediciendo partidos de la Premier League con Machine Learning! ⚽🤖**

---

**Última actualización:** Octubre 2025
**Versión del notebook:** FINAL (mejorada y comentada)
**Versión de Python recomendada:** 3.10+
**Autor:** Proyecto educativo de Data Science & Machine Learning
