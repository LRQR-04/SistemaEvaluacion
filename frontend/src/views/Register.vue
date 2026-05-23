<script setup>
import { ref, watch } from 'vue'
import api from '../services/api'
import { useRouter } from 'vue-router'

const nombre = ref('')
const apellidoPaterno = ref('')
const apellidoMaterno = ref('')
const correo = ref('')
const contrasenia = ref('')
const rol = ref('estudiante')

// Campos para estudiante
const matricula = ref('')
const grupo = ref('')

// Campos para docente
const numeroUsuario = ref('')
const especialidad = ref('')

const errores = ref({
  nombre: '',
  apellidoPaterno: '',
  apellidoMaterno: '',
  correo: '',
  contrasenia: '',
  matricula: '',
  grupo: '',
  numeroUsuario: '',
  especialidad: '',
})

const router = useRouter()

const limpiarErrores = () => {
  errores.value = {
    nombre: '',
    apellidoPaterno: '',
    apellidoMaterno: '',
    correo: '',
    contrasenia: '',
    matricula: '',
    grupo: '',
    numeroUsuario: '',
    especialidad: '',
  }
}

const validar = () => {
  limpiarErrores()

  // Nombre
  if (!nombre.value.trim()) {
    errores.value.nombre = 'Completa el campo para continuar'
  } else if (!/^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$/.test(nombre.value)) {
    errores.value.nombre = 'El nombre solo puede contener letras'
  } else if (nombre.value.length < 3 || nombre.value.length > 100) {
    errores.value.nombre = 'Debe tener entre 3 y 100 caracteres'
  }

  // Apellido paterno
  if (!apellidoPaterno.value.trim()) {
    errores.value.apellidoPaterno = 'Completa el campo para continuar'
  } else if (!/^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$/.test(apellidoPaterno.value)) {
    errores.value.apellidoPaterno = 'El apellido solo puede contener letras'
  } else if (apellidoPaterno.value.length < 3 || apellidoPaterno.value.length > 100) {
    errores.value.apellidoPaterno = 'Debe tener entre 3 y 100 caracteres'
  }

  // Apellido materno
  if (!apellidoMaterno.value.trim()) {
    errores.value.apellidoMaterno = 'Completa el campo para continuar'
  } else if (!/^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$/.test(apellidoMaterno.value)) {
    errores.value.apellidoMaterno = 'El apellido solo puede contener letras'
  } else if (apellidoMaterno.value.length < 3 || apellidoMaterno.value.length > 100) {
    errores.value.apellidoMaterno = 'Debe tener entre 3 y 100 caracteres'
  }

  // Correo
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

  if (!correo.value.trim()) {
    errores.value.correo = 'Completa el campo para continuar'
  } else if (!emailRegex.test(correo.value)) {
    errores.value.correo = 'Correo inválido'
  }

  // Password
  const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.#_-]).{8,}$/

  if (!contrasenia.value) {
    errores.value.contrasenia = 'Completa el campo para continuar'
  } else if (!passwordRegex.test(contrasenia.value)) {
    errores.value.contrasenia = 'Debe tener 8 caracteres, mayúscula, minúscula, número y símbolo'
  }

  // Validaciones para estudiante
  if (rol.value === 'estudiante') {
    if (!matricula.value.trim()) {
      errores.value.matricula = 'Completa el campo para continuar'
    } else if (!/^\d+$/.test(matricula.value)) {
      errores.value.matricula = 'El campo solo puede contener números'
    }

    if (!grupo.value.trim()) {
      errores.value.grupo = 'Completa el campo para continuar'
    }
  }

  // Validaciones para docente
  if (rol.value === 'docente') {
    if (!numeroUsuario.value.trim()) {
      errores.value.numeroUsuario = 'Completa el campo para continuar'
    } else if (!/^\d+$/.test(numeroUsuario.value)) {
      errores.value.numeroUsuario = 'El campo solo puede contener números'
    }

    if (!especialidad.value.trim()) {
      errores.value.especialidad = 'Completa el campo para continuar'
    }
  }

  return Object.values(errores.value).every((error) => error === '')
}

// Validación automática
watch(
  [
    nombre,
    apellidoPaterno,
    apellidoMaterno,
    correo,
    contrasenia,
    rol,
    matricula,
    grupo,
    numeroUsuario,
    especialidad,
  ],
  () => {
    validar()
  },
)

const registro = async () => {
  if (!validar()) return

  try {
    const payload = {
      nombre: nombre.value,
      apellido_paterno: apellidoPaterno.value,
      apellido_materno: apellidoMaterno.value,
      email: correo.value,
      contrasenia: contrasenia.value,
      rol: rol.value,
    }

    // Datos extra según el rol
    if (rol.value === 'estudiante') {
      payload.matricula = matricula.value
      payload.grupo = grupo.value
    }

    if (rol.value === 'docente') {
      payload.numero_usuario = numeroUsuario.value
      payload.especialidad = especialidad.value
    }

    await api.post('/auth/registro', payload)
    alert('Registro exitoso')
    router.push('/login')
  } catch (err) {
    const msg = err.response?.data?.detail

    switch (msg) {
      case 'El correo ya está registrado':
        errores.value.correo = 'El correo ya está registrado'
        break

      case 'La matrícula ya está registrada':
        errores.value.matricula = 'La matrícula ya está registrada'
        break

      case 'El número de usuario ya está registrado':
        errores.value.numeroUsuario = 'El número de usuario ya está registrado'
        break

      default:
        errores.value.correo = 'Error al registrar usuario'
        break
    }
  }
}
</script>

