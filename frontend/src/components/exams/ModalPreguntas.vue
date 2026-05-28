<script setup>
import { ref, watch } from 'vue'
import api from '../../services/api'
import { Pencil, Plus, Loader2 } from 'lucide-vue-next'

const props = defineProps({
  examen: Object,
})

const emit = defineEmits(['close', 'success'])

const preguntas = ref([])
const loading = ref(false)

const modoEdicion = ref(false)

const form = ref({
  id_pregunta: null,
  pregunta: '',
  opcion_a: '',
  opcion_b: '',
  opcion_c: '',
  respuesta_correcta: 'a',
  estatus: 'activa',
})

const errores = ref({
  pregunta: '',
  opcion_a: '',
  opcion_b: '',
  opcion_c: '',
})

const limpiarErrores = () => {
  errores.value = {
    pregunta: '',
    opcion_a: '',
    opcion_b: '',
    opcion_c: '',
  }
}

const validar = () => {
  limpiarErrores()

  if (!form.value.pregunta.trim()) {
    errores.value.pregunta = 'La pregunta es obligatoria'
  } else if (form.value.pregunta.length < 5) {
    errores.value.pregunta = 'La pregunta es demasiado corta'
  }

  if (!form.value.opcion_a.trim()) {
    errores.value.opcion_a = 'La opción A es obligatoria'
  }

  if (!form.value.opcion_b.trim()) {
    errores.value.opcion_b = 'La opción B es obligatoria'
  }

  if (!form.value.opcion_c.trim()) {
    errores.value.opcion_c = 'La opción C es obligatoria'
  }

  return Object.values(errores.value).every((e) => e === '')
}

const cargarPreguntas = async () => {
  if (!props.examen) return

  loading.value = true

  try {
    const res = await api.get(`/preguntas/examen/${props.examen.id_examen}`)
    preguntas.value = res.data
  } finally {
    loading.value = false
  }
}

watch(
  () => props.examen,
  () => cargarPreguntas(),
  { immediate: true },
)

const limpiar = () => {
  form.value = {
    id_pregunta: null,
    pregunta: '',
    opcion_a: '',
    opcion_b: '',
    opcion_c: '',
    respuesta_correcta: 'a',
    estatus: 'activa',
  }

  limpiarErrores()

  modoEdicion.value = false
}

const editar = (p) => {
  form.value = { ...p }
  modoEdicion.value = true
}

const cambiarEstado = async (pregunta) => {
  const estadoActual = pregunta.estatus

  const nuevoEstado = estadoActual === 'activa' ? 'inactiva' : 'activa'

  const confirmar = confirm(
    `¿Deseas ${nuevoEstado === 'activa' ? 'activar' : 'desactivar'} esta pregunta?`,
  )

  /* CANCELADO */
  if (!confirmar) {
    return
  }

  try {
    await api.put(`/preguntas/${pregunta.id_pregunta}`, {
      ...pregunta,
      estatus: nuevoEstado,
    })

    pregunta.estatus = nuevoEstado

    emit(
      'success',
      `Pregunta ${nuevoEstado === 'activa' ? 'activada' : 'desactivada'} correctamente`,
    )
  } catch (err) {
    emit('success', err.response?.data?.detail || 'Error al actualizar estado', 'error')
  }
}

const guardar = async () => {
  if (!validar()) return

  try {
    const payload = {
      pregunta: form.value.pregunta,
      opcion_a: form.value.opcion_a,
      opcion_b: form.value.opcion_b,
      opcion_c: form.value.opcion_c,
      respuesta_correcta: form.value.respuesta_correcta,
      estatus: form.value.estatus,
      id_examen: props.examen.id_examen,
    }

    if (modoEdicion.value) {
      await api.put(`/preguntas/${form.value.id_pregunta}`, payload)

      emit('success', 'Pregunta actualizada')
    } else {
      await api.post('/preguntas', payload)

      emit('success', 'Pregunta creada')
    }

    limpiar()
    cargarPreguntas()
  } catch (err) {
    const msg = err.response?.data?.detail

    emit('success', msg || 'Error al guardar la pregunta', 'error')
  }
}
</script>

