"""
Script para ejecutar el analisis completo de Premier League
Este script ejecuta todas las secciones del notebook de forma automatica
"""
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_curve, auc
from sklearn.preprocessing import StandardScaler
import requests
import pickle
import os
import warnings
warnings.filterwarnings('ignore')

# Configuración de visualización
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

print("="*80)
print(" "*20 + "🏆 PREMIER LEAGUE MATCH PREDICTOR")
print("="*80 + "\n")

# ==========================================
# SECCIÓN 1: CONFIGURACIÓN
# ==========================================
print("📦 SECCIÓN 1: Configuración")
print("-" * 80)

API_KEY = "f50c3bb69922405b8963e15c66c23877"
LEAGUE = "PL"
API_BASE = "https://api.football-data.org/v4"
HEADERS = {"X-Auth-Token": API_KEY}

# Crear directorios
os.makedirs('data', exist_ok=True)
os.makedirs('outputs', exist_ok=True)
os.makedirs('models', exist_ok=True)

print("✅ Directorios creados: data/, outputs/, models/\n")

# ==========================================
# SECCIÓN 2: OBTENCIÓN DE DATOS
# ==========================================
print("📊 SECCIÓN 2: Obtención de Datos de la API")
print("-" * 80)

def fetch_standings():
    url = f"{API_BASE}/competitions/{LEAGUE}/standings"

    try:
        print("📡 Conectando a football-data.org API...")
        response = requests.get(url, headers=HEADERS, timeout=10)

        if response.status_code == 200:
            data = response.json()
            table = data["standings"][0]["table"]

            teams = []
            for row in table:
                teams.append({
                    "id": row["team"]["id"],
                    "name": row["team"]["name"],
                    "position": row["position"],
                    "played": row["playedGames"],
                    "won": row["won"],
                    "draw": row["draw"],
                    "lost": row["lost"],
                    "points": row["points"],
                    "goalsFor": row["goalsFor"],
                    "goalsAgainst": row["goalsAgainst"],
                    "goalDifference": row["goalDifference"]
                })

            print(f"✅ Datos obtenidos: {len(teams)} equipos de la Premier League")
            return pd.DataFrame(teams)

        elif response.status_code == 429:
            print("⚠️ Límite de API alcanzado. Cargando datos guardados...")
            return pd.read_csv('data/teams_raw.csv')
        else:
            raise Exception(f"Error en API: {response.status_code}")

    except Exception as e:
        print(f"⚠️ Error: {e}")
        if os.path.exists('data/teams_raw.csv'):
            print("📂 Cargando datos guardados...")
            return pd.read_csv('data/teams_raw.csv')
        raise

df_teams = fetch_standings()
df_teams.to_csv('data/teams_raw.csv', index=False)
print(f"💾 Datos guardados: data/teams_raw.csv")
print(f"\n📊 Primeras filas:\n{df_teams.head()}\n")

# ==========================================
# SECCIÓN 3: ESTADÍSTICAS DESCRIPTIVAS
# ==========================================
print("\n📈 SECCIÓN 3: Estadísticas Descriptivas")
print("-" * 80)
print(f"Equipos: {len(df_teams)}")
print(f"Columnas: {len(df_teams.columns)}")
print(f"\nEstadísticas básicas:")
print(df_teams[['points', 'goalsFor', 'goalsAgainst', 'won', 'draw', 'lost']].describe())

# ==========================================
# SECCIÓN 4: FEATURE ENGINEERING
# ==========================================
print("\n\n⚙️ SECCIÓN 4: Feature Engineering")
print("-" * 80)

df_features = df_teams.copy()

# Métricas por partido
df_features['points_per_game'] = df_features['points'] / df_features['played'].replace(0, 1)
df_features['goals_for_per_game'] = df_features['goalsFor'] / df_features['played'].replace(0, 1)
df_features['goals_against_per_game'] = df_features['goalsAgainst'] / df_features['played'].replace(0, 1)

