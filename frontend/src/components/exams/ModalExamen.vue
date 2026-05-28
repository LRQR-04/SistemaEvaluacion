<script setup>
import { ref, watch, computed } from 'vue'
import api from '../../services/api'

/* Props */
const props = defineProps({
  examen: {
    type: Object,
    default: null,
  },
})

const emit = defineEmits(['close', 'success'])

/* Modo */
const esEdicion = computed(() => !!props.examen)

// Rango de fechas
const today = new Date()
today.setHours(0, 0, 0, 0)

const minFecha = today.toISOString().split('T')[0]

const maxFechaObj = new Date(today)
maxFechaObj.setFullYear(maxFechaObj.getFullYear() + 1)

const maxFecha = maxFechaObj.toISOString().split('T')[0]

const form = ref({
  nombre_examen: '',
  fecha_aplicacion: '',
  estatus: 'activo',
})

const errores = ref({
  nombre_examen: '',
  fecha_aplicacion: '',
})

const formatearFechaLocal = (fecha) => {
  if (!fecha) return ''
  return fecha.split('T')[0] // evita UTC shift
}

watch(
  () => props.examen,
  (examen) => {
    if (examen) {
      form.value = {
        nombre_examen: examen.nombre_examen || '',
        fecha_aplicacion: formatearFechaLocal(examen.fecha_aplicacion),
        estatus: examen.estatus || 'activo',
      }
    } else {
      form.value = {
        nombre_examen: '',
        fecha_aplicacion: '',
        estatus: 'activo',
      }
    }
  },
  { immediate: true },
)

const limpiarErrores = () => {
  errores.value = {
    nombre_examen: '',
    fecha_aplicacion: '',
  }
}

const validar = () => {
  limpiarErrores()

  if (!form.value.nombre_examen.trim()) {
    errores.value.nombre_examen = 'Completa el campo para continuar'
  }

  if (!form.value.fecha_aplicacion) {
    errores.value.fecha_aplicacion = 'Completa el campo para continuar'
  } else {
    const fechaSeleccionada = new Date(form.value.fecha_aplicacion)
    const min = new Date(minFecha)
    const max = new Date(maxFecha)

    if (fechaSeleccionada < min) {
      errores.value.fecha_aplicacion = 'No puedes seleccionar fechas pasadas'
    }

    if (fechaSeleccionada > max) {
      errores.value.fecha_aplicacion = 'La fecha no puede ser mayor a 1 año desde hoy'
    }
  }

  return Object.values(errores.value).every((e) => e === '')
}

const guardar = async () => {
  if (!validar()) return

  try {
    const payload = {
      nombre_examen: form.value.nombre_examen,
      fecha_aplicacion: form.value.fecha_aplicacion,
      estatus: form.value.estatus,
    }

    if (!esEdicion.value) {
      await api.post('/examenes', payload)
      emit('success', 'Examen creado correctamente')
    } else {
      await api.put(`/examenes/${props.examen.id_examen}`, payload)
      emit('success', 'Examen actualizado correctamente')
    }

    emit('close')
  } catch (err) {
    emit('error', 'Error al guardar examen')
  }
}
</script>

<template>
  <div class="overlay" @click.self="$emit('close')">
    <div class="modal-card">
      <div class="header">
        <h3>
          {{ esEdicion ? 'Editar examen' : 'Crear examen' }}
        </h3>

        <button class="close-btn" @click="$emit('close')">✕</button>
      </div>

      <!-- FORM -->
      <div class="form-grid">
        <!-- Nombre -->
        <div class="field full">
          <label>Nombre del examen</label>
          <input
            v-model="form.nombre_examen"
            placeholder="Ej: Examen de Matemáticas"
            :class="{ inputError: errores.nombre_examen }"
          />
          <span class="error-text">{{ errores.nombre_examen }}</span>
        </div>

        <!-- Fecha -->
        <div class="field">
          <label>Fecha de aplicación</label>
          <input
            v-model="form.fecha_aplicacion"
            type="date"
            :min="minFecha"
            :max="maxFecha"
            :class="{ inputError: errores.fecha_aplicacion }"
          />
          <span class="error-text">{{ errores.fecha_aplicacion }}</span>
        </div>

        <!-- Estatus -->
        <div class="field">
          <label>Estatus</label>
          <select v-model="form.estatus">
            <option value="activo">Activo</option>
            <option value="inactivo">Inactivo</option>
            <option value="borrador">Borrador</option>
          </select>
        </div>
      </div>

      <!-- BOTONES -->
      <div class="actions">
        <button class="btn-secondary" @click="$emit('close')">Cancelar</button>

        <button class="btn-primary" @click="guardar">
          {{ esEdicion ? 'Actualizar' : 'Guardar' }}
        </button>
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
  backdrop-filter: blur(4px);
}

.modal-card {
  background: white;
  width: 520px;
  max-width: 95%;
  border-radius: 18px;
  padding: 24px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 18px;
}

.close-btn {
  border: none;
  background: #f3f4f6;
  width: 34px;
  height: 34px;
  border-radius: 10px;
  cursor: pointer;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 14px;
}

.field {
  display: flex;
  flex-direction: column;
}

.field.full {
  grid-column: span 1;
}

label {
  font-size: 14px;
  margin-bottom: 6px;
}

input,
select {
  padding: 11px;
  border-radius: 10px;
  border: 1px solid #d1d5db;
  outline: none;
}

input:focus,
select:focus {
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
}

.inputError {
  border-color: #ef4444;
}

.error-text {
  color: #ef4444;
  font-size: 12px;
  margin-top: 4px;
}

.actions {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.btn-primary {
  background: linear-gradient(135deg, #6366f1, #7c3aed);
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 10px;
  cursor: pointer;
}

.btn-secondary {
  background: #e5e7eb;
  border: none;
  padding: 10px 16px;
  border-radius: 10px;
  cursor: pointer;
}

.btn-primary:hover {
  transform: translateY(-1px);
}

.btn-secondary:hover {
  background: #d1d5db;
}
</style>
