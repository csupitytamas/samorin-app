<template>
  <div>
    <h2>{{ t('editEvent') }}</h2>
    <form @submit.prevent="saveEvent">
      <div>
        <label>{{ t('name') }}:</label>
        <input v-model="event.name" required />
      </div>
      <div>
        <label>{{ t('startDate') }}:</label>
        <input type="date" v-model="event.start_date" required />
      </div>
      <div>
        <label>{{ t('endDate') }}:</label>
        <input type="date" v-model="event.end_date" required />
      </div>
      <button type="submit">{{ t('save') }}</button>
      <button @click="archiveEvent" type="button" style="color:orange;">{{ t('closeEvent') }}</button>
    </form>

    <div v-if="successMessage" style="color:green; margin-top:10px;">{{ successMessage }}</div>
    <div v-if="errorMessage" style="color:red; margin-top:10px;">{{ errorMessage }}</div>

    <h3>{{ t('arenas') }}</h3>
    <ul>
      <li v-for="arena in arenas" :key="arena.id" style="margin-bottom: 10px;">
        <template v-if="editingArenaId === arena.id">
          <input
            v-model="arenaNewName"
            @keyup.enter="saveArenaName(arena)"
            @blur="saveArenaName(arena)"
            style="width:120px;"
          />
          <button @click="saveArenaName(arena)">{{ t('save') }}</button>
          <button @click="cancelEditArena">{{ t('cancel') }}</button>
        </template>
        <template v-else>
          {{ arena.name }}
          <button @click="startEditArena(arena)">{{ t('edit') }}</button>
        </template>
      </li>
      <li v-if="arenas.length === 0" style="color:gray;">{{ t('noArenas') }}</li>
    </ul>
  </div>
</template>

<script>
import { fetchEvent, updateEvent, archiveEvent, fetchArenas, updateArena } from '@/api/api'
import { mapState } from 'vuex'
import translations from '@/translations'

export default {
  name: "EventEdit",
  props: ['id'],
  data() {
    return {
      event: { name: '', start_date: '', end_date: '' },
      arenas: [],
      successMessage: '',
      errorMessage: '',
      editingArenaId: null,
      arenaNewName: ""
    }
  },
  computed: {
    ...mapState(['lang']),
    t() {
      return key => translations[this.lang]?.[key] || key
    }
  },
  methods: {
    loadData() {
      fetchEvent(this.id)
        .then(res => { this.event = res.data; })
        .catch(() => { this.errorMessage = this.t('couldNotLoadEvent'); });

      fetchArenas()
        .then(res => {
          this.arenas = res.data.filter(a => a.event == this.id);
        })
        .catch(() => { this.arenas = []; });
    },
    saveEvent() {
      updateEvent(this.id, this.event)
        .then(() => {
          this.successMessage = this.t('eventSaved');
          this.errorMessage = "";
          this.$router.push('/events/list');
        })
        .catch(() => {
          this.successMessage = "";
          this.errorMessage = this.t('couldNotSaveEvent');
        });
    },
    archiveEvent() {
      if (!confirm(this.t('confirmCloseEvent'))) return;
      archiveEvent(this.id)
        .then(() => {
          this.successMessage = this.t('eventArchived');
          this.errorMessage = "";
          this.$router.push('/events/list');
        })
        .catch(() => {
          this.successMessage = "";
          this.errorMessage = this.t('couldNotArchiveEvent');
        });
    },
    startEditArena(arena) {
      this.editingArenaId = arena.id;
      this.arenaNewName = arena.name;
    },
    cancelEditArena() {
      this.editingArenaId = null;
      this.arenaNewName = "";
    },
    saveArenaName(arena) {
      if (!this.arenaNewName.trim() || this.arenaNewName === arena.name) {
        this.cancelEditArena();
        return;
      }
      updateArena(arena.id, { name: this.arenaNewName })
        .then(() => {
          this.loadData();
          this.cancelEditArena();
        })
        .catch(() => {
          alert(this.t('couldNotRenameArena'));
        });
    }
  },
  mounted() {
    this.loadData();
  }
}
</script>