# Fuerza
df_features['attack_strength'] = df_features['goals_for_per_game']
df_features['defense_strength'] = 1 / (df_features['goals_against_per_game'].replace(0, 0.1))

# Eficiencia
df_features['win_rate'] = (df_features['won'] / df_features['played'].replace(0, 1)) * 100
df_features['draw_rate'] = (df_features['draw'] / df_features['played'].replace(0, 1)) * 100
df_features['loss_rate'] = (df_features['lost'] / df_features['played'].replace(0, 1)) * 100

# Scores
df_features['goal_difference_per_game'] = df_features['goalDifference'] / df_features['played'].replace(0, 1)
df_features['form_score'] = (df_features['points_per_game'] * 0.6 + df_features['goal_difference_per_game'] * 0.4)
df_features['team_score'] = (
    df_features['attack_strength'] * 0.35 +
    df_features['defense_strength'] * 0.35 +
    df_features['form_score'] * 0.30
)

df_features.to_csv('data/teams_with_features.csv', index=False)
print("✅ Features creados exitosamente")
print(f"💾 Guardado: data/teams_with_features.csv")
print(f"\nTop 5 equipos por score total:")
print(df_features[['name', 'team_score', 'attack_strength', 'defense_strength', 'form_score']].sort_values('team_score', ascending=False).head())

# ==========================================
# SECCIÓN 5: VISUALIZACIONES
# ==========================================
print("\n\n📊 SECCIÓN 5: Generando Visualizaciones")
print("-" * 80)

# Vis 1: Distribución de puntos
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
df_sorted = df_features.sort_values('points', ascending=True)
axes[0].barh(df_sorted['name'], df_sorted['points'], color='steelblue')
axes[0].set_xlabel('Puntos', fontsize=12)
axes[0].set_title('Puntos por Equipo', fontsize=14, fontweight='bold')
axes[0].grid(axis='x', alpha=0.3)

