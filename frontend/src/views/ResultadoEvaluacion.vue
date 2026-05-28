<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const resultado = history.state.resultado
const examen = history.state.examen
const alumno = history.state.alumno

const continuar = () => {
  router.push('/evaluacion')
}

if (!resultado) {
  console.error('No hay resultados')
}
</script>

<template>
  <div class="container">
    <div class="card">
      <h1>Resultado del examen</h1>
      <div class="info">
        <p>
          <strong>Examen:</strong>
          {{ examen }}
        </p>

        <p>
          <strong>Alumno:</strong>
          {{ alumno }}
        </p>
      </div>

      <div class="summary">
        <p><strong>Calificación:</strong> {{ resultado.calificacion.toFixed(2) }}</p>

        <p>
          <strong>Correctas:</strong>
          {{ resultado.correctas }} / {{ resultado.total }}
        </p>
      </div>

      <table>
        <thead>
          <tr>
            <th>Pregunta</th>
            <th>Respuesta alumno</th>
            <th>Correcta</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="(r, index) in resultado.respuestas" :key="r.id_pregunta">
            <td>{{ index + 1 }}</td>
            <td>
              {{ r.respuesta_alumno || 'Sin responder' }}
            </td>
            <td>
              <span v-if="r.es_correcta">✅</span>
              <span v-else>❌</span>
            </td>
          </tr>
        </tbody>
      </table>
      <div class="actions">
        <button @click="continuar">Continuar</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  padding: 40px;
}

.card {
  width: 800px;
  background: white;
  padding: 25px;
  border-radius: 14px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
}

.summary {
  margin-bottom: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 12px;
  border-bottom: 1px solid #ddd;
  text-align: center;
}

th {
  background: #f5f5f5;
}
.info {
  margin-bottom: 20px;
}

.actions {
  margin-top: 25px;
  display: flex;
  justify-content: flex-end;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 10px;
  background: #6366f1;
  color: white;
  cursor: pointer;
}

button:hover {
  background: #4f46e5;
}
.info {
  margin-bottom: 20px;
}

.actions {
  margin-top: 25px;
  display: flex;
  justify-content: flex-end;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 10px;
  background: #6366f1;
  color: white;
  cursor: pointer;
}

button:hover {
  background: #4f46e5;
}

.info {
  margin-bottom: 20px;
}

.actions {
  margin-top: 25px;
  display: flex;
  justify-content: flex-end;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 10px;
  background: #6366f1;
  color: white;
  cursor: pointer;
}

button:hover {
  background: #4f46e5;
}
</style>
