<script setup>
import { Eye } from 'lucide-vue-next'

const props = defineProps({
  examenes: Array,
  pagina: {
    type: Number,
    default: 1,
  },
  limit: {
    type: Number,
    default: 10,
  },
})

const emit = defineEmits(['preguntas'])

const formatDate = (date) => {
  if (!date) return ''

  const [year, month, day] = date.split('T')[0].split('-')

  return new Date(year, month - 1, day).toLocaleDateString('es-MX', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

const getIndex = (index) => {
  return index + 1 + (props.pagina - 1) * props.limit
}

const getDocenteNombre = (examen) => {
  return examen.docente?.usuario
    ? `${examen.docente.usuario.nombre} ${examen.docente.usuario.apellido_paterno} ${examen.docente.usuario.apellido_materno}`
    : 'Sin asignar'
}

const getBadgeClass = (estatus) => {
  switch (estatus) {
    case 'activo':
      return 'activo'
    case 'inactivo':
      return 'inactivo'
    case 'borrador':
      return 'borrador'
    default:
      return ''
  }
}
</script>

<template>
  <div class="table-container">
    <table>
      <!-- HEADER -->
      <thead>
        <tr>
          <th>#</th>
          <th>Examen</th>
          <th>Docente</th>
          <th>Fecha</th>
          <th>Reactivos</th>
          <th>Estatus</th>
          <th>Acciones</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="(examen, index) in examenes" :key="examen.id_examen">
          <!-- INDEX -->
          <td>
            {{ getIndex(index) }}
          </td>

          <!-- EXAMEN -->
          <td class="exam-cell">
            <div class="exam-name">
              {{ examen.nombre_examen }}
            </div>
          </td>

          <!-- DOCENTE -->
          <td>
            {{ getDocenteNombre(examen) }}
          </td>

          <!-- FECHA -->
          <td>
            {{ formatDate(examen.fecha_aplicacion) }}
          </td>

          <!-- REACTIVOS -->
          <td>
            <span class="chip"> {{ examen.total_reactivos }} preguntas </span>
          </td>

          <!-- ESTATUS -->
          <td>
            <span class="badge" :class="getBadgeClass(examen.estatus)">
              {{ examen.estatus }}
            </span>
          </td>

          <!-- ACCIONES -->
          <td class="actions-cell">
            <button class="action-btn" @click="emit('preguntas', examen)">
              <Eye size="16" />
              Ver preguntas
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <p v-if="examenes.length === 0" class="empty">No hay exámenes registrados</p>
  </div>
</template>

<style scoped>
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

.chip {
  background: #ede9fe;
  color: #5b21b6;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
}

.badge {
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 500;
}

.activo {
  background: #dcfce7;
  color: #166534;
}

.inactivo {
  background: #fee2e2;
  color: #991b1b;
}

.borrador {
  background: #e0e7ff;
  color: #3730a3;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  border: none;
  background: #ede9fe;
  color: #5b21b6;
  padding: 3px 12px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
}

.action-btn:hover {
  background: #ddd6fe;
}

.empty {
  text-align: center;
  padding: 20px;
  color: #6b7280;
}
</style>
