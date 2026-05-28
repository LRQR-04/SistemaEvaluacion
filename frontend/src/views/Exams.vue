<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import api from '../services/api'

import { useAuthStore } from '../stores/autenticacion'

import Alerta from '../components/Alerta.vue'
import TablaExamenes from '../components/exams/TablaExamenes.vue'
import GridExamenes from '../components/exams/GridExamenes.vue'
import ModalExamen from '../components/exams/ModalExamen.vue'
import ModalPreguntas from '../components/exams/ModalPreguntas.vue'
import ModalResultados from '../components/exams/ModalResultados.vue'
import ModalTabla from '../components/ModalTabla.vue'

const auth = useAuthStore()
const examenes = ref([])

const page = ref(1)
const total = ref(0)

const modalPreguntas = ref(false)
const examenPreguntas = ref(null)

const modalExamen = ref(false)
const examenSeleccionado = ref(null)

const modalResultados = ref(false)
const examenResultados = ref(null)

const modalDinamico = ref(false)
const preguntas = ref([])
const loadingPreguntas = ref(false)
const evaluacionSeleccionada = ref(null)

const columnasPreguntas = [
  {
    key: 'pregunta',
    label: 'Pregunta',
  },

  {
    key: 'opcion_a',
    label: 'Opción A',
  },

  {
    key: 'opcion_b',
    label: 'Opción B',
  },

  {
    key: 'opcion_c',
    label: 'Opción C',
  },

  {
    key: 'respuesta_correcta',
    label: 'Correcta',
  },

  {
    key: 'estatus',
    label: 'Estatus',
  },
]

const alertMsg = ref('')
const alertType = ref('success')

const filtros = ref({
  docente: '',
  nombre_examen: '',
  fecha_aplicacion: '',
  total_reactivos: '',
  estatus: '',
})

const esAdmin = computed(() => auth.user?.rol === 'admin')

const endpoint = computed(() => '/examenes')

const cargar = async () => {
  try {
    const { data } = await api.get(endpoint.value, {
      params: {
        page: page.value,
        limit: 10,
        ...filtros.value,
      },
    })

    examenes.value = data.data
    total.value = data.total
  } catch (error) {
    mostrarAlerta(error.response?.data?.detail || 'Error al cargar exámenes', 'error')
  }
}

onMounted(() => {
  if (auth.user) cargar()
})

watch(page, cargar)

watch(
  () => auth.user,
  (val) => {
    if (val) {
      page.value = 1
      cargar()
    }
  },
)

const buscar = () => {
  page.value = 1
  cargar()
}

const nuevo = () => {
  examenSeleccionado.value = null
  modalExamen.value = true
}

const editar = (examen) => {
  examenSeleccionado.value = examen
  modalExamen.value = true
}

const abrirPreguntas = (examen) => {
  examenPreguntas.value = examen
  modalPreguntas.value = true
}

const cerrarPreguntas = () => {
  modalPreguntas.value = false
  examenPreguntas.value = null
}

const abrirResultados = (examen) => {
  examenResultados.value = examen
  modalResultados.value = true
}

const cerrarResultados = () => {
  modalResultados.value = false
  examenResultados.value = null
}

const abrirModalDinamico = async (examen) => {
  evaluacionSeleccionada.value = examen
  modalDinamico.value = true
  loadingPreguntas.value = true

  try {
    const { data } = await api.get(`/preguntas/examen/${examen.id_examen}`)

    preguntas.value = data
  } catch (error) {
    mostrarAlerta('Error al cargar preguntas', 'error')
  } finally {
    loadingPreguntas.value = false
  }
}

const cerrarModalDinamico = () => {
  modalDinamico.value = false
  preguntas.value = []
  evaluacionSeleccionada.value = null
}

const mostrarAlerta = (msg, type = 'success') => {
  alertMsg.value = msg
  alertType.value = type
  setTimeout(() => (alertMsg.value = ''), 3000)
}

const handleSuccess = async (msg, type = 'success') => {
  mostrarAlerta(msg, type)
  await cargar()
}

