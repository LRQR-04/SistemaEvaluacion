<script setup>
import { ref, watch } from 'vue'
import api from '../../services/api'
import { Eye, Loader2 } from 'lucide-vue-next'

const props = defineProps({
  examen: Object,
})

const emit = defineEmits(['close', 'success'])

const resultados = ref([])
const respuestasAlumno = ref([])

const loading = ref(false)
const loadingRespuestas = ref(false)

const alumnoSeleccionado = ref(null)

const formatearFecha = (fecha) => {
  if (!fecha) return ''

  return new Date(fecha).toLocaleDateString('es-MX', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  })
}

const cargarResultados = async () => {
  if (!props.examen) return

  loading.value = true

  try {
    const res = await api.get(`/resultados/examen/${props.examen.id_examen}`)
    resultados.value = res.data
  } catch (err) {
    emit('success', err.response?.data?.detail || 'Error al cargar resultados', 'error')
  } finally {
    loading.value = false
  }
}

watch(
  () => props.examen,
  () => cargarResultados(),
  { immediate: true },
)

const verRespuestas = async (resultado) => {
  alumnoSeleccionado.value = resultado
  loadingRespuestas.value = true

  try {
    const res = await api.get(`/respuestas/resultado/${resultado.id_resultado}`)
    respuestasAlumno.value = res.data
  } catch (err) {
    emit('success', err.response?.data?.detail || 'Error al cargar respuestas', 'error')
  } finally {
    loadingRespuestas.value = false
  }
}
</script>

<template>
  <div class="overlay" @click.self="$emit('close')">
    <div class="modal">
      <!-- HEADER -->
      <div class="header">
        <div>
          <h3>Resultados del examen</h3>

          <p class="subtitle">
            {{ examen?.nombre_examen }}
          </p>
        </div>

        <button class="close" @click="$emit('close')">✕</button>
      </div>

      <!-- CONTENT -->
      <div class="content">
        <!-- PANEL IZQUIERDO -->
        <div class="list">
          <div v-if="loading" class="loading">
            <Loader2 class="spin" size="18" />
            Cargando resultados...
          </div>

          <div v-else-if="resultados.length === 0" class="empty">No hay resultados registrados</div>

          <div
            v-else
            v-for="r in resultados"
            :key="r.id_resultado"
            class="card"
            :class="{
              active: alumnoSeleccionado?.id_resultado === r.id_resultado,
            }"
          >
            <div class="card-top">
              <span class="badge"> {{ r.calificacion }}/10 </span>
              <span class="date"> {{ formatearFecha(r.fecha_evaluacion) }} </span>
            </div>

            <p class="student">{{ r.nombre }} {{ r.apellido_paterno }} {{ r.apellido_materno }}</p>

            <p class="matricula">
              Matrícula:
              {{ r.matricula }}
            </p>

            <div class="footer">
              <button @click="verRespuestas(r)">
                <Eye size="14" />
                Ver respuestas
              </button>
            </div>
          </div>
        </div>

        <!-- PANEL DERECHO -->
        <div class="details">
          <template v-if="alumnoSeleccionado">
            <div class="detail-header">
              <h4>
                Respuestas de
                {{ alumnoSeleccionado.nombre }} {{ alumnoSeleccionado.apellido_paterno }}
                {{ alumnoSeleccionado.apellido_materno }}
              </h4>

              <span class="score">
                Calificación:
                {{ alumnoSeleccionado.calificacion }}/10
              </span>
            </div>

            <div v-if="loadingRespuestas" class="loading">
              <Loader2 class="spin" size="18" />
              Cargando respuestas...
            </div>

            <div
              v-else
              v-for="respuesta in respuestasAlumno"
              :key="respuesta.id_respuesta"
              class="respuesta-card"
            >
              <p class="question">
                {{ respuesta.pregunta }}
              </p>

              <div class="answers">
                <p>
                  <strong>Respuesta alumno:</strong>
                  {{
                    respuesta.respuesta_alumno
                      ? respuesta.respuesta_alumno.toUpperCase()
                      : 'Sin responder'
                  }}
                </p>

                <p>
                  <strong>Correcta:</strong>
                  {{ respuesta.respuesta_correcta.toUpperCase() }}
                </p>
              </div>

              <span class="result-badge" :class="respuesta.es_correcta ? 'correct' : 'incorrect'">
                {{ respuesta.es_correcta ? 'Correcta' : 'Incorrecta' }}
              </span>
            </div>
          </template>

          <div v-else class="empty-detail">Selecciona un alumno para visualizar sus respuestas</div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal {
  width: 950px;
  max-width: 92%;
  background: white;
  border-radius: 14px;
  padding: 14px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.16);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.header h3 {
  font-size: 18px;
}

.subtitle {
  font-size: 12px;
  color: #6b7280;
  margin-top: 2px;
}

.close {
  border: none;
  background: #f3f4f6;
  width: 30px;
  height: 30px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
}

.content {
  display: grid;
  grid-template-columns: 0.95fr 1.1fr;
  gap: 12px;
}

.list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 65vh;
  overflow-y: auto;
}

.card {
  border: 1px solid #e5e7eb;
  padding: 10px;
  border-radius: 10px;
  transition: 0.2s;
}

.card.active {
  border-color: #6366f1;
  background: #f5f3ff;
}

.card-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.student {
  font-weight: 600;
  margin-bottom: 4px;
  font-size: 14px;
}

.matricula {
  font-size: 12px;
  color: #6b7280;
  margin-bottom: 10px;
}

.footer {
  display: flex;
  justify-content: flex-end;
}

.footer button {
  border: none;
  background: #eef2ff;
  color: #4338ca;
  padding: 7px 9px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
}

.badge {
  background: #dcfce7;
  color: #166534;
  padding: 3px 8px;
  border-radius: 999px;
  font-size: 10px;
  font-weight: 600;
}

.date {
  font-size: 11px;
  color: #6b7280;
}

.details {
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 12px;
  max-height: 65vh;
  overflow-y: auto;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  gap: 10px;
}

.detail-header h4 {
  font-size: 15px;
}

.score {
  background: #ede9fe;
  color: #5b21b6;
  padding: 5px 10px;
  border-radius: 999px;
  font-size: 11px;
  white-space: nowrap;
}

.respuesta-card {
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 10px;
  margin-bottom: 10px;
}

.question {
  font-weight: 600;
  margin-bottom: 8px;
  font-size: 13px;
}

.answers {
  display: flex;
  flex-direction: column;
  gap: 5px;
  font-size: 13px;
  color: #4b5563;
}

.result-badge {
  display: inline-block;
  margin-top: 8px;
  padding: 4px 9px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 500;
}

.correct {
  background: #dcfce7;
  color: #166534;
}

.incorrect {
  background: #fee2e2;
  color: #991b1b;
}

.loading,
.empty,
.empty-detail {
  padding: 18px;
  text-align: center;
  color: #6b7280;
  font-size: 13px;
}

.empty-detail {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  100% {
    transform: rotate(360deg);
  }
}

@media (max-width: 900px) {
  .content {
    grid-template-columns: 1fr;
  }

  .modal {
    width: 95%;
  }

  .details,
  .list {
    max-height: unset;
  }
}
</style>
