# -*- coding: utf-8 -*-
"""
Visualizador Web de Resultados del Análisis de Premier League
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from flask import Flask, render_template_string, send_from_directory
import pandas as pd
import os
import pickle

app = Flask(__name__)

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Premier League Predictor - Resultados</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            padding: 20px;
            min-height: 100vh;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }

        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }

        h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }

        .subtitle {
            font-size: 1.2em;
            opacity: 0.9;
        }

        nav {
            background: #f8f9fa;
            padding: 15px 40px;
            border-bottom: 2px solid #e9ecef;
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }

        nav a {
            color: #667eea;
            text-decoration: none;
            padding: 10px 20px;
            border-radius: 8px;
            transition: all 0.3s;
            font-weight: 600;
        }

        nav a:hover {
            background: #667eea;
            color: white;
        }

        .content {
            padding: 40px;
        }

        .section {
            margin-bottom: 40px;
        }

        .section h2 {
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }

        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
            text-align: center;
        }

        .stat-value {
            font-size: 2.5em;
            font-weight: bold;
            margin: 10px 0;
        }

        .stat-label {
            font-size: 0.9em;
            opacity: 0.9;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }

        th {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }

        td {
            padding: 12px 15px;
            border-bottom: 1px solid #f0f0f0;
        }

        tr:hover {
            background: #f8f9fa;
        }

        .image-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 30px;
            margin: 20px 0;
        }

        .image-card {
            background: white;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }

        .image-card img {
            width: 100%;
            border-radius: 10px;
            margin-bottom: 15px;
        }

        .image-card h3 {
            color: #667eea;
            margin-bottom: 10px;
        }

        .badge {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
        }

        .badge-success {
            background: #28a745;
            color: white;
        }

        .badge-info {
            background: #17a2b8;
            color: white;
        }

        .badge-warning {
            background: #ffc107;
            color: #333;
        }

        footer {
            background: #f8f9fa;
            padding: 30px;
            text-align: center;
            color: #666;
            border-top: 2px solid #e9ecef;
        }

        .highlight {
            background: #fff3cd;
            padding: 2px 8px;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>⚽ Premier League Match Predictor</h1>
            <p class="subtitle">Análisis Completo con Machine Learning</p>
        </header>

        <nav>
            <a href="#summary">📊 Resumen</a>
            <a href="#teams">🏆 Equipos</a>
            <a href="#predictions">🎯 Predicciones</a>
            <a href="#models">🤖 Modelos</a>
            <a href="#visualizations">📈 Visualizaciones</a>
        </nav>

        <div class="content">
            <!-- RESUMEN -->
            <section id="summary" class="section">
                <h2>📊 Resumen del Proyecto</h2>
                <div class="stats-grid">
                    {% for _, row in summary.iterrows() %}
                    <div class="stat-card">
                        <div class="stat-label">{{ row['metric'] }}</div>
                        <div class="stat-value">{{ row['value'] }}</div>
                    </div>
                    {% endfor %}
                </div>
            </section>

            <!-- EQUIPOS -->
            <section id="teams" class="section">
                <h2>🏆 Análisis de Equipos (Top 10)</h2>
                <p style="margin-bottom: 20px;">Equipos ordenados por <span class="highlight">Team Score</span> (combinación de ataque, defensa y forma)</p>
                <table>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Equipo</th>
                            <th>Posición</th>
                            <th>Puntos</th>
                            <th>GF</th>
                            <th>GC</th>
                            <th>Ataque</th>
                            <th>Defensa</th>
                            <th>Forma</th>
                            <th>Team Score</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for idx, row in teams.head(10).iterrows() %}
                        <tr>
                            <td><strong>{{ loop.index }}</strong></td>
                            <td><strong>{{ row['name'] }}</strong></td>
                            <td>{{ row['position'] }}º</td>
                            <td><strong>{{ row['points'] }}</strong></td>
                            <td>{{ row['goalsFor'] }}</td>
                            <td>{{ row['goalsAgainst'] }}</td>
                            <td>{{ "%.2f"|format(row['attack_strength']) }}</td>
                            <td>{{ "%.2f"|format(row['defense_strength']) }}</td>
                            <td>{{ "%.2f"|format(row['form_score']) }}</td>
                            <td><strong>{{ "%.2f"|format(row['team_score']) }}</strong></td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </section>

            <!-- PREDICCIONES -->
            <section id="predictions" class="section">
                <h2>🎯 Predicciones de Partidos (10 ejemplos)</h2>
                <p style="margin-bottom: 20px;">Predicciones generadas por el modelo <span class="highlight">{{ predictions['model_used'].iloc[0] }}</span></p>
                <table>
                    <thead>
                        <tr>
                            <th>Equipo A</th>
                            <th>vs</th>
                            <th>Equipo B</th>
                            <th>Prob. A</th>
                            <th>Prob. B</th>
                            <th>Ganador</th>
                            <th>Confianza</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for idx, row in predictions.head(10).iterrows() %}
                        <tr>
                            <td><strong>{{ row['teamA'] }}</strong></td>
                            <td style="text-align: center;">⚔️</td>
                            <td><strong>{{ row['teamB'] }}</strong></td>
                            <td>{{ row['probA'] }}%</td>
                            <td>{{ row['probB'] }}%</td>
                            <td>
                                <span class="badge badge-success">{{ row['winner'] }}</span>
                            </td>
                            <td><strong>{{ row['confidence'] }}%</strong></td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </section>

            <!-- MODELOS -->
            <section id="models" class="section">
                <h2>🤖 Comparación de Modelos ML</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Modelo</th>
                            <th>Accuracy</th>
                            <th>Estado</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for idx, row in models.iterrows() %}
                        <tr>
                            <td><strong>{{ row['model'] }}</strong></td>
                            <td><strong>{{ "%.2f"|format(row['accuracy'] * 100) }}%</strong></td>
                            <td>
                                {% if row['best_model'] %}
                                <span class="badge badge-success">✅ MEJOR MODELO</span>
                                {% else %}
                                <span class="badge badge-info">Entrenado</span>
                                {% endif %}
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </section>

            <!-- VISUALIZACIONES -->
            <section id="visualizations" class="section">
                <h2>📈 Visualizaciones Generadas</h2>
                <div class="image-grid">
                    {% for image in images %}
                    <div class="image-card">
                        <img src="/outputs/{{ image }}" alt="{{ image }}">
                        <h3>{{ image.replace('.png', '').replace('_', ' ').title() }}</h3>
                    </div>
                    {% endfor %}
                </div>
            </section>
        </div>

        <footer>
            <p><strong>🎉 Análisis completado exitosamente</strong></p>
            <p style="margin-top: 10px;">Proyecto de Machine Learning - Premier League</p>
            <p style="margin-top: 20px; font-size: 0.9em;">
                📁 Archivos generados en: <code>outputs/</code>, <code>data/</code>, <code>models/</code>
            </p>
        </footer>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    # Cargar datos
    try:
        summary = pd.read_csv('outputs/project_summary.csv')
        teams = pd.read_csv('outputs/teams_analysis.csv').sort_values('team_score', ascending=False)
        predictions = pd.read_csv('outputs/match_predictions.csv')
        models = pd.read_csv('outputs/model_performance.csv').sort_values('accuracy', ascending=False)

        # Listar imágenes
        images = [f for f in os.listdir('outputs') if f.endswith('.png')]
        images.sort()

        return render_template_string(
            HTML_TEMPLATE,
            summary=summary,
            teams=teams,
            predictions=predictions,
            models=models,
            images=images
        )
    except Exception as e:
        return f"<h1>Error cargando datos:</h1><pre>{str(e)}</pre>"

@app.route('/outputs/<path:filename>')
def serve_output(filename):
    return send_from_directory('outputs', filename)

if __name__ == '__main__':
    print("="*80)
    print("🌐 SERVIDOR WEB INICIADO")
    print("="*80)
    print("\n📍 URL: http://127.0.0.1:5000")
    print("\n🔗 Abre esta URL en tu navegador para ver los resultados\n")
    print("="*80)
    print("\n⏸️  Presiona CTRL+C para detener el servidor\n")

    app.run(debug=True, port=5000, use_reloader=False)
