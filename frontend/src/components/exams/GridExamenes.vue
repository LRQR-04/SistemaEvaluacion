<script setup>
import CardExamen from './CardExamen.vue'

const props = defineProps({
  examenes: {
    type: Array,
    default: () => [],
  },
})

const emit = defineEmits(['editar', 'preguntas', 'resultados'])
</script>

<template>
  <div>
    <!-- Estado vacío -->
    <p v-if="examenes.length === 0" class="empty">No hay exámenes registrados</p>

    <!-- Grid de exámenes -->
    <div v-else class="grid">
      <CardExamen
        v-for="examen in examenes"
        :key="examen.id_examen"
        :examen="examen"
        @editar="emit('editar', $event)"
        @preguntas="emit('preguntas', $event)"
        @resultados="emit('resultados', $event)"
      />
    </div>
  </div>
</template>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 18px;
}

.empty {
  text-align: center;
  color: #6b7280;
  font-size: 14px;
  padding: 40px 0;
  background: #f9fafb;
  border: 1px dashed #d1d5db;
  border-radius: 12px;
}
</style>
