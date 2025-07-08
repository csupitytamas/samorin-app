<template>
  <div>
    <h2>Add Arena to Event (ID: {{ eventId }})</h2>
    <form @submit.prevent="createArena">
      <div>
        <label>Arena name:</label>
        <input v-model="arena.name" required>
      </div>
      <button type="submit">Create Arena</button>
    </form>
    <div v-if="successMessage" style="color:green">{{ successMessage }}</div>
    <div v-if="errorMessage" style="color:red">{{ errorMessage }}</div>
  </div>
</template>

<script>
import { createArena } from '@/api/api'

export default {
  name: 'ArenaCreate',
  props: ['eventId'],
  data() {
    return {
      arena: {
        event: this.eventId || '', // automatikusan kitöltve
        name: ''
      },
      successMessage: '',
      errorMessage: ''
    }
  },
  methods: {
    createArena() {
        createArena(this.arena)
      .then(response => {
        const arenaId = response.data.id; // DRF automatikusan visszaadja az id-t
        this.$router.push({ name: 'arena-edit', params: { arenaId } });
      })
        .catch(error => {
          this.errorMessage = "Error: " + (error.response?.data?.detail || error.message);
          this.successMessage = '';
        });
    }
  }
}
</script>