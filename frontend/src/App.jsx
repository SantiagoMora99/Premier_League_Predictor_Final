import { useEffect, useMemo, useState } from 'react'
import axios from 'axios'
import './App.css'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

function App() {
  const [teams, setTeams] = useState([])
  const [loadingTeams, setLoadingTeams] = useState(true)
  const [error, setError] = useState('')

  const [teamA, setTeamA] = useState('')
  const [teamB, setTeamB] = useState('')
  const [predictLoading, setPredictLoading] = useState(false)
  const [prediction, setPrediction] = useState(null)

  useEffect(() => {
    const fetchTeams = async () => {
      setLoadingTeams(true)
      setError('')
      try {
        const resp = await axios.get(`${API_BASE}/teams`)
        setTeams(resp.data.teams || [])
      } catch (e) {
        setError(e?.response?.data?.detail || e.message || 'Error cargando equipos')
      } finally {
        setLoadingTeams(false)
      }
    }
    fetchTeams()
  }, [])

  const sortedTeams = useMemo(() => {
    return [...teams].sort((a, b) => a.name.localeCompare(b.name))
  }, [teams])

  const canPredict = teamA && teamB && teamA !== teamB

  const handlePredict = async () => {
    if (!canPredict) {
      setError('Debes elegir dos equipos diferentes')
      return
    }
    setPredictLoading(true)
    setError('')
    setPrediction(null)
    try {
      const resp = await axios.get(`${API_BASE}/predict`, {
        params: { teamA_id: Number(teamA), teamB_id: Number(teamB) }
      })
      setPrediction(resp.data)
    } catch (e) {
      setError(e?.response?.data?.detail || e.message || 'Error en la predicción')
    } finally {
      setPredictLoading(false)
    }
  }

  return (
    <div style={{ maxWidth: 720, margin: '0 auto', padding: 24 }}>
      <h1>Predicción Premier League</h1>

      {loadingTeams && <p>Cargando equipos...</p>}
      {error && <p style={{ color: 'salmon' }}>{error}</p>}

      {!loadingTeams && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
          <div>
            <label htmlFor="teamA">Equipo A</label>
            <select id="teamA" value={teamA} onChange={(e) => setTeamA(e.target.value)} style={{ width: '100%', padding: 8 }}>
              <option value="">Selecciona equipo</option>
              {sortedTeams.map(t => (
                <option key={t.id} value={t.id}>{t.name}</option>
              ))}
            </select>
          </div>
          <div>
            <label htmlFor="teamB">Equipo B</label>
            <select id="teamB" value={teamB} onChange={(e) => setTeamB(e.target.value)} style={{ width: '100%', padding: 8 }}>
              <option value="">Selecciona equipo</option>
              {sortedTeams.map(t => (
                <option key={t.id} value={t.id}>{t.name}</option>
              ))}
            </select>
          </div>
        </div>
      )}

      <div style={{ marginTop: 16 }}>
        <button disabled={!canPredict || predictLoading} onClick={handlePredict}>
          {predictLoading ? 'Calculando...' : 'Predecir'}
        </button>
      </div>

      {prediction && (
        <div style={{ marginTop: 24, padding: 16, border: '1px solid #444', borderRadius: 8 }}>
          <h2>Resultado</h2>
          <p>{prediction.teamA} vs {prediction.teamB}</p>
          <p>Probabilidades: {prediction.probA}% - {prediction.probB}%</p>
          <p>Ganador: <strong>{prediction.winner}</strong></p>
          <p>Confianza: {prediction.confidence}%</p>
          <small style={{ color: '#888' }}>{prediction.model_note}</small>
        </div>
      )}
    </div>
  )
}

export default App
