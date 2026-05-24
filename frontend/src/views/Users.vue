<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import api from '../services/api'

import ModalUsuario from '../components/ModalUsuario.vue'
import Alerta from '../components/Alerta.vue'

import { useAuthStore } from '../stores/autenticacion.js'
import { Pencil, GraduationCap, Users, UserCheck, FileText, BookOpen } from 'lucide-vue-next'

const auth = useAuthStore()

const registros = ref([])

const page = ref(1)
const total = ref(0)

const vista = ref('todos')

const filtros = ref({
  nombre: '',
  correo: '',
  rol: '',
  estado: '',
  matricula: '',
  grupo: '',
  numero_usuario: '',
})

const modalUsuario = ref(false)

const usuarioSeleccionado = ref(null)

const alertMsg = ref('')
const alertType = ref('success')

/* Cargar usuarios */
const endpointActual = computed(() => {
  if (vista.value === 'estudiantes') return '/estudiantes'
  if (vista.value === 'docentes') return '/docentes'

  return '/usuarios'
})

const cargar = async () => {
  try {
    const res = await api.get(endpointActual.value, {
      params: {
        page: page.value,
        limit: 10,
        nombre: filtros.value.nombre,
        correo: filtros.value.correo,
        rol: filtros.value.rol,
        estado: filtros.value.estado,

        matricula: filtros.value.matricula,
        grupo: filtros.value.grupo,

        numero_usuario: filtros.value.numero_usuario,
      },
    })

    registros.value = res.data.data
    total.value = res.data.total
  } catch (error) {
    mostrarAlerta('Error al cargar registros', 'error')
  }
}

onMounted(cargar)

watch(page, cargar)

watch(vista, () => {
  page.value = 1
  cargar()
})

/* Cambio de vista */
const cambiarVista = (tipo) => {
  vista.value = tipo

  filtros.value = {
    nombre: '',
    correo: '',
    rol: '',
    estado: '',
    matricula: '',
    grupo: '',
    numero_usuario: '',
  }
}

/* Buscar */
const buscar = () => {
  page.value = 1
  cargar()
}

/* Crear */
const nuevo = () => {
  usuarioSeleccionado.value = null
  modalUsuario.value = true
}

/* Editar */
const editar = (usuario) => {
  if (usuario.rol === 'admin' && usuario.id_usuario !== auth.user.user_id) {
    return
  }

  usuarioSeleccionado.value = usuario
  modalUsuario.value = true
}

/* Cambio estado */
const toggleEstado = async (e, usuario) => {
  const nuevoEstado = e.target.checked

  if (usuario.rol === 'admin' && usuario.id_usuario !== auth.user.user_id) {
    e.target.checked = !nuevoEstado

    mostrarAlerta('No puedes modificar otro administrador', 'error')

    return
  }

  const confirmacion = confirm(
    `¿Seguro que deseas ${nuevoEstado ? 'activar' : 'suspender'} este usuario?`,
  )

  if (!confirmacion) {
    e.target.checked = !nuevoEstado
    return
  }

  try {
    await api.patch(`/usuarios/${usuario.id_usuario}/estado`)
    mostrarAlerta('Estado actualizado correctamente')
    await cargar()
  } catch (error) {
    e.target.checked = !nuevoEstado

    const msg = error.response?.data?.detail || 'Error al actualizar estado'
    mostrarAlerta(msg, 'error')
  }
}

/* Navegación */
const verHistorial = (estudiante) => {
  // router.push(`/historial/${estudiante.id_estudiante}`)
}

const verExamenes = (docente) => {
  // router.push(`/docentes/${docente.id_docente}/examenes`)
}

/* Alertas */
const mostrarAlerta = (msg, type = 'success') => {
  alertMsg.value = msg
  alertType.value = type

  setTimeout(() => (alertMsg.value = ''), 10000)
}

/* Paginación */
const totalPages = computed(() => {
  const pages = Math.ceil(total.value / 10)
  return pages > 0 ? pages : 1
})

const handleSuccess = async (msg, type = 'success') => {
  mostrarAlerta(msg, type)

  // Actualizar tabla
  await cargar()
}
</script>

