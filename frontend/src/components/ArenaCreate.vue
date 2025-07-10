<template>
  <div>
    <h2>{{ t('createArena') }}</h2>
    <form @submit.prevent="createArena">
      <div>
        <label>{{ t('arenaName') }}:</label>
        <input v-model="arena.name" required />
      </div>
      <button type="submit">{{ t('createArenaButton') }}</button>
    </form>
    <div v-if="successMessage" style="color:green">{{ successMessage }}</div>
    <div v-if="errorMessage" style="color:red">{{ errorMessage }}</div>

    <hr />
    <h3>{{ t('existingArenas') }}</h3>
    <ul>
      <li v-for="arena in arenas" :key="arena.id">
        {{ arena.name }}
        <button @click="goToEditArena(arena)" style="margin-left: 10px;">{{ t('edit') }}</button>
      </li>
      <li v-if="arenas.length === 0" style="color:gray;">{{ t('noArenasYet') }}</li>
    </ul>
  </div>
</template>

<script>
import { createArena, fetchArenas } from '@/api/api'
import { mapState } from 'vuex'
import translations from '@/translations'

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
  computed: {
    ...mapState(['lang']),
    t() {
      return key => translations[this.lang]?.[key] || key
    }
  },
  methods: {
    createArena() {
      createArena(this.arena)
        .then(() => {
          this.successMessage = this.t('arenaCreated');
          this.errorMessage = '';
          this.arena.name = '';
          this.fetchExistingArenas();
        })
        .catch(error => {
          this.errorMessage = this.t('error') + ": " + (error.response?.data?.detail || error.message);
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