const totalPages = computed(() => {
  const pages = Math.ceil(total.value / 10)
  return pages > 0 ? pages : 1
})
</script>

<template>
  <div class="container">
    <Alerta v-if="alertMsg" :message="alertMsg" :type="alertType" />

    <div class="header">
      <div>
        <h2>Exámenes</h2>
        <p class="subtitle">Gestión de evaluaciones</p>
      </div>

      <button v-if="!esAdmin" class="btn-primary" @click="nuevo">+ Nuevo examen</button>
    </div>

    <!-- Filtros -->
    <div class="filters">
      <input v-model="filtros.nombre_examen" placeholder="Buscar examen" @input="buscar" />

      <input v-model="filtros.fecha_aplicacion" type="date" @change="buscar" />

      <select v-model="filtros.estatus" @change="buscar">
        <option value="">Todos</option>
        <option value="activo">Activo</option>
        <option value="inactivo">Inactivo</option>
        <option value="borrador">Borrador</option>
      </select>
    </div>

    <!-- Tabla / Grid -->
    <TablaExamenes v-if="esAdmin" :examenes="examenes" @preguntas="abrirModalDinamico" />

    <GridExamenes
      v-else
      :examenes="examenes"
      @editar="editar"
      @preguntas="abrirPreguntas"
      @resultados="abrirResultados"
    />

    <!-- Paginación -->
    <div class="pagination">
      <button @click="page--" :disabled="page === 1">←</button>
      <span>{{ page }} / {{ totalPages }}</span>
      <button @click="page++" :disabled="page === totalPages">→</button>
    </div>

    <!-- Modals -->
    <ModalExamen
      v-if="modalExamen"
      :examen="examenSeleccionado"
      @close="modalExamen = false"
      @success="handleSuccess"
    />

    <ModalPreguntas
      v-if="modalPreguntas"
      :examen="examenPreguntas"
      @close="cerrarPreguntas"
      @success="handleSuccess"
    />

    <ModalResultados
      v-if="modalResultados"
      :examen="examenResultados"
      @close="cerrarResultados"
      @success="handleSuccess"
    />

    <ModalTabla
      v-if="modalDinamico"
      title="Preguntas del examen"
      :subtitle="evaluacionSeleccionada?.nombre_examen"
      :columns="columnasPreguntas"
      :rows="preguntas"
      :loading="loadingPreguntas"
      empty-message="No hay preguntas registradas"
      width="1100px"
      @close="cerrarModalDinamico"
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

.tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 18px;
}

.tab {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border: none;
  border-radius: 10px;
  background: #f3f4f6;
  cursor: pointer;
  transition: 0.2s;
}

.tab.active {
  background: linear-gradient(135deg, #6366f1, #7c3aed);
  color: white;
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
  min-width: 200px;
  outline: none;
  transition: 0.2s;
}

input:focus,
select:focus {
  border-color: #6366f1;
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
  padding: 4px 8px;
  border-radius: 8px;
  font-size: 12px;
}

.btn-primary {
  background: linear-gradient(135deg, #6366f1, #7c3aed);
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 10px;
  cursor: pointer;
  transition: 0.2s;
}

.btn-primary:hover {
  opacity: 0.9;
}

.icon-btn {
  border: none;
  background: none;
  cursor: pointer;
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
  transition: 0.2s;
}

.pagination button:hover {
  background: #e5e7eb;
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

.switch {
  position: relative;
  display: inline-block;
  width: 42px;
  height: 22px;
}

.switch input {
  display: none;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: #d1d5db;
  transition: 0.3s;
  border-radius: 20px;
}

.slider::before {
  content: '';
  position: absolute;
  width: 16px;
  height: 16px;
  left: 3px;
  bottom: 3px;
  background: white;
  border-radius: 50%;
  transition: 0.3s;
}

input:checked + .slider {
  background: #22c55e;
}

input:checked + .slider::before {
  transform: translateX(20px);
}

.avatar {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: #6366f1;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
}

@media (max-width: 768px) {
  .filters {
    flex-direction: column;
  }

  input,
  select {
    min-width: 100%;
  }
}
</style>
