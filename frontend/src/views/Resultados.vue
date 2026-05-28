<script setup>
import { ref, computed, onMounted, watch } from 'vue'

import api from '../services/api'

import { useAuthStore } from '../stores/autenticacion.js'

import ModalTabla from '../components/ModalTabla.vue'
import Alerta from '../components/Alerta.vue'

import { Eye } from 'lucide-vue-next'

const auth = useAuthStore()

const idEstudiante = ref(null)

const registros = ref([])

const page = ref(1)
const total = ref(0)

const loading = ref(false)

const filtros = ref({
  alumno: '',
  examen: '',
  fecha: '',
})

const modalTabla = ref(false)

const modalTitle = ref('')
const modalSubtitle = ref('')

const modalColumns = ref([])
const modalRows = ref([])

const modalLoading = ref(false)

const alertMsg = ref('')
const alertType = ref('success')

/* =========================================
   ALERTAS
========================================= */
const mostrarAlerta = (msg, type = 'success') => {
  alertMsg.value = msg
  alertType.value = type

  setTimeout(() => {
    alertMsg.value = ''
  }, 3000)
}

/* =========================================
   OBTENER ID ESTUDIANTE
========================================= */
const cargarIdEstudiante = async () => {
  try {
    const res = await api.get(`/estudiantes/usuario/${auth.user.user_id}`)

    idEstudiante.value = res.data.id_estudiante
  } catch (error) {
    mostrarAlerta('Error al obtener estudiante', 'error')
  }
}

/* =========================================
   ENDPOINT DINÁMICO
========================================= */
const endpointActual = computed(() => {
  // ADMIN
  if (auth.user?.rol === 'admin') {
    return '/resultados'
  }

  // ESTUDIANTE
  if (auth.user?.rol === 'estudiante') {
    if (!idEstudiante.value) return null

    return `/resultados/estudiante/${idEstudiante.value}/tabla`
  }

  return null
})

const cargar = async () => {
  if (!endpointActual.value) return

  loading.value = true

  try {
    const res = await api.get(endpointActual.value, {
      params: {
        page: page.value,
        limit: 10,
        alumno: filtros.value.alumno,
        examen: filtros.value.examen,
        fecha: filtros.value.fecha,
      },
    })

    registros.value = res.data.data
    total.value = res.data.total
  } catch (error) {
    console.error(error)

    mostrarAlerta(error.response?.data?.detail || 'Error al cargar resultados', 'error')
  } finally {
    loading.value = false
  }
}

/* =========================================
   BUSCAR
========================================= */
const buscar = () => {
  page.value = 1
  cargar()
}

/* =========================================
   VER RESPUESTAS
========================================= */
const verRespuestas = async (resultado) => {
  modalLoading.value = true
  modalTabla.value = true

  modalTitle.value = 'Detalle de respuestas'

  modalSubtitle.value =
    auth.user?.rol === 'admin'
      ? `${resultado.nombre_alumno} - ${resultado.nombre_examen}`
      : resultado.nombre_examen

  modalColumns.value = [
    {
      label: 'Pregunta',
      key: 'pregunta',
    },
    {
      label: 'Respuesta alumno',
      key: 'respuesta_alumno',
    },
    {
      label: 'Estado',
      key: 'estado',
    },
  ]

  try {
    const res = await api.get(`/respuestas/resultado/${resultado.id_resultado}`)

    modalRows.value = res.data.map((r, index) => ({
      pregunta: `Pregunta ${index + 1}`,
      respuesta_alumno: r.respuesta_alumno || 'Sin responder',
      estado: r.es_correcta ? '✅ Correcta' : '❌ Incorrecta',
    }))
  } catch (error) {
    mostrarAlerta(error.response?.data?.detail || 'Error al cargar respuestas', 'error')
  } finally {
    modalLoading.value = false
  }
}

/* =========================================
   FECHAS
========================================= */
const formatearFecha = (fecha) => {
  if (!fecha) return ''

  return new Date(fecha).toLocaleDateString('es-MX', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  })
}

/* =========================================
   PAGINACIÓN
========================================= */
const totalPages = computed(() => {
  const pages = Math.ceil(total.value / 10)

  return pages > 0 ? pages : 1
})

watch(page, () => {
  cargar()
})

