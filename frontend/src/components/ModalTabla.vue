<script setup>
import { computed } from 'vue'
import { X, Loader2 } from 'lucide-vue-next'

const props = defineProps({
  title: {
    type: String,
    default: 'Información',
  },

  subtitle: {
    type: String,
    default: '',
  },

  columns: {
    type: Array,
    default: () => [],
  },

  rows: {
    type: Array,
    default: () => [],
  },

  loading: {
    type: Boolean,
    default: false,
  },

  emptyMessage: {
    type: String,
    default: 'No hay información disponible',
  },

  width: {
    type: String,
    default: '1000px',
  },
})

const emit = defineEmits(['close'])

const modalStyle = computed(() => ({
  width: props.width,
}))
</script>

<template>
  <div class="overlay" @click.self="emit('close')">
    <div class="modal" :style="modalStyle">
      <!-- HEADER -->
      <div class="header">
        <div>
          <h3>{{ title }}</h3>

          <p v-if="subtitle" class="subtitle">
            {{ subtitle }}
          </p>
        </div>

        <button class="close" @click="emit('close')">
          <X size="18" />
        </button>
      </div>

      <!-- SLOT SUPERIOR -->
      <slot name="top" />

      <!-- TABLA -->
      <div class="table-container">
        <div v-if="loading" class="loading">
          <Loader2 class="spin" size="18" />
          Cargando información...
        </div>

        <table v-else-if="rows.length > 0">
          <thead>
            <tr>
              <th v-for="column in columns" :key="column.key">
                {{ column.label }}
              </th>

              <th v-if="$slots.actions">Acciones</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="(row, index) in rows" :key="index">
              <td v-for="column in columns" :key="column.key">
                {{ row[column.key] }}
              </td>

              <td v-if="$slots.actions">
                <slot name="actions" :row="row" />
              </td>
            </tr>
          </tbody>
        </table>

        <div v-else class="empty">
          {{ emptyMessage }}
        </div>
      </div>

      <!-- SLOT INFERIOR -->
      <slot name="bottom" />
    </div>
  </div>
</template>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal {
  background: white;
  max-width: 95%;
  border-radius: 16px;
  padding: 18px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.18);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.header h3 {
  font-size: 18px;
  margin-bottom: 3px;
}

.subtitle {
  font-size: 13px;
  color: #6b7280;
}

.close {
  width: 34px;
  height: 34px;
  border: none;
  border-radius: 10px;
  background: #f3f4f6;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
}

.table-container {
  overflow-x: auto;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th {
  background: #f9fafb;
  color: #374151;
  font-size: 13px;
  font-weight: 600;
}

th,
td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #f3f4f6;
  font-size: 13px;
}

tbody tr:hover {
  background: #fafafa;
}

.loading,
.empty {
  padding: 24px;
  text-align: center;
  color: #6b7280;
  font-size: 13px;
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  100% {
    transform: rotate(360deg);
  }
}

@media (max-width: 768px) {
  .modal {
    width: 95% !important;
    padding: 14px;
  }

  th,
  td {
    padding: 10px;
    font-size: 12px;
  }
}
</style>
