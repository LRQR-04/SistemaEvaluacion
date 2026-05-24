<script setup>
import { ref, watch, computed } from 'vue'
import api from '../services/api'

const props = defineProps({
  usuario: {
    type: Object,
    default: null,
  },
})

/* Modo */
const esEdicion = computed(() => !!props.usuario)

const emit = defineEmits(['close', 'success'])

const form = ref({
  nombre: '',
  apellido_paterno: '',
  apellido_materno: '',
  email: '',
  contrasenia: '',
  rol: 'estudiante',
  estado: 'activo',

  // Estudiante
  matricula: '',
  grupo: '',

  // Docente
  numero_usuario: '',
  especialidad: '',
})

watch(
  () => props.usuario,
  (usuario) => {
    if (usuario) {
      form.value = {
        nombre: usuario.nombre || '',
        apellido_paterno: usuario.apellido_paterno || '',
        apellido_materno: usuario.apellido_materno || '',
        email: usuario.email || '',
        contrasenia: '',
        rol: usuario.rol || 'estudiante',
        estado: usuario.estado || 'activo',

        // Estudiante
        matricula: usuario.estudiante?.matricula || '',
        grupo: usuario.estudiante?.grupo || '',

        // Docente
        numero_usuario: usuario.docente?.numero_usuario || '',
        especialidad: usuario.docente?.especialidad || '',
      }
    } else {
      form.value = {
        nombre: '',
        apellido_paterno: '',
        apellido_materno: '',
        email: '',
        contrasenia: '',
        rol: 'estudiante',
        estado: 'activo',
        matricula: '',
        grupo: '',
        numero_usuario: '',
        especialidad: '',
      }
    }
  },
  { immediate: true },
)

const errores = ref({
  nombre: '',
  apellido_paterno: '',
  apellido_materno: '',
  email: '',
  contrasenia: '',
  matricula: '',
  grupo: '',
  numero_usuario: '',
  especialidad: '',
})

const limpiarErrores = () => {
  errores.value = {
    nombre: '',
    apellido_paterno: '',
    apellido_materno: '',
    email: '',
    contrasenia: '',
    matricula: '',
    grupo: '',
    numero_usuario: '',
    especialidad: '',
  }
}

/* Validación */
const validar = () => {
  limpiarErrores()

  // Nombre
  if (!form.value.nombre.trim()) {
    errores.value.nombre = 'El campo es obligatorio'
  } else if (form.value.nombre.length < 3 || form.value.nombre.length > 100) {
    errores.value.nombre = 'Debe tener entre 3 y 100 caracteres'
  }

  // Apellido paterno
  if (!form.value.apellido_paterno.trim()) {
    errores.value.apellido_paterno = 'Completa el campo para continuar'
  } else if (!/^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$/.test(form.value.apellido_paterno)) {
    errores.value.apellido_paterno = 'El apellido solo puede contener letras'
  } else if (form.value.apellido_paterno.length < 3 || form.value.apellido_paterno.length > 100) {
    errores.value.apellido_paterno = 'Debe tener entre 3 y 100 caracteres'
  }

  // Apellido materno
  if (!form.value.apellido_materno.trim()) {
    errores.value.apellido_materno = 'Completa el campo para continuar'
  } else if (!/^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$/.test(form.value.apellido_materno)) {
    errores.value.apellido_materno = 'El apellido solo puede contener letras'
  } else if (form.value.apellido_materno.length < 3 || form.value.apellido_materno.length > 100) {
    errores.value.apellido_materno = 'Debe tener entre 3 y 100 caracteres'
  }

  // Email
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!form.value.email.trim()) {
    errores.value.email = 'El campo es obligatorio'
  } else if (!emailRegex.test(form.value.email)) {
    errores.value.email = 'Correo inválido'
  }

  // Contraseña
  const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.#_-]).{8,}$/

  if (!esEdicion.value) {
    if (!form.value.contrasenia) {
      errores.value.contrasenia = 'El campo es obligatorio'
    } else if (!passwordRegex.test(form.value.contrasenia)) {
      errores.value.contrasenia = 'Debe tener 8 caracteres, mayúscula, minúscula, número y símbolo'
    }
  }

  // Estudiante
  if (form.value.rol === 'estudiante') {
    if (!form.value.matricula.trim()) {
      errores.value.matricula = 'Completa el campo para continuar'
    } else if (!/^\d+$/.test(form.value.matricula)) {
      errores.value.matricula = 'El campo solo puede contener números'
    }

    if (!form.value.grupo.trim()) {
      errores.value.grupo = 'Completa el campo para continuar'
    }
  }

  // Docente
  if (form.value.rol === 'docente') {
    if (!form.value.numero_usuario.trim()) {
      errores.value.numero_usuario = 'Completa el campo para continuar'
    } else if (!/^\d+$/.test(form.value.numero_usuario)) {
      errores.value.numero_usuario = 'El campo solo puede contener números'
    }

    if (!form.value.especialidad.trim()) {
      errores.value.especialidad = 'Completa el campo para continuar'
    }
  }

  return Object.values(errores.value).every((error) => error === '')
}

