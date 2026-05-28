<script setup>
import { FileText, Pencil, ClipboardList, BarChart3, Calendar, Calendar1 } from 'lucide-vue-next'
import { computed } from 'vue'

const props = defineProps({
  examen: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['editar', 'preguntas', 'resultados'])

/* Formatear fecha */
const formatDate = (date) => {
  if (!date) return ''

  const [year, month, day] = date.split('T')[0].split('-')

  const months = [
    'ene',
    'feb',
    'mar',
    'abr',
    'may',
    'jun',
    'jul',
    'ago',
    'sep',
    'oct',
    'nov',
    'dic',
  ]

  return `${parseInt(day)} ${months[parseInt(month) - 1]} ${year}`
}

/* Badge dinámico de estatus */
const badgeClass = computed(() => {
  const status = props.examen?.estatus

  if (status === 'activo') return 'activo'
  if (status === 'inactivo') return 'inactivo'
  if (status === 'borrador') return 'borrador'

  return ''
})
</script>

<template>
  <div class="card">
    <!-- HEADER -->
    <div class="top">
      <div class="icon">
        <FileText size="18" />
      </div>

      <span class="badge" :class="badgeClass">
        {{ examen.estatus }}
      </span>
    </div>

    <!-- TITULO -->
    <h3 class="title">
      {{ examen.nombre_examen || 'Sin título' }}
    </h3>

    <div class="info">
      <span> {{ examen.total_reactivos || 0 }} preguntas </span>
    </div>

    <!-- FECHA -->
    <div class="fecha"><Calendar size="16" /> {{ formatDate(examen.fecha_aplicacion) }}</div>

    <!-- ACCIONES -->
    <div class="actions">
      <button @click="emit('preguntas', examen)">
        <ClipboardList size="16" />
        Preguntas
      </button>

      <button @click="emit('editar', examen)">
        <Pencil size="16" />
        Editar
      </button>

      <button @click="emit('resultados', examen)">
        <BarChart3 size="16" />
        Resultados
      </button>
    </div>
  </div>
</template>

<style scoped>
.card {
  background: white;
  border-radius: 18px;
  padding: 18px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
  transition: 0.2s;
}

.card:hover {
  transform: translateY(-3px);
}

.top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
}

.icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: #ede9fe;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #5b21b6;
}

.badge {
  padding: 5px 10px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
}

/* Estados */
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

.title {
  font-size: 16px;
  font-weight: 600;
  margin: 10px 0;
}

.descripcion {
  color: #6b7280;
  margin: 10px 0;
  font-size: 13px;
}

.info {
  display: flex;
  gap: 12px;
  margin-top: 10px;
  font-size: 13px;
  color: #4b5563;
}

.fecha {
  margin-top: 12px;
  color: #6b7280;
  font-size: 13px;
}

.actions {
  margin-top: 18px;
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.actions button {
  border: none;
  background: #f3f4f6;
  padding: 8px 12px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  font-size: 13px;
  transition: 0.2s;
}

.actions button:hover {
  background: #e5e7eb;
}
</style>