<template>
  <div class="overlay" @click.self="$emit('close')">
    <div class="modal">
      <!-- HEADER -->
      <div class="header">
        <div>
          <h3>Banco de preguntas</h3>

          <p class="subtitle">
            {{ examen?.nombre_examen }}
          </p>
        </div>

        <button class="close" @click="$emit('close')">✕</button>
      </div>

      <div class="content">
        <!-- LISTA -->
        <div class="list">
          <div v-if="loading" class="loading">
            <Loader2 class="spin" size="18" />
            Cargando preguntas...
          </div>

          <div v-else-if="preguntas.length === 0" class="empty">No hay preguntas registradas</div>

          <div v-else v-for="p in preguntas" :key="p.id_pregunta" class="card">
            <div class="card-top">
              <span class="badge">
                {{ p.estatus }}
              </span>

              <!-- SWITCH -->
              <label class="switch">
                <input
                  type="checkbox"
                  :checked="p.estatus === 'activa'"
                  @click.prevent="cambiarEstado(p)"
                />
                <span class="slider"></span>
              </label>
            </div>

            <p class="question">
              {{ p.pregunta }}
            </p>

            <div class="options">
              <span>A) {{ p.opcion_a }}</span>
              <span>B) {{ p.opcion_b }}</span>
              <span>C) {{ p.opcion_c }}</span>
            </div>

            <div class="footer">
              <span class="correcta"> Correcta: {{ p.respuesta_correcta.toUpperCase() }} </span>

              <div class="actions">
                <button @click="editar(p)">
                  <Pencil size="14" />
                  Editar
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- FORM -->
        <div class="form">
          <h4>
            {{ modoEdicion ? 'Editar pregunta' : 'Nueva pregunta' }}
          </h4>

          <!-- Pregunta -->
          <div class="field">
            <input
              v-model="form.pregunta"
              placeholder="Escribe la pregunta"
              :class="{ inputError: errores.pregunta }"
            />

            <span class="error-text">
              {{ errores.pregunta }}
            </span>
          </div>

          <!-- Opciones -->
          <div class="field">
            <input
              v-model="form.opcion_a"
              placeholder="Opción A"
              :class="{ inputError: errores.opcion_a }"
            />

            <span class="error-text">
              {{ errores.opcion_a }}
            </span>
          </div>

          <div class="field">
            <input
              v-model="form.opcion_b"
              placeholder="Opción B"
              :class="{ inputError: errores.opcion_b }"
            />

            <span class="error-text">
              {{ errores.opcion_b }}
            </span>
          </div>

          <div class="field">
            <input
              v-model="form.opcion_c"
              placeholder="Opción C"
              :class="{ inputError: errores.opcion_c }"
            />

            <span class="error-text">
              {{ errores.opcion_c }}
            </span>
          </div>

          <!-- RESPUESTA -->
          <select v-model="form.respuesta_correcta">
            <option value="a">A</option>
            <option value="b">B</option>
            <option value="c">C</option>
          </select>

          <!-- BOTONES -->
          <button class="btn-primary" @click="guardar">
            <Plus size="14" />

            {{ modoEdicion ? 'Actualizar' : 'Crear' }}
          </button>

          <button v-if="modoEdicion" class="btn-secondary" @click="limpiar">
            Cancelar edición
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal {
  width: 820px;
  max-width: 92%;
  background: white;
  border-radius: 16px;
  padding: 18px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.18);
}

.header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 14px;
}

.subtitle {
  font-size: 13px;
  color: #6b7280;
}

.close {
  border: none;
  background: #f3f4f6;
  width: 34px;
  height: 34px;
  border-radius: 10px;
  cursor: pointer;
}

.content {
  display: grid;
  grid-template-columns: 1.2fr 0.9fr;
  gap: 14px;
}

.list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-height: 60vh;
  overflow-y: auto;
}

.card {
  border: 1px solid #e5e7eb;
  padding: 12px;
  border-radius: 12px;
}

.card-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.question {
  font-weight: 600;
  margin-bottom: 8px;
  font-size: 14px;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 13px;
  color: #6b7280;
  margin-bottom: 10px;
}

.footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.badge {
  background: #ede9fe;
  color: #5b21b6;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 11px;
  text-transform: capitalize;
}

.correcta {
  font-size: 12px;
  color: #4b5563;
}

.actions button {
  border: none;
  background: #f3f4f6;
  padding: 7px 10px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.field {
  display: flex;
  flex-direction: column;
}

input,
select {
  padding: 10px;
  border: 1px solid #d1d5db;
  border-radius: 10px;
  outline: none;
}

input:focus,
select:focus {
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.12);
}

.inputError {
  border-color: #ef4444;
}

.error-text {
  font-size: 12px;
  color: #ef4444;
  margin-top: 4px;
}

.btn-primary {
  border: none;
  background: linear-gradient(135deg, #6366f1, #7c3aed);
  color: white;
  padding: 10px;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  justify-content: center;
  gap: 6px;
  align-items: center;
}

.btn-secondary {
  border: none;
  background: #e5e7eb;
  padding: 10px;
  border-radius: 10px;
  cursor: pointer;
}

.loading,
.empty {
  padding: 20px;
  text-align: center;
  color: #6b7280;
}

.spin {
  animation: spin 1s linear infinite;
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
  inset: 0;
  background: #d1d5db;
  border-radius: 999px;
  transition: 0.3s;
  cursor: pointer;
}

.slider::before {
  content: '';
  position: absolute;
  width: 16px;
  height: 16px;
  left: 3px;
  top: 3px;
  background: white;
  border-radius: 50%;
  transition: 0.3s;
}

.switch input:checked + .slider {
  background: #22c55e;
}

.switch input:checked + .slider::before {
  transform: translateX(20px);
}

@keyframes spin {
  100% {
    transform: rotate(360deg);
  }
}
</style>