<template>
  <div class="container">
    <Alerta :message="alertMsg" :type="alertType" />

    <div class="header">
      <div>
        <h2>Administración de usuarios</h2>
        <p class="subtitle">Gestiona estudiantes, docentes y usuarios</p>
      </div>

      <button v-if="vista === 'todos'" class="btn-primary" @click="nuevo">+ Nuevo</button>
    </div>

    <!-- Menu superior -->
    <div class="tabs">
      <button class="tab" :class="{ active: vista === 'todos' }" @click="cambiarVista('todos')">
        <Users size="16" />
        Todos
      </button>

      <button
        class="tab"
        :class="{ active: vista === 'estudiantes' }"
        @click="cambiarVista('estudiantes')"
      >
        <GraduationCap size="16" />
        Estudiantes
      </button>

      <button
        class="tab"
        :class="{ active: vista === 'docentes' }"
        @click="cambiarVista('docentes')"
      >
        <UserCheck size="16" />
        Docentes
      </button>
    </div>

    <!-- Filtros -->
    <div class="filters">
      <!-- TODOS -->
      <template v-if="vista === 'todos'">
        <input v-model="filtros.nombre" placeholder="Buscar por nombre" @input="buscar" />
        <input v-model="filtros.correo" placeholder="Buscar por correo" @input="buscar" />

        <select v-model="filtros.rol" @change="buscar">
          <option value="">Todos los roles</option>
          <option value="admin">Admin</option>
          <option value="estudiante">Estudiante</option>
          <option value="docente">Docente</option>
        </select>

        <select v-model="filtros.estado" @change="buscar">
          <option value="">Todos</option>
          <option value="activo">Activo</option>
          <option value="inactivo">Inactivo</option>
        </select>
      </template>

      <!-- ESTUDIANTES -->
      <template v-if="vista === 'estudiantes'">
        <input v-model="filtros.nombre" placeholder="Buscar por nombre" @input="buscar" />
        <input v-model="filtros.matricula" placeholder="Buscar por matrícula" @input="buscar" />
        <input v-model="filtros.grupo" placeholder="Buscar por grupo" @input="buscar" />
      </template>

      <!-- DOCENTES -->
      <template v-if="vista === 'docentes'">
        <input v-model="filtros.nombre" placeholder="Buscar por nombre" @input="buscar" />
        <input v-model="filtros.numero_usuario" placeholder="Número de usuario" @input="buscar" />
      </template>
    </div>

    <!-- Tabla -->
    <div class="table-container">
      <table>
        <!-- TODOS -->
        <template v-if="vista === 'todos'">
          <thead>
            <tr>
              <th>#</th>
              <th>Nombre completo</th>
              <th>Correo</th>
              <th>Rol</th>
              <th>Estatus</th>
              <th>Acciones</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="(usuario, index) in registros" :key="usuario.id_usuario">
              <td>{{ index + 1 }}</td>
              <td class="user-cell">
                <div class="avatar">
                  {{ usuario.nombre?.charAt(0)?.toUpperCase() }}
                </div>
                {{
                  usuario.nombre + ' ' + usuario.apellido_paterno + ' ' + usuario.apellido_materno
                }}
              </td>
              <td>{{ usuario.email }}</td>
              <td>
                <span class="badge">
                  {{ usuario.rol }}
                </span>
              </td>
              <td>
                <label class="switch">
                  <input
                    type="checkbox"
                    :checked="usuario.estado === 'activo'"
                    @change="(e) => toggleEstado(e, usuario)"
                  />
                  <span class="slider"></span>
                </label>
              </td>
              <td>
                <button class="icon-btn" @click="editar(usuario)">
                  <Pencil size="16" />
                </button>
              </td>
            </tr>
          </tbody>
        </template>

        <!-- ESTUDIANTES -->
        <template v-if="vista === 'estudiantes'">
          <thead>
            <tr>
              <th>#</th>
              <th>Nombre</th>
              <th>Matrícula</th>
              <th>Grupo</th>
              <th>Acciones</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="(estudiante, index) in registros" :key="estudiante.id_estudiante">
              <td>{{ index + 1 }}</td>
              <td>
                {{
                  estudiante.usuario.nombre +
                  ' ' +
                  estudiante.usuario.apellido_paterno +
                  ' ' +
                  estudiante.usuario.apellido_materno
                }}
              </td>
              <td>
                {{ estudiante.matricula }}
              </td>
              <td>
                {{ estudiante.grupo }}
              </td>
              <td>
                <button class="action-btn" @click="verHistorial(estudiante)">
                  <BookOpen size="16" />
                  Historial académico
                </button>
              </td>
            </tr>
          </tbody>
        </template>

        <!-- DOCENTES -->
        <template v-if="vista === 'docentes'">
          <thead>
            <tr>
              <th>#</th>
              <th>Nombre</th>
              <th>Número usuario</th>
              <th>Especialidad</th>
              <th>Acciones</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="(docente, index) in registros" :key="docente.id_docente">
              <td>{{ index + 1 }}</td>
              <td>
                {{
                  docente.usuario.nombre +
                  ' ' +
                  docente.usuario.apellido_paterno +
                  ' ' +
                  docente.usuario.apellido_materno
                }}
              </td>
              <td>
                {{ docente.numero_usuario }}
              </td>
              <td>
                {{ docente.especialidad }}
              </td>
              <td>
                <button class="action-btn" @click="verExamenes(docente)">
                  <FileText size="16" />
                  Ver exámenes
                </button>
              </td>
            </tr>
          </tbody>
        </template>
      </table>
      <p v-if="registros.length === 0" class="empty">No se encontraron resultados</p>
    </div>

    <!-- Paginación -->
    <div class="pagination">
      <button @click="page--" :disabled="page === 1">←</button>
      <span>{{ page }} / {{ totalPages }}</span>
      <button @click="page++" :disabled="page === totalPages">→</button>
    </div>

    <!-- Modal -->
    <ModalUsuario
      v-if="modalUsuario"
      :usuario="usuarioSeleccionado"
      @close="modalUsuario = false"
      @success="handleSuccess"
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

.user-cell {
  display: flex;
  align-items: center;
  gap: 10px;
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
</style>
