# -*- coding: utf-8 -*-
"""
Visualizador Web INTERACTIVO de Resultados - Premier League
Con selector de equipos para predicciones en vivo
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from flask import Flask, render_template_string, send_from_directory, request, jsonify
import pandas as pd
import os
import pickle

app = Flask(__name__)

# Cargar datos globales
df_features = pd.read_csv('data/teams_with_features.csv')
with open('models/best_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Función de predicción
def predict_match(team_a_id, team_b_id):
    team_a = df_features[df_features['id'] == team_a_id].iloc[0]
    team_b = df_features[df_features['id'] == team_b_id].iloc[0]

    # Crear el match con las MISMAS 12 características que se usaron en el entrenamiento
    match = pd.DataFrame([{
        'attack_diff': team_a['attack_strength'] - team_b['attack_strength'],
        'defense_diff': team_a['defense_strength'] - team_b['defense_strength'],
        'form_diff': team_a['form_score'] - team_b['form_score'],
        'points_diff': team_a['points'] - team_b['points'],
        'goal_diff_diff': team_a['goalDifference'] - team_b['goalDifference'],
        'teamA_attack': team_a['attack_strength'],
        'teamA_defense': team_a['defense_strength'],
        'teamA_form': team_a['form_score'],
        'teamB_attack': team_b['attack_strength'],
        'teamB_defense': team_b['defense_strength'],
        'teamB_form': team_b['form_score'],
        'score_diff': team_a['team_score'] - team_b['team_score'],
    }])

    proba = model.predict_proba(match)[0]
    prob_b, prob_a = proba[0] * 100, proba[1] * 100

    return {
        'teamA': team_a['name'],
        'teamB': team_b['name'],
        'probA': round(prob_a, 2),
        'probB': round(prob_b, 2),
        'winner': team_a['name'] if prob_a > prob_b else team_b['name'],
        'confidence': round(max(prob_a, prob_b), 2),
        'teamA_stats': {
            'attack': round(team_a['attack_strength'], 2),
            'defense': round(team_a['defense_strength'], 2),
            'form': round(team_a['form_score'], 2),
            'score': round(team_a['team_score'], 2)
        },
        'teamB_stats': {
            'attack': round(team_b['attack_strength'], 2),
            'defense': round(team_b['defense_strength'], 2),
            'form': round(team_b['form_score'], 2),
            'score': round(team_b['team_score'], 2)
        }
    }

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Premier League Predictor - Interactivo</title>
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

        .predictor-section {
            padding: 40px;
            background: #f8f9fa;
            border-bottom: 2px solid #e9ecef;
        }

        .predictor-title {
            color: #667eea;
            margin-bottom: 30px;
            text-align: center;
            font-size: 2em;
        }

        .team-selector {
            display: grid;
            grid-template-columns: 1fr auto 1fr;
            gap: 20px;
            align-items: center;
            margin-bottom: 30px;
        }

        .team-box {
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }

        .team-box label {
            display: block;
            margin-bottom: 10px;
            font-weight: 600;
            color: #667eea;
            font-size: 1.1em;
        }

        .team-box select {
            width: 100%;
            padding: 15px;
            border: 2px solid #667eea;
            border-radius: 10px;
            font-size: 1em;
            background: white;
            cursor: pointer;
            transition: all 0.3s;
        }

        .team-box select:hover {
            border-color: #764ba2;
            box-shadow: 0 0 10px rgba(102, 126, 234, 0.3);
        }

        .vs-text {
            font-size: 3em;
            font-weight: bold;
            color: #667eea;
            text-align: center;
        }

        .predict-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 20px 60px;
            font-size: 1.3em;
            border-radius: 50px;
            cursor: pointer;
            display: block;
            margin: 0 auto;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
            transition: all 0.3s;
            font-weight: 600;
        }

        .predict-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
        }

        .predict-btn:active {
            transform: translateY(-1px);
        }

        .result-container {
            margin-top: 30px;
            display: none;
        }

        .result-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
        }

        .result-header {
            text-align: center;
            margin-bottom: 30px;
        }

        .result-header h2 {
            font-size: 2em;
            margin-bottom: 10px;
        }

        .matchup {
            font-size: 1.5em;
            opacity: 0.9;
        }

        .winner-section {
            background: rgba(255, 255, 255, 0.2);
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 30px;
        }

        .winner-label {
            font-size: 1.2em;
            margin-bottom: 10px;
            opacity: 0.9;
        }

        .winner-name {
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 15px;
        }

        .confidence {
            font-size: 1.5em;
        }

        .probabilities {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }

        .prob-box {
            background: rgba(255, 255, 255, 0.15);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
        }

        .prob-team {
            font-size: 1.3em;
            font-weight: 600;
            margin-bottom: 10px;
        }

        .prob-value {
            font-size: 2.5em;
            font-weight: bold;
        }

        .stats-section {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
        }

        .team-stats {
            background: rgba(255, 255, 255, 0.1);
            padding: 25px;
            border-radius: 15px;
        }

        .team-stats h3 {
            font-size: 1.5em;
            margin-bottom: 20px;
            text-align: center;
        }

        .stat-row {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        }

        .stat-label {
            opacity: 0.9;
        }

        .stat-value {
            font-weight: bold;
            font-size: 1.1em;
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

        .loading {
            display: none;
            text-align: center;
            margin-top: 20px;
            font-size: 1.2em;
            color: #667eea;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .spinner {
            display: inline-block;
            width: 40px;
            height: 40px;
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>⚽ Premier League Match Predictor</h1>
            <p class="subtitle">Predicción Interactiva con Machine Learning</p>
        </header>

        <div class="predictor-section">
            <h2 class="predictor-title">🎯 Predice el Resultado</h2>

            <div class="team-selector">
                <div class="team-box">
                    <label for="teamA">🔵 Equipo A</label>
                    <select id="teamA">
                        <option value="">Selecciona un equipo</option>
                        {% for _, row in teams.iterrows() %}
                        <option value="{{ row['id'] }}">{{ row['name'] }}</option>
                        {% endfor %}
                    </select>
                </div>

                <div class="vs-text">VS</div>

                <div class="team-box">
                    <label for="teamB">🔴 Equipo B</label>
                    <select id="teamB">
                        <option value="">Selecciona un equipo</option>
                        {% for _, row in teams.iterrows() %}
                        <option value="{{ row['id'] }}">{{ row['name'] }}</option>
                        {% endfor %}
                    </select>
                </div>
            </div>

            <button class="predict-btn" onclick="predictMatch()">🔮 Predecir Resultado</button>

            <div class="loading" id="loading">
                <div class="spinner"></div>
                <div>Analizando equipos...</div>
            </div>

            <div class="result-container" id="result">
                <!-- Resultado dinámico aquí -->
            </div>
        </div>

        <div class="content">
            <section class="section">
                <h2>🏆 Equipos Disponibles (Top 10)</h2>
                <table>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Equipo</th>
                            <th>Posición</th>
                            <th>Puntos</th>
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
                            <td>{{ "%.2f"|format(row['team_score']) }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </section>
        </div>
    </div>

    <script>
        function predictMatch() {
            const teamA = document.getElementById('teamA').value;
            const teamB = document.getElementById('teamB').value;
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');

            if (!teamA || !teamB) {
                alert('⚠️ Por favor selecciona ambos equipos');
                return;
            }

            if (teamA === teamB) {
                alert('❌ Debes seleccionar dos equipos diferentes');
                return;
            }

            // Mostrar loading
            loading.style.display = 'block';
            result.style.display = 'none';

            // Hacer petición
            fetch('/api/predict?teamA=' + teamA + '&teamB=' + teamB)
                .then(response => {
                    // Verificar si la respuesta es exitosa
                    if (!response.ok) {
                        return response.json().then(err => {
                            throw new Error(err.error || 'Error desconocido del servidor');
                        });
                    }
                    return response.json();
                })
                .then(data => {
                    loading.style.display = 'none';

                    // Verificar si hay error en los datos
                    if (data.error) {
                        alert('Error: ' + data.error);
                        return;
                    }

                    result.style.display = 'block';
                    result.innerHTML = `
                        <div class="result-card">
                            <div class="result-header">
                                <h2>Resultado de la Prediccion</h2>
                                <div class="matchup">${data.teamA} vs ${data.teamB}</div>
                            </div>

                            <div class="winner-section">
                                <div class="winner-label">Ganador Predicho</div>
                                <div class="winner-name">${data.winner}</div>
                                <div class="confidence">Confianza: ${data.confidence}%</div>
                            </div>

                            <div class="probabilities">
                                <div class="prob-box">
                                    <div class="prob-team">${data.teamA}</div>
                                    <div class="prob-value">${data.probA}%</div>
                                </div>
                                <div class="prob-box">
                                    <div class="prob-team">${data.teamB}</div>
                                    <div class="prob-value">${data.probB}%</div>
                                </div>
                            </div>

                            <div class="stats-section">
                                <div class="team-stats">
                                    <h3>${data.teamA}</h3>
                                    <div class="stat-row">
                                        <span class="stat-label">Ataque:</span>
                                        <span class="stat-value">${data.teamA_stats.attack}</span>
                                    </div>
                                    <div class="stat-row">
                                        <span class="stat-label">Defensa:</span>
                                        <span class="stat-value">${data.teamA_stats.defense}</span>
                                    </div>
                                    <div class="stat-row">
                                        <span class="stat-label">Forma:</span>
                                        <span class="stat-value">${data.teamA_stats.form}</span>
                                    </div>
                                    <div class="stat-row">
                                        <span class="stat-label">Score Total:</span>
                                        <span class="stat-value">${data.teamA_stats.score}</span>
                                    </div>
                                </div>

                                <div class="team-stats">
                                    <h3>${data.teamB}</h3>
                                    <div class="stat-row">
                                        <span class="stat-label">Ataque:</span>
                                        <span class="stat-value">${data.teamB_stats.attack}</span>
                                    </div>
                                    <div class="stat-row">
                                        <span class="stat-label">Defensa:</span>
                                        <span class="stat-value">${data.teamB_stats.defense}</span>
                                    </div>
                                    <div class="stat-row">
                                        <span class="stat-label">Forma:</span>
                                        <span class="stat-value">${data.teamB_stats.form}</span>
                                    </div>
                                    <div class="stat-row">
                                        <span class="stat-label">Score Total:</span>
                                        <span class="stat-value">${data.teamB_stats.score}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                    // Scroll al resultado
                    result.scrollIntoView({ behavior: 'smooth' });
                })
                .catch(error => {
                    loading.style.display = 'none';
                    result.style.display = 'none';
                    alert('Error: ' + error.message);
                    console.error('Error completo:', error);
                });
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    try:
        summary = pd.read_csv('outputs/project_summary.csv')
        teams = pd.read_csv('outputs/teams_analysis.csv').sort_values('team_score', ascending=False)

        return render_template_string(HTML_TEMPLATE, teams=teams, summary=summary)
    except Exception as e:
        return f"<h1>Error:</h1><pre>{str(e)}</pre>"

@app.route('/api/predict')
def api_predict():
    try:
        # Obtener parámetros
        team_a_id = request.args.get('teamA')
        team_b_id = request.args.get('teamB')

        # Validar que existan
        if not team_a_id or not team_b_id:
            return jsonify({
                'error': 'Faltan parámetros teamA o teamB'
            }), 400

        # Convertir a enteros
        try:
            team_a_id = int(team_a_id)
            team_b_id = int(team_b_id)
        except ValueError:
            return jsonify({
                'error': 'Los IDs de equipos deben ser números'
            }), 400

        # Validar que sean diferentes
        if team_a_id == team_b_id:
            return jsonify({
                'error': 'Debes seleccionar dos equipos diferentes'
            }), 400

        print(f"[API] Prediciendo: Team A ID={team_a_id}, Team B ID={team_b_id}")

        # Realizar predicción
        result = predict_match(team_a_id, team_b_id)

        print(f"[API] Resultado: {result['winner']} con {result['confidence']}% confianza")

        return jsonify(result)

    except KeyError as e:
        print(f"[ERROR] KeyError: {e}")
        return jsonify({
            'error': f'Equipo no encontrado: {str(e)}'
        }), 404

    except Exception as e:
        print(f"[ERROR] Exception en /api/predict: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': f'Error interno del servidor: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("="*80)
    print("🌐 SERVIDOR WEB INTERACTIVO INICIADO")
    print("="*80)
    print("\n📍 URL: http://127.0.0.1:5001")
    print("\n🔗 Abre esta URL en tu navegador")
    print("🎯 Selecciona dos equipos y predice el resultado")
    print("\n="*80)
    print("\n⏸️  Presiona CTRL+C para detener\n")

    app.run(debug=True, port=5001, use_reloader=False)