axes[1].hist(df_features['points'], bins=10, color='coral', edgecolor='black', alpha=0.7)
axes[1].set_xlabel('Puntos', fontsize=12)
axes[1].set_ylabel('Frecuencia', fontsize=12)
axes[1].set_title('Distribución de Puntos', fontsize=14, fontweight='bold')
axes[1].axvline(df_features['points'].mean(), color='red', linestyle='--', linewidth=2, label=f'Media: {df_features["points"].mean():.1f}')
axes[1].legend()
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('outputs/01_distribucion_puntos.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Gráfico 1: outputs/01_distribucion_puntos.png")

# Vis 2: Ataque vs Defensa
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
top_attack = df_features.nlargest(10, 'goalsFor').sort_values('goalsFor')
axes[0].barh(top_attack['name'], top_attack['goalsFor'], color='green', alpha=0.7)
axes[0].set_xlabel('Goles a Favor', fontsize=12)
axes[0].set_title('Top 10 Mejores Ataques', fontsize=14, fontweight='bold')
axes[0].grid(axis='x', alpha=0.3)

top_defense = df_features.nsmallest(10, 'goalsAgainst').sort_values('goalsAgainst', ascending=False)
axes[1].barh(top_defense['name'], top_defense['goalsAgainst'], color='red', alpha=0.7)
axes[1].set_xlabel('Goles en Contra', fontsize=12)
axes[1].set_title('Top 10 Mejores Defensas', fontsize=14, fontweight='bold')
axes[1].grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig('outputs/02_ataque_defensa.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Gráfico 2: outputs/02_ataque_defensa.png")

# Vis 3: Matriz de correlación
numeric_cols = ['played', 'won', 'draw', 'lost', 'points', 'goalsFor', 'goalsAgainst', 'goalDifference']
correlation_matrix = df_features[numeric_cols].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0, square=True, linewidths=1)
plt.title('Matriz de Correlación de Variables', fontsize=14, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('outputs/03_matriz_correlacion.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Gráfico 3: outputs/03_matriz_correlacion.png")

# ==========================================
# SECCIÓN 6: CREACIÓN DE DATASET ML
# ==========================================
print("\n\n🤖 SECCIÓN 6: Creación de Dataset para ML")
print("-" * 80)

def create_match_dataset(df):
    matches = []
    for i, team_a in df.iterrows():
        for j, team_b in df.iterrows():
            if i != j:
                match = {
                    'teamA_id': team_a['id'],
                    'teamB_id': team_b['id'],
                    'teamA_name': team_a['name'],
                    'teamB_name': team_b['name'],
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
                    'teamA_score': team_a['team_score'],
                    'teamB_score': team_b['team_score'],
                    'score_diff': team_a['team_score'] - team_b['team_score'],
                }
                prob_a_wins = 1 / (1 + np.exp(-match['score_diff']))
                match['winner'] = 1 if prob_a_wins > 0.5 else 0
                matches.append(match)
    return pd.DataFrame(matches)

df_matches = create_match_dataset(df_features)
df_matches.to_csv('data/matches_dataset.csv', index=False)
print(f"✅ Dataset creado: {len(df_matches)} enfrentamientos")
print(f"💾 Guardado: data/matches_dataset.csv")
print(f"   Team A gana: {(df_matches['winner'] == 1).sum()}")
print(f"   Team B gana: {(df_matches['winner'] == 0).sum()}")

# ==========================================
# SECCIÓN 7: ENTRENAMIENTO DE MODELOS
# ==========================================
print("\n\n🧠 SECCIÓN 7: Entrenamiento de Modelos ML")
print("-" * 80)

feature_columns = [
    'attack_diff', 'defense_diff', 'form_diff', 'points_diff', 'goal_diff_diff',
    'teamA_attack', 'teamA_defense', 'teamA_form',
    'teamB_attack', 'teamB_defense', 'teamB_form',
    'score_diff'
]

X = df_matches[feature_columns]
y = df_matches['winner']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
print(f"📊 Dataset dividido: {len(X_train)} train, {len(X_test)} test")

# Scaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

with open('models/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)
print("💾 Scaler guardado: models/scaler.pkl")

# Entrenar modelos
models = {}
results = {}

print("\n🔄 Entrenando modelos...")

# Logistic Regression
print("  1️⃣ Logistic Regression...")
lr_model = LogisticRegression(random_state=42, max_iter=1000)
lr_model.fit(X_train_scaled, y_train)
lr_pred = lr_model.predict(X_test_scaled)
lr_accuracy = accuracy_score(y_test, lr_pred)
models['Logistic Regression'] = lr_model
results['Logistic Regression'] = lr_accuracy
print(f"     Accuracy: {lr_accuracy:.4f}")

# Random Forest
print("  2️⃣ Random Forest...")
rf_model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
rf_model.fit(X_train, y_train)
rf_pred = rf_model.predict(X_test)
rf_accuracy = accuracy_score(y_test, rf_pred)
models['Random Forest'] = rf_model
results['Random Forest'] = rf_accuracy
print(f"     Accuracy: {rf_accuracy:.4f}")

# Gradient Boosting
print("  3️⃣ Gradient Boosting...")
gb_model = GradientBoostingClassifier(n_estimators=100, random_state=42, max_depth=5)
gb_model.fit(X_train, y_train)
gb_pred = gb_model.predict(X_test)
gb_accuracy = accuracy_score(y_test, gb_pred)
models['Gradient Boosting'] = gb_model
results['Gradient Boosting'] = gb_accuracy
print(f"     Accuracy: {gb_accuracy:.4f}")

# Mejor modelo
results_df = pd.DataFrame(list(results.items()), columns=['Modelo', 'Accuracy'])
results_df = results_df.sort_values('Accuracy', ascending=False)
best_model_name = results_df.iloc[0]['Modelo']
best_model = models[best_model_name]

print(f"\n🏆 Mejor modelo: {best_model_name} (Accuracy: {results_df.iloc[0]['Accuracy']:.4f})")

with open('models/best_model.pkl', 'wb') as f:
    pickle.dump(best_model, f)
print("💾 Mejor modelo guardado: models/best_model.pkl")

# ==========================================
# SECCIÓN 8: EVALUACIÓN
# ==========================================
print("\n\n📈 SECCIÓN 8: Evaluación del Modelo")
print("-" * 80)

if best_model_name == 'Logistic Regression':
    y_pred = lr_pred
    y_pred_proba = lr_model.predict_proba(X_test_scaled)[:, 1]
elif best_model_name == 'Random Forest':
    y_pred = rf_pred
    y_pred_proba = rf_model.predict_proba(X_test)[:, 1]
else:
    y_pred = gb_pred
    y_pred_proba = gb_model.predict_proba(X_test)[:, 1]

print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Team B Wins', 'Team A Wins']))

# ROC Curve
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
roc_auc = auc(fpr, tpr)
print(f"\n📊 AUC Score: {roc_auc:.4f}")

# Confusion Matrix
plt.figure(figsize=(8, 6))
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
           xticklabels=['Team B Wins', 'Team A Wins'],
           yticklabels=['Team B Wins', 'Team A Wins'])
plt.xlabel('Predicción', fontsize=12)
plt.ylabel('Real', fontsize=12)
plt.title(f'Matriz de Confusión - {best_model_name}', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('outputs/04_confusion_matrix.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Gráfico 4: outputs/04_confusion_matrix.png")

# ROC Curve plot
plt.figure(figsize=(10, 8))
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Classifier')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate', fontsize=12)
plt.ylabel('True Positive Rate', fontsize=12)
plt.title(f'ROC Curve - {best_model_name}', fontsize=14, fontweight='bold')
plt.legend(loc="lower right")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('outputs/05_roc_curve.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Gráfico 5: outputs/05_roc_curve.png")

# ==========================================
# SECCIÓN 9: SISTEMA DE PREDICCIÓN
# ==========================================
print("\n\n🎯 SECCIÓN 9: Sistema de Predicción")
print("-" * 80)

def predict_match_ml(team_a_id, team_b_id, model, scaler, df_features, use_scaling=False):
    try:
        team_a = df_features[df_features['id'] == team_a_id].iloc[0]
        team_b = df_features[df_features['id'] == team_b_id].iloc[0]
    except IndexError:
        return {"error": "Equipo no encontrado"}

    match_features = pd.DataFrame([{
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

    if use_scaling and scaler is not None:
        match_features_scaled = scaler.transform(match_features)
        prediction_proba = model.predict_proba(match_features_scaled)[0]
    else:
        prediction_proba = model.predict_proba(match_features)[0]

    prob_b_wins = prediction_proba[0] * 100
    prob_a_wins = prediction_proba[1] * 100

    if prob_a_wins > prob_b_wins:
        winner = team_a['name']
        confidence = prob_a_wins
    else:
        winner = team_b['name']
        confidence = prob_b_wins

    return {
        "teamA": team_a['name'],
        "teamB": team_b['name'],
        "probA": round(prob_a_wins, 2),
        "probB": round(prob_b_wins, 2),
        "winner": winner,
        "confidence": round(confidence, 2),
        "model_used": best_model_name
    }

# Prueba
team_a = df_features.iloc[0]
team_b = df_features.iloc[1]

print(f"\n🧪 Prueba del sistema:")
print(f"   {team_a['name']} vs {team_b['name']}")

use_scaling = (best_model_name == 'Logistic Regression')
prediction = predict_match_ml(team_a['id'], team_b['id'], best_model, scaler, df_features, use_scaling)

print(f"\n   🏆 Ganador predicho: {prediction['winner']}")
print(f"   📊 Confianza: {prediction['confidence']}%")
print(f"   📈 Probabilidades:")
print(f"      {prediction['teamA']}: {prediction['probA']}%")
print(f"      {prediction['teamB']}: {prediction['probB']}%")

# ==========================================
# SECCIÓN 10: EXPORTAR CSVs
# ==========================================
print("\n\n💾 SECCIÓN 10: Exportación de CSVs")
print("-" * 80)

# 1. Teams analysis
output_teams = df_features[['id', 'name', 'position', 'played', 'won', 'draw', 'lost',
                           'points', 'goalsFor', 'goalsAgainst', 'goalDifference',
                           'attack_strength', 'defense_strength', 'form_score', 'team_score']]
output_teams.to_csv('outputs/teams_analysis.csv', index=False)
print("✅ 1. outputs/teams_analysis.csv")

# 2. Match predictions (50 predicciones de ejemplo)
predictions_list = []
for i in range(min(10, len(df_features))):
    for j in range(i+1, min(10, len(df_features))):
        team_a = df_features.iloc[i]
        team_b = df_features.iloc[j]
        pred = predict_match_ml(team_a['id'], team_b['id'], best_model, scaler, df_features, use_scaling)
        predictions_list.append(pred)

df_predictions = pd.DataFrame(predictions_list)
df_predictions.to_csv('outputs/match_predictions.csv', index=False)
print(f"✅ 2. outputs/match_predictions.csv ({len(df_predictions)} predicciones)")

# 3. Model performance
model_metrics = pd.DataFrame({
    'model': list(results.keys()),
    'accuracy': list(results.values())
})
model_metrics['best_model'] = model_metrics['model'] == best_model_name
model_metrics.to_csv('outputs/model_performance.csv', index=False)
print("✅ 3. outputs/model_performance.csv")

# 4. Training dataset
df_matches.to_csv('outputs/training_dataset.csv', index=False)
print(f"✅ 4. outputs/training_dataset.csv ({len(df_matches)} enfrentamientos)")

# 5. Summary
summary = {
    'metric': [
        'Total Teams', 'Total Matches in Training', 'Best Model',
        'Best Model Accuracy', 'Total Features', 'Training Samples',
        'Test Samples', 'AUC Score'
    ],
    'value': [
        len(df_features), len(df_matches), best_model_name,
        f"{results[best_model_name]:.4f}", len(feature_columns),
        len(X_train), len(X_test), f"{roc_auc:.4f}"
    ]
}
df_summary = pd.DataFrame(summary)
df_summary.to_csv('outputs/project_summary.csv', index=False)
print("✅ 5. outputs/project_summary.csv")

# ==========================================
# RESUMEN FINAL
# ==========================================
print("\n\n" + "="*80)
print(" "*30 + "RESUMEN FINAL")
print("="*80 + "\n")

print("📁 ARCHIVOS GENERADOS:\n")
print("📂 data/")
print("   ├── teams_raw.csv")
print("   ├── teams_with_features.csv")
print("   └── matches_dataset.csv")
print("\n📂 outputs/")
print("   ├── teams_analysis.csv")
print("   ├── match_predictions.csv")
print("   ├── model_performance.csv")
print("   ├── training_dataset.csv")
print("   ├── project_summary.csv")
print("   └── [5 gráficos PNG]")
print("\n📂 models/")
print("   ├── best_model.pkl")
print("   └── scaler.pkl")

print("\n" + "="*80)
print("\n📊 ESTADÍSTICAS DEL PROYECTO:\n")
print(f"   🏆 Equipos analizados: {len(df_features)}")
print(f"   🤖 Mejor modelo: {best_model_name}")
print(f"   🎯 Accuracy: {results[best_model_name]:.4f}")
print(f"   📈 AUC Score: {roc_auc:.4f}")
print(f"   🔢 Features: {len(feature_columns)}")
print(f"   📝 Predicciones generadas: {len(df_predictions)}")
print(f"   📊 Gráficos: 5")

print("\n" + "="*80)
print("\n✅ ANÁLISIS COMPLETADO EXITOSAMENTE")
print("\n" + "="*80)
