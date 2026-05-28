<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

import api from '../services/api'
import { useAuthStore } from '../stores/autenticacion.js'

const auth = useAuthStore()
const router = useRouter()

const examenes = ref([])
const estudiantes = ref([])

const loading = ref(false)
const loadingSubmit = ref(false)

const inputFile = ref(null)

const errorServidor = ref('')
const successMessage = ref('')

const form = ref({
  id_examen: '',
  id_estudiante: '',
  archivo: null,
})

const errores = ref({
  id_examen: '',
  id_estudiante: '',
  archivo: '',
})

const validar = () => {
  errores.value = {
    id_examen: '',
    id_estudiante: '',
    archivo: '',
  }

  if (!form.value.id_examen) {
    errores.value.id_examen = 'Selecciona un examen'
  }

  if (!form.value.id_estudiante) {
    errores.value.id_estudiante = 'Seleccione a un estudiante'
  }

  if (!form.value.archivo) {
    errores.value.archivo = 'Debes subir la hoja de respuestas'
  }

  return !errores.value.id_examen && !errores.value.id_estudiante && !errores.value.archivo
}

const cargarDatos = async () => {
  loading.value = true
  errorServidor.value = ''

  try {
    const docenteRes = await api.get(`/docentes/usuario/${auth.user.user_id}`)

    const idDocente = docenteRes.data.id_docente

    const [examenesRes, estudiantesRes] = await Promise.all([
      api.get(`/examenes/docente/${idDocente}/activos`),
      api.get('/estudiantes/activos'),
    ])

    examenes.value = examenesRes.data
    estudiantes.value = estudiantesRes.data
  } catch (err) {
    console.error(err)

    errorServidor.value = err.response?.data?.detail || 'Error al cargar la información'
  } finally {
    loading.value = false
  }
}

const onFileChange = (e) => {
  form.value.archivo = e.target.files[0]
  form.value.archivo = file

  errores.value.archivo = ''
}

const limpiarFormulario = () => {
  form.value = {
    id_examen: '',
    id_estudiante: '',
    archivo: null,
  }

  if (inputFile.value) {
    inputFile.value.value = null
  }
}

const enviar = async () => {
  errorServidor.value = ''
  successMessage.value = ''

  if (!validar()) return

  loadingSubmit.value = true

  try {
    const formData = new FormData()

    formData.append('id_examen', form.value.id_examen)
    formData.append('id_estudiante', form.value.id_estudiante)
    formData.append('file', form.value.archivo)

    const response = await api.post('/evaluacion/omr', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })

    const examenSeleccionado = examenes.value.find((ex) => ex.id_examen === form.value.id_examen)

    const alumnoSeleccionado = estudiantes.value.find(
      (al) => al.id_estudiante === form.value.id_estudiante,
    )

    successMessage.value = 'La evaluación fue procesada correctamente'

    router.push({
      name: 'resultado-evaluacion',
      state: {
        resultado: response.data,
        examen: examenSeleccionado?.nombre_examen,
        alumno: `${alumnoSeleccionado?.nombre} ${alumnoSeleccionado?.apellido_paterno}`,
      },
    })

    limpiarFormulario()
  } catch (err) {
    console.error(err)

    errorServidor.value = err.response?.data?.detail || 'Ocurrió un error al procesar la hoja'
  } finally {
    loadingSubmit.value = false
  }
}

onMounted(() => {
  cargarDatos()
})
</script>

<template>
  <div class="container">
    <div class="card">
      <h2>Evaluación automática</h2>

      <!-- LOADING -->
      <div v-if="loading" class="loading">Cargando información...</div>

      <template v-else>
        <!-- ERROR SERVIDOR -->
        <div v-if="errorServidor" class="alert error-alert">
          {{ errorServidor }}
        </div>

        <!-- SUCCESS -->
        <div v-if="successMessage" class="alert success-alert">
          {{ successMessage }}
        </div>

        <!-- EXAMEN -->
        <div class="field">
          <label>Examen</label>

          <select v-model="form.id_examen">
            <option value="">Selecciona un examen</option>

            <option v-for="ex in examenes" :key="ex.id_examen" :value="ex.id_examen">
              {{ ex.nombre_examen }}
            </option>
          </select>

          <span v-if="errores.id_examen" class="error">
            {{ errores.id_examen }}
          </span>
        </div>

        <!-- ALUMNO -->
        <div class="field">
          <label>Alumno</label>

          <select v-model="form.id_estudiante">
            <option value="">Selecciona un alumno</option>

            <option v-for="al in estudiantes" :key="al.id_estudiante" :value="al.id_estudiante">
              {{ al.nombre }} {{ al.apellido_paterno }}
            </option>
          </select>

          <span v-if="errores.id_estudiante" class="error">
            {{ errores.id_estudiante }}
          </span>
        </div>

        <!-- ARCHIVO -->
        <div class="field">
          <label>Hoja de respuestas</label>
          <input ref="inputFile" type="file" accept=".jpg,.jpeg,.png,.pdf" @change="onFileChange" />
          <span v-if="errores.archivo" class="error">
            {{ errores.archivo }}
          </span>
        </div>

        <!-- BOTÓN -->
        <button @click="enviar" :disabled="loadingSubmit">
          {{ loadingSubmit ? 'Procesando evaluación...' : 'Subir evaluación' }}
        </button>
      </template>
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
  width: 420px;
  background: white;
  padding: 20px;
  border-radius: 14px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
}

h2 {
  margin-bottom: 20px;
  color: #111827;
}

.field {
  margin-bottom: 14px;
  display: flex;
  flex-direction: column;
}

label {
  margin-bottom: 6px;
  font-size: 14px;
  font-weight: 600;
  color: #374151;
}

select,
input {
  padding: 10px;
  border-radius: 10px;
  border: 1px solid #ddd;
  font-size: 14px;
}

select:focus,
input:focus {
  outline: none;
  border-color: #6366f1;
}

.error {
  color: red;
  font-size: 12px;
  margin-top: 4px;
}

button {
  width: 100%;
  padding: 12px;
  background: #6366f1;
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: 0.3s;
  font-size: 14px;
  font-weight: 600;
}

button:hover {
  background: #4f46e5;
}

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.loading {
  text-align: center;
  padding: 20px;
  color: #6b7280;
}

.alert {
  padding: 12px;
  border-radius: 10px;
  margin-bottom: 16px;
  font-size: 14px;
}

.error-alert {
  background: #fee2e2;
  color: #b91c1c;
  border: 1px solid #fecaca;
}

.success-alert {
  background: #dcfce7;
  color: #166534;
  border: 1px solid #bbf7d0;
}
</style>
