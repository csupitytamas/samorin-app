<template>
  <div class="container">
    <h2>{{ t('createArena') }}</h2>
    <div class="box-border">
      <form @submit.prevent="createArena" class="inline-form row">
        <div style="flex:1; min-width:200px;">
          <input v-model="arena.name" :placeholder="t('arenaName')" required />
        </div>
        <button type="submit">{{ t('createArenaButton') }}</button>
      </form>
      <div v-if="successMessage" style="color:green; margin-top:10px; text-align:center;">
        {{ successMessage }}
      </div>
      <div v-if="errorMessage" style="color:red; margin-top:10px; text-align:center;">
        {{ errorMessage }}
      </div>
    </div>

    <h3>{{ t('existingArenas') }}</h3>
    <div class="box-border" v-if="arenas.length > 0">
      <ul style="list-style:none; padding:0;">
        <li v-for="arena in arenas" :key="arena.id" style="margin:8px 0; display:flex; justify-content:space-between; align-items:center;">
          <span style="font-weight:bold;">{{ arena.name }}</span>
          <button @click="goToEditArena(arena)" style="padding: 4px 12px;">{{ t('edit') }}</button>
        </li>
      </ul>
    </div>
    <div v-else class="muted" style="text-align:center; margin-top:1rem;">
      {{ t('noArenasYet') }}
    </div>
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