const guardar = async () => {
  if (!validar()) return

  try {
    const payload = {
      nombre: form.value.nombre,
      apellido_paterno: form.value.apellido_paterno,
      apellido_materno: form.value.apellido_materno,
      email: form.value.email,
      estado: form.value.estado,
    }

    // Solo en creación
    if (!esEdicion.value) {
      payload.rol = form.value.rol
      payload.contrasenia = form.value.contrasenia
    }

    // Estudiante
    if (form.value.rol === 'estudiante') {
      payload.matricula = form.value.matricula
      payload.grupo = form.value.grupo
    }

    // Docente
    if (form.value.rol === 'docente') {
      payload.numero_usuario = form.value.numero_usuario
      payload.especialidad = form.value.especialidad
    }

    // Crear
    if (!esEdicion.value) {
      await api.post('/usuarios', payload)
      emit('success', 'Usuario creado correctamente')
    }

    // Editar
    else {
      await api.put(`/usuarios/${props.usuario.id_usuario}`, payload)
      emit('success', 'Usuario actualizado correctamente')
    }
    emit('close')
  } catch (err) {
    const msg = err.response?.data?.detail

    switch (msg) {
      case 'El correo ya está registrado':
        errores.value.email = 'El correo ya está registrado'
        break

      case 'La matrícula ya está registrada':
        errores.value.matricula = 'La matrícula ya está registrada'
        break

      case 'El número de usuario ya está registrado':
        errores.value.numero_usuario = 'El número de usuario ya está registrado'
        break

      default:
        emit('success', msg || 'Error del servidor', 'error')
        break
    }
  }
}
</script>

<template>
  <div class="overlay" @click.self="$emit('close')">
    <div class="modal-card">
      <div class="header">
        <h3>{{ esEdicion ? 'Editar usuario' : 'Crear usuario' }}</h3>
        <button class="close-btn" @click="$emit('close')">✕</button>
      </div>

      <!-- Form -->
      <div class="form-grid">
        <!-- Nombre -->
        <div class="field full">
          <label>Nombre</label>
          <input
            v-model="form.nombre"
            placeholder="Nombre"
            :class="{
              inputError: errores.nombre,
            }"
          />
          <span class="error-text">
            {{ errores.nombre }}
          </span>
        </div>

        <!-- Apellido paterno -->
        <div class="field">
          <label>Apellido paterno</label>
          <input
            v-model="form.apellido_paterno"
            placeholder="Apellido paterno"
            :class="{
              inputError: errores.apellido_paterno,
            }"
          />
          <span class="error-text">
            {{ errores.apellido_paterno }}
          </span>
        </div>

        <!-- Apellido materno -->
        <div class="field">
          <label>Apellido materno</label>
          <input
            v-model="form.apellido_materno"
            placeholder="Apellido materno"
            :class="{
              inputError: errores.apellido_materno,
            }"
          />
          <span class="error-text">
            {{ errores.apellido_materno }}
          </span>
        </div>

        <!-- Correo -->
        <div class="field full">
          <label>Correo</label>
          <input
            v-model="form.email"
            type="email"
            placeholder="Correo electrónico"
            :class="{
              inputError: errores.email,
            }"
          />
          <span class="error-text">
            {{ errores.email }}
          </span>
        </div>

        <!-- Password -->
        <div v-if="!esEdicion" class="field full">
          <label>Contraseña</label>

          <input
            v-model="form.contrasenia"
            type="password"
            placeholder="Contraseña"
            :class="{
              inputError: errores.contrasenia,
            }"
          />

          <span class="error-text">
            {{ errores.contrasenia }}
          </span>
        </div>

        <!-- Rol -->
        <div class="field">
          <label>Rol</label>

          <!-- CREAR -->
          <select v-if="!esEdicion" v-model="form.rol">
            <option value="estudiante">Estudiante</option>
            <option value="docente">Docente</option>
            <option value="admin">Administrador</option>
          </select>

          <!-- EDITAR -->
          <div v-else class="role-display">
            <span class="badge">
              {{ form.rol }}
            </span>
            <small> El rol no puede modificarse </small>
          </div>
        </div>

        <!-- ESTUDIANTE -->
        <template v-if="form.rol === 'estudiante'">
          <div class="field">
            <label>Matrícula</label>
            <input
              v-model="form.matricula"
              placeholder="Matrícula"
              :class="{
                inputError: errores.matricula,
              }"
            />
            <span class="error-text">
              {{ errores.matricula }}
            </span>
          </div>

          <div class="field">
            <label>Grupo</label>
            <input
              v-model="form.grupo"
              placeholder="Grupo"
              :class="{
                inputError: errores.grupo,
              }"
            />
            <span class="error-text">
              {{ errores.grupo }}
            </span>
          </div>
        </template>

        <!-- DOCENTE -->
        <template v-if="form.rol === 'docente'">
          <div class="field">
            <label> Número de usuario </label>
            <input
              v-model="form.numero_usuario"
              placeholder="Número de usuario"
              :class="{
                inputError: errores.numero_usuario,
              }"
            />
            <span class="error-text">
              {{ errores.numero_usuario }}
            </span>
          </div>

          <div class="field">
            <label> Especialidad </label>
            <input
              v-model="form.especialidad"
              placeholder="Especialidad"
              :class="{
                inputError: errores.especialidad,
              }"
            />
            <span class="error-text">
              {{ errores.especialidad }}
            </span>
          </div>
        </template>
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
  width: 750px;
  max-width: 95%;
  max-height: 90vh;
  overflow-y: auto;
  border-radius: 18px;
  padding: 24px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  animation: fadeIn 0.2s ease;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 20px;
}

.subtitle {
  color: #6b7280;
  font-size: 14px;
  margin-top: 4px;
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
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.field {
  display: flex;
  flex-direction: column;
}

.field.full {
  grid-column: span 2;
}

label {
  margin-bottom: 6px;
  font-size: 14px;
  font-weight: 500;
}

input,
select {
  padding: 11px 12px;
  border-radius: 10px;
  border: 1px solid #d1d5db;
  outline: none;
  transition: 0.2s;
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
  margin-top: 24px;
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

.role-display {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 10px 12px;
  border-radius: 10px;
  background: #f3f4f6;
}

.role-display small {
  color: #6b7280;
  font-size: 12px;
}

.badge {
  width: fit-content;
  background: #ede9fe;
  color: #5b21b6;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  text-transform: capitalize;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
