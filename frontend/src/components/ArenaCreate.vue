<template>
  <div>
    <h2></h2>
    <form @submit.prevent="createArena">
      <div>
        <label>Arena name:</label>
        <input v-model="arena.name" required>
      </div>
      <button type="submit">Create Arena</button>
    </form>
    <div v-if="successMessage" style="color:green">{{ successMessage }}</div>
    <div v-if="errorMessage" style="color:red">{{ errorMessage }}</div>

    <hr>
    <h3>Existing arenas for this event:</h3>
      <ul>
      <li v-for="arena in arenas" :key="arena.id">
        {{ arena.name }}
        <button @click="goToEditArena(arena)" style="margin-left: 10px;">Edit</button>
      </li>
      <li v-if="arenas.length === 0" style="color:gray;">No arenas yet</li>
    </ul>
  </div>
</template>

<script>
import { createArena, fetchArenas } from '@/api/api'

export default {
  name: 'ArenaCreate',
  props: ['eventId'],
  data() {
    return {
      arena: {
        event: this.eventId || '', // auto fill
        name: ''
      },
      successMessage: '',
      errorMessage: '',
      arenas: []
    }
  },
  methods: {
  createArena() {
    createArena(this.arena)
      .then(() => {
        this.successMessage = 'Arena created successfully!';
        this.errorMessage = '';
        this.arena.name = '';
        this.fetchExistingArenas();
      })
      .catch(error => {
        this.errorMessage = "Error: " + (error.response?.data?.detail || error.message);
        this.successMessage = '';
      });
  },
  fetchExistingArenas() {
    fetchArenas()
      .then(response => {
        this.arenas = response.data.filter(a => a.event == this.eventId);
      })
      .catch(() => { this.arenas = []; });
  },
  goToEditArena(arena) {
    this.$router.push({ name: 'arena-edit', params: { arenaId: arena.id } });
  }
},
  mounted() {
    this.fetchExistingArenas();
  }
}
</script>