<template>
  <div class="register-container">
    <div class="register-card">
      <h2>Crear cuenta</h2>
      <p class="subtitle">Completa los datos para registrarte</p>

      <div class="form-grid">
        <!-- Nombre -->
        <div class="field">
          <input v-model="nombre" placeholder="Nombre" :class="{ inputError: errores.nombre }" />
          <span class="error-text">{{ errores.nombre }}</span>
        </div>

        <!-- Apellido paterno -->
        <div class="field">
          <input
            v-model="apellidoPaterno"
            placeholder="Apellido paterno"
            :class="{ inputError: errores.apellidoPaterno }"
          />
          <span class="error-text">{{ errores.apellidoPaterno }}</span>
        </div>

        <!-- Apellido materno -->
        <div class="field">
          <input
            v-model="apellidoMaterno"
            placeholder="Apellido materno"
            :class="{ inputError: errores.apellidoMaterno }"
          />
          <span class="error-text">{{ errores.apellidoMaterno }}</span>
        </div>

        <!-- Correo -->
        <div class="field full-width">
          <input
            v-model="correo"
            type="email"
            placeholder="Correo electrónico"
            :class="{ inputError: errores.correo }"
          />
          <span class="error-text">{{ errores.correo }}</span>
        </div>

        <!-- Contraseña -->
        <div class="field full-width">
          <input
            v-model="contrasenia"
            type="password"
            placeholder="Contraseña"
            :class="{ inputError: errores.contrasenia }"
          />
          <span class="error-text">{{ errores.contrasenia }}</span>
        </div>

        <!-- Rol -->
        <div class="field full-width">
          <select v-model="rol">
            <option value="estudiante">Estudiante</option>
            <option value="docente">Docente</option>
          </select>
        </div>

        <!-- Campos estudiante -->
        <template v-if="rol === 'estudiante'">
          <div class="field">
            <input
              v-model="matricula"
              placeholder="Matrícula"
              :class="{ inputError: errores.matricula }"
            />
            <span class="error-text">{{ errores.matricula }}</span>
          </div>

          <div class="field">
            <input v-model="grupo" placeholder="Grupo" :class="{ inputError: errores.grupo }" />
            <span class="error-text">{{ errores.grupo }}</span>
          </div>
        </template>

        <!-- Campos docente -->
        <template v-if="rol === 'docente'">
          <div class="field">
            <input
              v-model="numeroUsuario"
              placeholder="Número de usuario"
              :class="{ inputError: errores.numeroUsuario }"
            />
            <span class="error-text">{{ errores.numeroUsuario }}</span>
          </div>

          <div class="field">
            <input
              v-model="especialidad"
              placeholder="Área de especialidad"
              :class="{ inputError: errores.especialidad }"
            />
            <span class="error-text">{{ errores.especialidad }}</span>
          </div>
        </template>
      </div>

      <button @click="registro">Registrarse</button>

      <p class="login-text">
        ¿Ya tienes cuenta?
        <router-link to="/login">Inicia sesión</router-link>
      </p>
    </div>
  </div>
</template>

<style scoped>
.register-container {
  min-height: 100vh;
  padding: 30px 15px;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #9333ea, #4f46e5);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.register-card {
  background: white;
  padding: 2rem;
  width: 100%;
  max-width: 700px;
  border-radius: 18px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

.register-card h2 {
  text-align: center;
  margin-bottom: 0.5rem;
}

.subtitle {
  text-align: center;
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 2rem;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.full-width {
  grid-column: span 2;
}

.field {
  display: flex;
  flex-direction: column;
}

input,
select {
  width: 100%;
  padding: 12px;
  border-radius: 12px;
  border: 1px solid #ddd;
  outline: none;
  transition: 0.3s;
  font-size: 14px;
  box-sizing: border-box;
}

input:focus,
select:focus {
  border-color: #7c3aed;
  box-shadow: 0 0 6px rgba(124, 58, 237, 0.4);
}

.inputError {
  border: 1px solid red;
}

.error-text {
  color: red;
  font-size: 12px;
  margin-top: 4px;
}

button {
  width: 100%;
  margin-top: 1.5rem;
  padding: 12px;
  border: none;
  border-radius: 12px;
  background: #7c3aed;
  color: white;
  font-weight: bold;
  cursor: pointer;
  transition: 0.3s;
}

button:hover {
  background: #6d28d9;
  transform: scale(1.02);
}

.login-text {
  margin-top: 1rem;
  text-align: center;
  font-size: 0.9rem;
}

.login-text a {
  color: #7c3aed;
  font-weight: bold;
  text-decoration: none;
}

@media (max-width: 600px) {
  .form-grid {
    grid-template-columns: 1fr;
  }

  .full-width {
    grid-column: span 1;
  }
}
</style>