/* =========================================
   INIT
========================================= */
onMounted(async () => {
  if (auth.user?.rol === 'estudiante') {
    await cargarIdEstudiante()
  }

  await cargar()
})
</script>

<template>
  <div class="container">
    <Alerta :message="alertMsg" :type="alertType" />

    <!-- HEADER -->
    <div class="header">
      <div>
        <h2>
          {{ auth.user?.rol === 'admin' ? 'Resultados generales' : 'Mis resultados' }}
        </h2>

        <p class="subtitle">Consulta de evaluaciones realizadas</p>
      </div>
    </div>

    <!-- FILTROS -->
    <div class="filters">
      <!-- ADMIN -->
      <input
        v-if="auth.user?.rol === 'admin'"
        v-model="filtros.alumno"
        placeholder="Buscar alumno"
        @input="buscar"
      />

      <input v-model="filtros.examen" placeholder="Buscar examen" @input="buscar" />
      <input type="date" v-model="filtros.fecha" @change="buscar" />
    </div>

    <!-- TABLA -->
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>#</th>
            <th v-if="auth.user?.rol === 'admin'">Alumno</th>
            <th>Examen</th>
            <th>Calificación</th>
            <th>Fecha</th>
            <th>Acciones</th>
          </tr>
        </thead>

        <tbody v-if="!loading">
          <tr v-for="(resultado, index) in registros" :key="resultado.id_resultado">
            <td>{{ index + 1 }}</td>
            <td v-if="auth.user?.rol === 'admin'">
              {{ resultado.nombre_alumno }}
            </td>
            <td>
              {{ resultado.nombre_examen }}
            </td>
            <td>
              <span class="badge"> {{ resultado.calificacion }}/10 </span>
            </td>
            <td>
              {{ formatearFecha(resultado.fecha_evaluacion) }}
            </td>
            <td>
              <button class="action-btn" @click="verRespuestas(resultado)">
                <Eye size="16" />
                Ver respuestas
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- LOADING -->
      <div v-if="loading" class="loading">Cargando resultados...</div>

      <!-- VACÍO -->
      <p v-if="!loading && registros.length === 0" class="empty">No se encontraron resultados</p>
    </div>

    <!-- PAGINACIÓN -->
    <div class="pagination">
      <button @click="page--" :disabled="page === 1">←</button>
      <span>{{ page }} / {{ totalPages }}</span>
      <button @click="page++" :disabled="page === totalPages">→</button>
    </div>

    <!-- MODAL -->
    <ModalTabla
      v-if="modalTabla"
      :title="modalTitle"
      :subtitle="modalSubtitle"
      :columns="modalColumns"
      :rows="modalRows"
      :loading="modalLoading"
      @close="modalTabla = false"
    />
  </div>
</template>

<style scoped>
.container {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 18px;
}

.subtitle {
  color: #6b7280;
  font-size: 14px;
}

.filters {
  display: flex;
  gap: 10px;
  margin-bottom: 18px;
  flex-wrap: wrap;
}

input,
select {
  padding: 10px;
  border-radius: 10px;
  border: 1px solid #ddd;
  min-width: 220px;
}

.table-container {
  background: white;
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 14px;
  text-align: left;
}

thead {
  background: #f9fafb;
}

tbody tr {
  border-top: 1px solid #f3f4f6;
}

tbody tr:hover {
  background: #f9fafb;
}

.badge {
  background: #ede9fe;
  color: #5b21b6;
  padding: 5px 10px;
  border-radius: 8px;
  font-size: 13px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 8px;

  border: none;

  background: #ede9fe;
  color: #5b21b6;

  padding: 8px 12px;

  border-radius: 8px;

  cursor: pointer;

  transition: 0.2s;
}

.action-btn:hover {
  background: #ddd6fe;
}

.pagination {
  margin-top: 20px;

  display: flex;
  justify-content: center;
  align-items: center;

  gap: 10px;
}

.pagination button {
  border: none;

  padding: 8px 12px;

  border-radius: 8px;

  cursor: pointer;

  background: #f3f4f6;
}

.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.empty {
  text-align: center;
  padding: 20px;
  color: #6b7280;
}

.loading {
  text-align: center;
  padding: 20px;
  color: #6b7280;
}
</style>
